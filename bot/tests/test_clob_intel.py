"""
OracleFarming -- CLOB Intelligence Prototype

Runs the pipeline to get matched games, then for each LIVE game:
  1. Fetches BBO (best bid/offer) from the Polymarket SDK
  2. Compares current price vs sharp odds to find PANIC situations
  3. For detected panics, shows full analysis and recommended action
  4. Simulates profit if price corrects 50% toward fair value

Run:
  cd /home/user/PolyFarm/bot && PYTHONPATH=. python3 tests/test_clob_intel.py
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
BALANCE = PAPER_SEED_BALANCE

# Panic detection thresholds
PANIC_EDGE_THRESHOLD = 0.05  # 5%+ gap between price and sharp = potential panic
PANIC_DROP_THRESHOLD = 0.05  # 5%+ drop from recent price levels


def classify_band(price: float):
    if price >= BAND_A_MIN_PRICE:
        return "A", BAND_A_MIN_EDGE, BAND_A_POSITION_PCT
    if BAND_B_MIN_PRICE <= price < BAND_B_MAX_PRICE:
        return "B", BAND_B_MIN_EDGE, BAND_B_POSITION_PCT
    if BAND_C_MIN_PRICE <= price < BAND_C_MAX_PRICE:
        return "C", BAND_C_MIN_EDGE, BAND_C_POSITION_PCT
    return None


def get_team_analysis(home_team: str, away_team: str):
    """Check dominant/fade status for both teams."""
    analysis = {"dominant": None, "fade": None}
    for tname, data in DOMINANT_TEAMS.items():
        if tname.lower() in home_team.lower() or tname.lower() in away_team.lower():
            analysis["dominant"] = {
                "team": tname,
                "comeback_rate": data.get("comeback_win_rate_when_trailing", 0),
                "overreaction": data.get("market_overreaction_tendency", ""),
                "notes": data.get("notes", ""),
            }
            break
    for tname, data in FADE_TEAMS.items():
        if tname.lower() in home_team.lower() or tname.lower() in away_team.lower():
            analysis["fade"] = {
                "team": tname,
                "confidence": data.get("confidence", ""),
                "reason": data.get("reason", ""),
            }
            break
    return analysis


def assess_risk(edge: float, is_live: bool, game_score: str,
                sport: str, team_analysis: dict):
    """Return a list of risk factors."""
    risks = []
    if not is_live:
        risks.append("Game not live yet -- price may not correct until tip-off")
    if edge > 0.15:
        risks.append(f"Edge {edge:.1%} is unusually large -- check for news/injury")
    if is_live and game_score:
        try:
            parts = str(game_score).split("-")
            s1, s2 = int(parts[0].strip()), int(parts[1].strip())
            diff = abs(s1 - s2)
            if "basketball" in sport and diff > 20:
                risks.append(f"Blowout score ({game_score}) -- correction unlikely")
            if "baseball" in sport and diff > 5:
                risks.append(f"Large run differential ({game_score})")
            if "hockey" in sport and diff > 3:
                risks.append(f"Large goal differential ({game_score})")
        except Exception:
            pass
    if team_analysis.get("fade") and team_analysis["fade"]["confidence"] in ("very_high", "high"):
        fade_team = team_analysis["fade"]["team"]
        risks.append(f"Fade team {fade_team} involved -- verify we're on correct side")
    if not risks:
        risks.append("No elevated risk factors detected")
    return risks


async def fetch_bbo(client, slug: str) -> dict:
    """Fetch BBO for a market slug using the SDK client."""
    try:
        result = await client.markets.bbo(slug)
        if result and hasattr(result, "marketData"):
            md = result.marketData
            best_bid = None
            best_ask = None
            current_px = None
            if hasattr(md, "bestBid") and md.bestBid:
                best_bid = float(md.bestBid.value) if hasattr(md.bestBid, "value") else None
            if hasattr(md, "bestAsk") and md.bestAsk:
                best_ask = float(md.bestAsk.value) if hasattr(md.bestAsk, "value") else None
            if hasattr(md, "currentPx") and md.currentPx:
                current_px = float(md.currentPx.value) if hasattr(md.currentPx, "value") else None
            return {
                "best_bid": best_bid,
                "best_ask": best_ask,
                "current_px": current_px,
                "spread": round(best_ask - best_bid, 4) if best_bid and best_ask else None,
            }
        # Try dict access as fallback
        if isinstance(result, dict):
            md = result.get("marketData", {})
            bb = md.get("bestBid", {})
            ba = md.get("bestAsk", {})
            cp = md.get("currentPx", {})
            best_bid = float(bb.get("value", 0)) if bb else None
            best_ask = float(ba.get("value", 0)) if ba else None
            current_px = float(cp.get("value", 0)) if cp else None
            return {
                "best_bid": best_bid,
                "best_ask": best_ask,
                "current_px": current_px,
                "spread": round(best_ask - best_bid, 4) if best_bid and best_ask else None,
            }
    except Exception as e:
        return {"error": str(e)}
    return {"error": "no data"}


async def run_clob_intel():
    print("=" * 70)
    print("  OracleFarming -- CLOB Intelligence Prototype")
    print(f"  {datetime.now(ET).strftime('%Y-%m-%d %I:%M %p ET')}")
    print(f"  Paper balance: ${BALANCE:,.0f}")
    print("=" * 70)

    # ── Initialize pipeline ─────────────────────────────
    ssl_ctx = ssl.create_default_context()
    pipeline = Pipeline(odds_api_key=ODDS_API_KEY, db=None)
    pipeline._http = httpx.AsyncClient(timeout=20, verify=ssl_ctx)

    # ── Run pipeline steps 1-8 ──────────────────────────
    print("\n--- Running pipeline (steps 1-8) ---")
    steps = [
        ("Step 1: Leagues", pipeline.step1_discover_leagues),
        ("Step 2: Teams", pipeline.step2_load_teams),
        ("Step 3: Odds keys", pipeline.step3_discover_odds_keys),
        ("Step 4: Odds", pipeline.step4_load_odds),
        ("Step 5: Match teams", pipeline.step5_match_teams),
        ("Step 6: Games", pipeline.step6_load_games),
        ("Step 7: Match games", pipeline.step7_match_games),
        ("Step 8: Scores", pipeline.step8_load_scores),
    ]
    for label, fn in steps:
        print(f"  {label}...", end=" ", flush=True)
        result = await fn()
        if result is False:
            print("FAILED")
            print(f"FATAL: {label} failed, cannot continue.")
            await pipeline.close()
            return
        print("OK")

    print(f"\n  Pipeline summary:")
    print(f"    Leagues: {len(pipeline.leagues)}")
    print(f"    Teams: {len(pipeline.teams)}")
    print(f"    Games: {len(pipeline.games)}")
    print(f"    Matched: {len(pipeline.matched_games)}")
    print(f"    Scores: {len(pipeline.scores)}")

    # ── Identify live games with edge ───────────────────
    live_games = []
    all_edge_games = []
    for slug, game in pipeline.games.items():
        edge_data = pipeline.get_edge(slug)
        if not edge_data:
            continue
        entry = {
            "slug": slug,
            "game": game,
            "edge": edge_data,
        }
        all_edge_games.append(entry)
        if game.get("is_live"):
            live_games.append(entry)

    print(f"\n  Games with edge: {len(all_edge_games)}")
    print(f"  Live games with edge: {len(live_games)}")

    # ── Initialize SDK client for BBO ───────────────────
    sdk_client = None
    bbo_available = False
    try:
        from polymarket_us import AsyncPolymarketUS
        sdk_client = AsyncPolymarketUS(
            key_id="d9864daf-4b48-4dfb-9234-eba9bd6a173c",
            secret_key="NxAcYppljqMM0NkPBTXYDkylLnyv4fh6nAtK1gQ7JdzMcqY1/j2GERggEvQf5lhDGHih3BvNdD7/fnnuhVtLNQ=="
        )
        bbo_available = True
        print("  SDK client initialized for BBO data.")
    except ImportError:
        print("  WARNING: polymarket_us SDK not available. Using pipeline prices only.")
    except Exception as e:
        print(f"  WARNING: SDK init failed ({e}). Using pipeline prices only.")

    # ── Analyze games: use live first, fall back to all edge games ──
    target_games = live_games if live_games else all_edge_games
    target_label = "LIVE" if live_games else "ALL EDGE"

    print(f"\n{'=' * 70}")
    print(f"  CLOB INTELLIGENCE SCAN -- {target_label} GAMES")
    print(f"{'=' * 70}")

    panics = []
    scanned = 0

    for entry in target_games:
        slug = entry["slug"]
        game = entry["game"]
        edge_data = entry["edge"]
        scanned += 1

        sharp = edge_data["sharp_prob"]
        poly_price = game["yes_price"]
        edge = edge_data["edge"]

        # Fetch BBO if SDK available
        bbo = None
        if bbo_available and sdk_client:
            bbo = await fetch_bbo(sdk_client, slug)
            if bbo and not bbo.get("error"):
                # Use BBO current price if available
                if bbo.get("current_px") and bbo["current_px"] > 0:
                    poly_price = bbo["current_px"]
                    edge = round(sharp - poly_price, 4)

        # Detect panic: large gap between sharp and current price
        is_panic = abs(edge) >= PANIC_EDGE_THRESHOLD

        if is_panic:
            team_analysis = get_team_analysis(game["home_team"], game["away_team"])
            risks = assess_risk(
                edge, game.get("is_live", False),
                game.get("game_score", ""), game.get("sport", ""),
                team_analysis
            )
            band_info = classify_band(poly_price)

            # Simulate 50% correction profit
            correction_target = poly_price + (edge * 0.50)
            shares_possible = int(BALANCE * 0.04 / poly_price) if poly_price > 0 else 0
            entry_cost = shares_possible * poly_price
            correction_profit = round(shares_possible * (correction_target - poly_price), 2)
            fee_total = round(entry_cost * TAKER_FEE_RATE * 2, 2)
            net_profit = round(correction_profit - fee_total, 2)

            panics.append({
                "slug": slug,
                "game": game,
                "edge": edge,
                "sharp": sharp,
                "poly_price": poly_price,
                "bbo": bbo,
                "team_analysis": team_analysis,
                "risks": risks,
                "band": band_info,
                "correction_target": correction_target,
                "shares": shares_possible,
                "entry_cost": entry_cost,
                "correction_profit": correction_profit,
                "fee_total": fee_total,
                "net_profit": net_profit,
            })

    print(f"\n  Scanned: {scanned} games")
    print(f"  Panics detected (>= {PANIC_EDGE_THRESHOLD:.0%} gap): {len(panics)}")

    if panics:
        # Sort by absolute edge descending
        panics.sort(key=lambda x: -abs(x["edge"]))

        print(f"\n{'-' * 70}")
        print(f"  PANIC SITUATIONS DETECTED")
        print(f"{'-' * 70}")

        for i, p in enumerate(panics, 1):
            g = p["game"]
            live_tag = " [LIVE]" if g.get("is_live") else ""
            score_str = f" | Score: {g['game_score']}" if g.get("game_score") else ""
            period_str = f" | Period: {g['game_period']}" if g.get("game_period") else ""
            bucket = g.get("game_bucket", "")

            print(f"\n  --- Panic #{i} ---")
            print(f"  {g['home_team']} vs {g['away_team']}")
            print(f"  League: {g['league'].upper()}{live_tag} | Bucket: {bucket}{score_str}{period_str}")
            print()

            # Price vs Sharp
            direction = "UNDERPRICED" if p["edge"] > 0 else "OVERPRICED"
            print(f"  Current Polymarket price: {p['poly_price']:.2f}c")
            print(f"  Sharp fair value:         {p['sharp']:.2f}c")
            print(f"  Misprice:                 {p['edge']:+.2%} ({direction})")

            # BBO data
            if p["bbo"] and not p["bbo"].get("error"):
                bbo = p["bbo"]
                print(f"  Best bid: {bbo.get('best_bid', 'N/A')}")
                print(f"  Best ask: {bbo.get('best_ask', 'N/A')}")
                spread = bbo.get("spread")
                if spread is not None:
                    print(f"  Spread:   {spread:.4f} ({spread * 100:.2f}c)")

            # Team analysis
            ta = p["team_analysis"]
            print()
            print(f"  Home record: {g.get('home_record', 'N/A')}")
            print(f"  Away record: {g.get('away_record', 'N/A')}")
            if ta["dominant"]:
                d = ta["dominant"]
                print(f"  DOMINANT TEAM: {d['team']}")
                print(f"    Comeback rate: {d['comeback_rate']:.0%}")
                print(f"    Market overreaction: {d['overreaction']}")
                print(f"    Notes: {d['notes']}")
            if ta["fade"]:
                f = ta["fade"]
                print(f"  FADE TEAM: {f['team']} (confidence: {f['confidence']})")
                print(f"    Reason: {f['reason']}")

            # Recommended action
            print()
            band_label = p["band"][0] if p["band"] else "?"
            print(f"  RECOMMENDED ACTION:")
            if p["edge"] > 0:
                print(f"    BUY YES @ {p['poly_price']:.2f}c (Band {band_label})")
                print(f"    Position: {p['shares']} shares (${p['entry_cost']:.0f})")
                print(f"    50% correction target: {p['correction_target']:.2f}c")
                print(f"    Expected profit: ${p['net_profit']:+.2f} "
                      f"(gross ${p['correction_profit']:.2f} - fees ${p['fee_total']:.2f})")
            else:
                print(f"    NO BUY -- price is ABOVE sharp value")
                print(f"    Wait for price to drop or consider opposite side")

            # Risk assessment
            print()
            print(f"  RISKS:")
            for risk in p["risks"]:
                print(f"    - {risk}")

    else:
        print("\n  No panic situations detected.")
        print("  Markets are currently priced within 5% of sharp consensus.")

        # Show closest-to-panic for reference
        if all_edge_games:
            print(f"\n  Closest to panic (top 10 by edge):")
            sorted_edge = sorted(all_edge_games, key=lambda x: -abs(x["edge"]["edge"]))[:10]
            for entry in sorted_edge:
                g = entry["game"]
                e = entry["edge"]
                live = " [LIVE]" if g.get("is_live") else ""
                print(f"    {g['league'].upper():4s}{live:6s} | "
                      f"{g['home_team'][:20]:20s} vs {g['away_team'][:20]:20s} | "
                      f"price {g['yes_price']:.2f} | sharp {e['sharp_prob']:.2f} | "
                      f"edge {e['edge']:+.2%}")

    # ── Simulated Telegram message ──────────────────────
    print(f"\n{'=' * 70}")
    print(f"  SIMULATED TELEGRAM MESSAGE")
    print(f"{'=' * 70}")

    now_et = datetime.now(ET)
    msg = []
    msg.append(f"OracleFarming CLOB Intel | {now_et.strftime('%b %d, %I:%M %p ET')}")
    msg.append("")
    msg.append(f"Pipeline: {len(pipeline.games)} games, "
               f"{len(pipeline.matched_games)} matched, "
               f"{len(live_games)} live")
    msg.append("")

    if panics:
        total_opportunity = sum(p["net_profit"] for p in panics if p["edge"] > 0)
        buy_panics = [p for p in panics if p["edge"] > 0]
        msg.append(f"ALERT: {len(panics)} panic situations detected")
        msg.append(f"Buyable panics: {len(buy_panics)}")
        if buy_panics:
            msg.append(f"Total opportunity: ${total_opportunity:+.2f}")
            msg.append("")
            for p in buy_panics[:3]:
                g = p["game"]
                msg.append(
                    f"  {g['league'].upper()} {g['home_team'][:15]} vs {g['away_team'][:15]}"
                )
                msg.append(
                    f"    {p['poly_price']:.0f}c vs {p['sharp']:.0f}c fair "
                    f"| {p['edge']:+.1%} gap | ${p['net_profit']:+.2f}"
                )
    else:
        msg.append("No panic situations detected.")
        msg.append("Markets efficiently priced within 5% of sharp consensus.")
        if all_edge_games:
            best = max(all_edge_games, key=lambda x: abs(x["edge"]["edge"]))
            g = best["game"]
            e = best["edge"]
            msg.append(f"Largest edge: {g['league'].upper()} "
                       f"{g['home_team'][:15]} vs {g['away_team'][:15]} "
                       f"at {e['edge']:+.1%}")

    msg.append("")
    msg.append("Next CLOB scan in 30 minutes.")

    print()
    for line in msg:
        print(f"  {line}")

    # ── Cleanup ─────────────────────────────────────────
    await pipeline.close()
    if sdk_client and hasattr(sdk_client, "close"):
        try:
            await sdk_client.close()
        except Exception:
            pass

    print(f"\n{'=' * 70}")
    print(f"  CLOB Intelligence scan complete.")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    try:
        asyncio.run(run_clob_intel())
    except KeyboardInterrupt:
        print("\nInterrupted.")
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        traceback.print_exc()
