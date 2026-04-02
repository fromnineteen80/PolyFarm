"""
OracleFarming -- Oracle Arb Simulation

Runs the full pipeline (steps 1-8), then simulates trades on every
game with detectable edge.  For each qualifying signal it shows:
  - Entry price, band, position size
  - Sharp odds vs Polymarket price
  - Intelligent position evaluator decision
  - Simulated outcome (WIN if sharp_prob > entry, LOSS otherwise)

At the end it prints a simulated Telegram investor summary.

Run:
  cd /home/user/PolyFarm/bot && PYTHONPATH=. python3 tests/test_oracle_arb.py
"""

import asyncio
import os
import ssl
import sys
import traceback
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# ── path setup ──────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx
from core.pipeline import Pipeline, normalize_team
from config import (
    BAND_A_MIN_PRICE, BAND_A_MIN_EDGE, BAND_A_POSITION_PCT,
    BAND_B_MIN_PRICE, BAND_B_MAX_PRICE, BAND_B_MIN_EDGE, BAND_B_POSITION_PCT,
    BAND_C_MIN_PRICE, BAND_C_MAX_PRICE, BAND_C_MIN_EDGE, BAND_C_POSITION_PCT,
    PAPER_SEED_BALANCE, TAKER_FEE_RATE,
    DOMINANT_TEAMS, FADE_TEAMS,
)

ET = ZoneInfo("America/New_York")
ODDS_API_KEY = "fbd86b881d7b58c956f0d45a25b16219"
BALANCE = PAPER_SEED_BALANCE  # $2,400


# ────────────────────────────────────────────────────────
# Band classification
# ────────────────────────────────────────────────────────
def classify_band(price: float):
    """Return (band_label, min_edge, position_pct) or None."""
    if price >= BAND_A_MIN_PRICE:
        return "A", BAND_A_MIN_EDGE, BAND_A_POSITION_PCT
    if BAND_B_MIN_PRICE <= price < BAND_B_MAX_PRICE:
        return "B", BAND_B_MIN_EDGE, BAND_B_POSITION_PCT
    if BAND_C_MIN_PRICE <= price < BAND_C_MAX_PRICE:
        return "C", BAND_C_MIN_EDGE, BAND_C_POSITION_PCT
    return None


# ────────────────────────────────────────────────────────
# Simplified _should_hold_position (mirrors order_manager)
# ────────────────────────────────────────────────────────
def evaluate_position(
    entry_price: float,
    sharp_prob: float,
    home_team: str,
    away_team: str,
    sport: str,
    home_record: str,
    away_record: str,
    game_score: str,
    game_period: str,
    is_live: bool,
    current_bid: float,
):
    """Return (should_hold, reasons_to_hold, reasons_to_exit)."""
    reasons_to_hold = []
    reasons_to_exit = []

    # 1. Sharp odds vs entry
    if sharp_prob > entry_price:
        reasons_to_hold.append(
            f"sharp {sharp_prob:.1%} > entry {entry_price:.1%}"
        )
    else:
        reasons_to_exit.append(
            f"sharp dropped to {sharp_prob:.1%}"
        )

    # 2. Team record
    record = home_record or ""
    if record and "-" in record:
        try:
            parts = record.split("-")
            wins, losses = int(parts[0]), int(parts[1])
            total = wins + losses
            if total > 0:
                wr = wins / total
                if wr >= 0.65:
                    reasons_to_hold.append(f"strong team ({record})")
                elif wr <= 0.35:
                    reasons_to_exit.append(f"weak team ({record})")
        except Exception:
            pass

    # 3. Dominant / fade team
    teams_str = f"{home_team} vs {away_team}"
    for tname, data in DOMINANT_TEAMS.items():
        if tname.lower() in teams_str.lower():
            cwr = data.get("comeback_win_rate_when_trailing", 0)
            reasons_to_hold.append(
                f"dominant: {tname} (comeback {cwr:.0%})"
            )
            break

    for tname, data in FADE_TEAMS.items():
        if tname.lower() in teams_str.lower():
            conf = data.get("confidence", "medium")
            if current_bid > 0.50:
                reasons_to_hold.append(
                    f"opponent is fade team {tname} ({conf})"
                )
            else:
                reasons_to_exit.append(
                    f"may be on fade team {tname}"
                )
            break

    # 4. Sport-specific score context
    if is_live and game_score and "-" in str(game_score):
        try:
            parts = str(game_score).split("-")
            s1, s2 = int(parts[0].strip()), int(parts[1].strip())
            if current_bid > 0.50:
                our_score, their_score = s1, s2
            else:
                our_score, their_score = s2, s1
            deficit = their_score - our_score
            lead = our_score - their_score

            if "basketball" in sport:
                if lead >= 15:
                    reasons_to_hold.append(f"comfortable lead +{lead}")
                elif deficit >= 15:
                    reasons_to_exit.append(f"down {deficit}")
                elif deficit > 0 and not game_period:
                    reasons_to_hold.append(f"down {deficit} early")
            elif "baseball" in sport:
                if lead >= 4:
                    reasons_to_hold.append(f"+{lead} runs")
                elif deficit >= 4:
                    reasons_to_exit.append(f"down {deficit} runs")
            elif "hockey" in sport:
                if lead >= 3:
                    reasons_to_hold.append(f"+{lead} goals")
                elif deficit >= 3:
                    reasons_to_exit.append(f"down {deficit} goals")
            elif "football" in sport:
                if lead >= 17:
                    reasons_to_hold.append(f"3+ score lead +{lead}")
                elif deficit >= 17:
                    reasons_to_exit.append(f"down {deficit}")
            elif "soccer" in sport.lower() or "Soccer" in sport:
                if lead >= 2:
                    reasons_to_hold.append(f"+{lead} goals")
                elif deficit >= 2:
                    reasons_to_exit.append(f"down {deficit} goals")
        except Exception:
            pass

    # 5. Current price
    if current_bid > 0.55:
        reasons_to_hold.append(f"still favored at {current_bid:.0%}")
    elif current_bid < 0.30:
        reasons_to_exit.append(f"heavily unfavored at {current_bid:.0%}")

    hold = len(reasons_to_hold) >= len(reasons_to_exit)
    return hold, reasons_to_hold, reasons_to_exit


# ────────────────────────────────────────────────────────
# Main simulation
# ────────────────────────────────────────────────────────
async def run_simulation():
    print("=" * 70)
    print("  OracleFarming -- Oracle Arb Simulation")
    print(f"  {datetime.now(ET).strftime('%Y-%m-%d %I:%M %p ET')}")
    print(f"  Paper balance: ${BALANCE:,.0f}")
    print("=" * 70)

    # Create pipeline with SSL context for proxy environments
    ssl_ctx = ssl.create_default_context()
    pipeline = Pipeline(odds_api_key=ODDS_API_KEY, db=None)
    # Replace the default httpx client with one that handles SSL
    pipeline._http = httpx.AsyncClient(timeout=20, verify=ssl_ctx)

    # ── Run steps 1-8 (skip 9 = Supabase) ──────────────
    print("\n--- Step 1: Discover leagues ---")
    if not await pipeline.step1_discover_leagues():
        print("FATAL: step 1 failed")
        return
    print(f"  Leagues: {[l['slug'] for l in pipeline.leagues]}")

    print("\n--- Step 2: Load teams ---")
    if not await pipeline.step2_load_teams():
        print("FATAL: step 2 failed")
        return
    print(f"  Teams loaded: {len(pipeline.teams)}")

    print("\n--- Step 3: Map odds keys ---")
    if not await pipeline.step3_discover_odds_keys():
        print("FATAL: step 3 failed")
        return
    print(f"  Mapped: {dict(pipeline.league_to_odds_key)}")

    print("\n--- Step 4: Load odds ---")
    if not await pipeline.step4_load_odds():
        print("FATAL: step 4 failed")
        return
    print(f"  Odds events: {len(pipeline.odds_events)}")

    print("\n--- Step 5: Match teams ---")
    await pipeline.step5_match_teams()
    print(f"  Team bridge entries: {len(pipeline.team_bridge)}")

    print("\n--- Step 6: Load games ---")
    await pipeline.step6_load_games()
    print(f"  Games loaded: {len(pipeline.games)}")

    print("\n--- Step 7: Match games ---")
    await pipeline.step7_match_games()
    print(f"  Matched: {len(pipeline.matched_games)}")

    print("\n--- Step 8: Load scores ---")
    await pipeline.step8_load_scores()
    print(f"  Scores fetched: {len(pipeline.scores)}")

    # ── Evaluate every matched game for edge ────────────
    print("\n" + "=" * 70)
    print("  EDGE SCAN -- All Matched Games")
    print("=" * 70)

    trades = []
    no_edge_count = 0

    for slug, game in sorted(pipeline.games.items(),
                              key=lambda x: x[1].get("league", "")):
        edge_data = pipeline.get_edge(slug)
        if not edge_data:
            no_edge_count += 1
            continue

        price = game["yes_price"]
        sharp = edge_data["sharp_prob"]
        edge = edge_data["edge"]

        band_info = classify_band(price)
        if not band_info:
            continue
        band_label, min_edge, pos_pct = band_info

        # Fee adjustment
        fee_cost = price * TAKER_FEE_RATE * 2  # entry + exit fees
        net_edge = edge - fee_cost

        qualifies = net_edge >= min_edge

        trade_record = {
            "slug": slug,
            "league": game["league"],
            "home": game["home_team"],
            "away": game["away_team"],
            "price": price,
            "sharp": sharp,
            "edge": edge,
            "net_edge": net_edge,
            "band": band_label,
            "min_edge": min_edge,
            "pos_pct": pos_pct,
            "pos_size": round(BALANCE * pos_pct, 2),
            "shares": int(round(BALANCE * pos_pct / price, 0)) if price > 0 else 0,
            "qualifies": qualifies,
            "books": edge_data.get("books_used", []),
            "is_live": game.get("is_live", False),
            "home_record": game.get("home_record", ""),
            "away_record": game.get("away_record", ""),
            "game_score": game.get("game_score", ""),
            "game_period": game.get("game_period", ""),
            "game_bucket": game.get("game_bucket", ""),
            "reversed": edge_data.get("reversed", False),
            "sport": game.get("sport", ""),
        }

        # Simulated outcome: if sharp > price, market corrects toward fair
        # WIN = price moves to sharp value, we profit the edge
        # LOSS = sharp was wrong, we lose ~half the edge on average
        if sharp > price:
            trade_record["sim_outcome"] = "WIN"
            # Correction: price moves 50-80% toward fair value
            correction = edge * 0.65
            trade_record["sim_pnl_per_share"] = round(correction - fee_cost, 4)
        else:
            trade_record["sim_outcome"] = "LOSS"
            # Loss: price moves away by ~30% of the mispricing
            trade_record["sim_pnl_per_share"] = round(-abs(edge) * 0.30 - fee_cost, 4)

        trade_record["sim_pnl"] = round(
            trade_record["sim_pnl_per_share"] * trade_record["shares"], 2
        )

        # Position evaluator
        current_bid = price  # simulate current = entry
        hold, hold_reasons, exit_reasons = evaluate_position(
            entry_price=price,
            sharp_prob=sharp,
            home_team=game["home_team"],
            away_team=game["away_team"],
            sport=game.get("sport", ""),
            home_record=game.get("home_record", ""),
            away_record=game.get("away_record", ""),
            game_score=game.get("game_score", ""),
            game_period=game.get("game_period", ""),
            is_live=game.get("is_live", False),
            current_bid=current_bid,
        )
        trade_record["evaluator_hold"] = hold
        trade_record["hold_reasons"] = hold_reasons
        trade_record["exit_reasons"] = exit_reasons

        trades.append(trade_record)

    # ── Display all trades ──────────────────────────────
    qualifying = [t for t in trades if t["qualifies"]]
    non_qualifying = [t for t in trades if not t["qualifies"]]

    print(f"\n  Total games with odds: {len(trades) + no_edge_count}")
    print(f"  Games with edge data: {len(trades)}")
    print(f"  Qualifying trades (edge >= band threshold): {len(qualifying)}")
    print(f"  Non-qualifying (edge too small): {len(non_qualifying)}")
    print(f"  No odds match: {no_edge_count}")

    if qualifying:
        print("\n" + "-" * 70)
        print("  QUALIFYING TRADES")
        print("-" * 70)

        for i, t in enumerate(qualifying, 1):
            direction = "HOME YES" if not t["reversed"] else "AWAY YES"
            live_tag = " [LIVE]" if t["is_live"] else ""
            score_str = f"  Score: {t['game_score']}" if t["game_score"] else ""

            print(f"\n  Trade #{i}: {t['home']} vs {t['away']}")
            print(f"    League: {t['league'].upper()}{live_tag}{score_str}")
            print(f"    Side: {direction} @ {t['price']:.2f}c")
            print(f"    Sharp fair value: {t['sharp']:.2f}c ({len(t['books'])} books)")
            print(f"    Edge: {t['edge']:+.2%} (net after fees: {t['net_edge']:+.2%})")
            print(f"    Band {t['band']}: threshold {t['min_edge']:.1%}, "
                  f"position {t['pos_pct']:.1%} = ${t['pos_size']:.0f} "
                  f"({t['shares']} shares)")
            print(f"    Records: {t['home_record'] or 'N/A'} vs {t['away_record'] or 'N/A'}")

            # Position evaluator
            if t["evaluator_hold"]:
                print(f"    Evaluator: HOLD")
                for r in t["hold_reasons"]:
                    print(f"      + {r}")
            else:
                print(f"    Evaluator: EXIT")
                for r in t["exit_reasons"]:
                    print(f"      - {r}")

            print(f"    Sim outcome: {t['sim_outcome']} "
                  f"(P&L: ${t['sim_pnl']:+.2f}, "
                  f"per share: {t['sim_pnl_per_share']:+.4f})")

    # ── Show a few non-qualifying for reference ─────────
    if non_qualifying:
        print("\n" + "-" * 70)
        print(f"  NON-QUALIFYING (showing top 10 by edge)")
        print("-" * 70)
        top_near = sorted(non_qualifying, key=lambda x: -abs(x["edge"]))[:10]
        for t in top_near:
            print(f"    {t['league'].upper():4s} | {t['home'][:20]:20s} vs {t['away'][:20]:20s} "
                  f"| {t['price']:.2f}c | sharp {t['sharp']:.2f} "
                  f"| edge {t['edge']:+.2%} | band {t['band']} needs {t['min_edge']:.1%}")

    # ── Simulated P&L summary ───────────────────────────
    print("\n" + "=" * 70)
    print("  SIMULATED P&L SUMMARY")
    print("=" * 70)

    if qualifying:
        wins = [t for t in qualifying if t["sim_outcome"] == "WIN"]
        losses = [t for t in qualifying if t["sim_outcome"] == "LOSS"]
        total_pnl = sum(t["sim_pnl"] for t in qualifying)
        total_deployed = sum(t["pos_size"] for t in qualifying)

        avg_win = (sum(t["sim_pnl"] for t in wins) / len(wins)) if wins else 0
        avg_loss = (sum(t["sim_pnl"] for t in losses) / len(losses)) if losses else 0
        win_rate = len(wins) / len(qualifying) * 100 if qualifying else 0

        print(f"\n  Trades: {len(qualifying)}")
        print(f"  Wins: {len(wins)} | Losses: {len(losses)}")
        print(f"  Win rate: {win_rate:.1f}%")
        print(f"  Avg win: ${avg_win:+.2f} | Avg loss: ${avg_loss:+.2f}")
        print(f"  Total simulated P&L: ${total_pnl:+.2f}")
        print(f"  Capital deployed: ${total_deployed:,.0f} of ${BALANCE:,.0f}")
        print(f"  ROI on deployed: {(total_pnl / total_deployed * 100) if total_deployed > 0 else 0:+.2f}%")
        print(f"  Daily return on balance: {(total_pnl / BALANCE * 100):+.2f}%")

        # Breakdown by league
        print("\n  By league:")
        league_pnl = {}
        for t in qualifying:
            lg = t["league"].upper()
            if lg not in league_pnl:
                league_pnl[lg] = {"count": 0, "pnl": 0, "wins": 0}
            league_pnl[lg]["count"] += 1
            league_pnl[lg]["pnl"] += t["sim_pnl"]
            if t["sim_outcome"] == "WIN":
                league_pnl[lg]["wins"] += 1

        for lg, d in sorted(league_pnl.items(), key=lambda x: -x[1]["pnl"]):
            wr = d["wins"] / d["count"] * 100 if d["count"] > 0 else 0
            print(f"    {lg:5s}: {d['count']:3d} trades, "
                  f"${d['pnl']:+7.2f}, {wr:.0f}% W")

        # Breakdown by band
        print("\n  By band:")
        for band in ["A", "B", "C"]:
            bt = [t for t in qualifying if t["band"] == band]
            if bt:
                bw = len([t for t in bt if t["sim_outcome"] == "WIN"])
                bp = sum(t["sim_pnl"] for t in bt)
                print(f"    Band {band}: {len(bt)} trades, "
                      f"${bp:+.2f}, {bw}/{len(bt)} W")
    else:
        print("\n  No qualifying trades found at this time.")
        print("  This is normal during off-hours or when markets are efficient.")

    # ── Simulated Telegram message ──────────────────────
    print("\n" + "=" * 70)
    print("  SIMULATED TELEGRAM MESSAGE (30-min summary)")
    print("=" * 70)

    now_et = datetime.now(ET)
    msg_lines = []
    msg_lines.append(f"OracleFarming | {now_et.strftime('%b %d, %I:%M %p ET')}")
    msg_lines.append("")

    if qualifying:
        msg_lines.append(f"Pipeline: {len(pipeline.games)} games, "
                         f"{len(pipeline.matched_games)} matched")
        msg_lines.append(f"Signals: {len(qualifying)} qualifying "
                         f"({len([t for t in qualifying if t['is_live']])} live)")
        msg_lines.append("")
        msg_lines.append(f"Simulated trades: {len(qualifying)}")
        msg_lines.append(f"Win rate: {win_rate:.0f}%")
        msg_lines.append(f"P&L: ${total_pnl:+.2f} "
                         f"({total_pnl / BALANCE * 100:+.2f}%)")
        msg_lines.append(f"Balance: ${BALANCE + total_pnl:,.2f}")
        msg_lines.append("")

        # Top 3 trades
        top3 = sorted(qualifying, key=lambda x: -abs(x["sim_pnl"]))[:3]
        msg_lines.append("Top signals:")
        for t in top3:
            msg_lines.append(
                f"  {t['league'].upper()} {t['home'][:15]} vs {t['away'][:15]} "
                f"| {t['edge']:+.1%} edge | {t['sim_outcome']}"
            )
    else:
        msg_lines.append(f"Pipeline: {len(pipeline.games)} games, "
                         f"{len(pipeline.matched_games)} matched")
        msg_lines.append("No qualifying signals this period.")
        msg_lines.append("Markets are efficient or games haven't started.")

    msg_lines.append("")
    msg_lines.append(f"Next scan in 30 minutes.")

    print()
    for line in msg_lines:
        print(f"  {line}")

    # ── Cleanup ─────────────────────────────────────────
    await pipeline.close()
    print("\n" + "=" * 70)
    print("  Simulation complete.")
    print("=" * 70)


if __name__ == "__main__":
    try:
        asyncio.run(run_simulation())
    except KeyboardInterrupt:
        print("\nInterrupted.")
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        traceback.print_exc()
