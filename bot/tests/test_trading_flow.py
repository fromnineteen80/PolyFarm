"""
OracleFarming Trading Flow Test
Runs the complete pipeline and simulates what the edge detector
would do on every live game. No trades placed — just reports
what the bot WOULD do and why.

Run: cd /home/user/PolyFarm/bot && python3 tests/test_trading_flow.py
"""
import asyncio
import sys
import ssl
import logging

logging.basicConfig(
    level=logging.WARNING,
    format='%(message)s'
)

async def test():
    import httpx
    from core.pipeline import Pipeline, normalize_team
    from core.team_registry import lookup_by_polymarket_id
    from config import (
        FAVORITES_FLOOR,
        BAND_A_MIN_PRICE, BAND_A_MIN_EDGE,
        BAND_B_MIN_PRICE, BAND_B_MIN_EDGE,
        BAND_C_MIN_PRICE, BAND_C_MIN_EDGE,
        TAKER_FEE_RATE, MAKER_REBATE_RATE,
        REPRICE_EXIT_PCT,
    )

    print("=" * 70)
    print("ORACLEFARMING TRADING FLOW TEST")
    print("=" * 70)

    # Run pipeline
    p = Pipeline(odds_api_key='fbd86b881d7b58c956f0d45a25b16219', db=None)
    try:
        p._http = httpx.AsyncClient(
            timeout=15,
            verify=ssl.create_default_context()
        )
    except Exception:
        p._http = httpx.AsyncClient(timeout=15)

    print("\n--- Pipeline ---")
    await p.step1_discover_leagues()
    print(f"Leagues: {len(p.leagues)}")
    await p.step2_load_teams()
    print(f"Teams: {len(p.teams)}")
    await p.step3_discover_odds_keys()
    print(f"Odds keys: {len(p.league_to_odds_key)}")
    await p.step4_load_odds()
    print(f"Odds events: {len(p.odds_events)}")
    await p.step5_match_teams()
    print(f"Bridge entries: {len(p.team_bridge)}")
    await p.step6_load_games()
    print(f"Games: {len(p.games)}")
    await p.step7_match_games()
    matched = len(p.matched_games)
    print(f"Matched: {matched}")
    await p.step8_load_scores()

    # Categorize games
    live_games = []
    today_games = []
    upcoming_games = []

    for slug, game in p.games.items():
        edge_data = p.get_edge(slug)
        bucket = game.get("game_bucket", "upcoming")
        entry = {
            "slug": slug,
            "home": game["home_team"],
            "away": game["away_team"],
            "league": game["league"],
            "price": game["yes_price"],
            "is_live": game.get("is_live", False),
            "is_finished": game.get("is_finished", False),
            "score": game.get("game_score", ""),
            "period": game.get("game_period", ""),
            "bucket": bucket,
            "edge_data": edge_data,
        }
        if game.get("is_live"):
            live_games.append(entry)
        elif bucket == "today":
            today_games.append(entry)
        else:
            upcoming_games.append(entry)

    print(f"\nLive: {len(live_games)} | Today: {len(today_games)} | Upcoming: {len(upcoming_games)}")

    # Show live games with edge analysis
    print("\n" + "=" * 70)
    print("LIVE GAMES WITH EDGE ANALYSIS")
    print("=" * 70)

    if not live_games:
        print("No live games right now.")

    for g in live_games:
        ed = g["edge_data"]
        print(f"\n  {g['home']} vs {g['away']} ({g['league']})")
        print(f"    Score: {g['score']} | Period: {g['period']}")
        print(f"    Polymarket price: {g['price']:.2f}")

        if not ed:
            print(f"    NO EDGE DATA (not matched to Odds API)")
            continue

        sharp = ed["sharp_prob"]
        edge = ed["edge"]
        edge_cents = round(edge * 100, 1)
        sign = "+" if edge > 0 else ""
        print(f"    Sharp prob: {sharp:.2f} | Edge: {sign}{edge_cents}c")

        # Would edge detector enter?
        poly_price = g["price"]
        reasons_no = []
        reasons_yes = []

        if poly_price < FAVORITES_FLOOR:
            reasons_no.append(f"price {poly_price:.2f} < floor {FAVORITES_FLOOR}")

        if poly_price >= BAND_A_MIN_PRICE:
            band = "A"
            threshold = BAND_A_MIN_EDGE
            size_pct = 0.04
        elif poly_price >= BAND_B_MIN_PRICE:
            band = "B"
            threshold = BAND_B_MIN_EDGE
            size_pct = 0.025
        elif poly_price >= BAND_C_MIN_PRICE:
            band = "C"
            threshold = BAND_C_MIN_EDGE
            size_pct = 0.015
        else:
            reasons_no.append(f"price {poly_price:.2f} below all bands")
            band = None
            threshold = 999
            size_pct = 0

        if band and edge < threshold:
            reasons_no.append(f"edge {edge_cents}c < Band {band} threshold {threshold*100}c")
        elif band and edge >= threshold:
            reasons_yes.append(f"edge {edge_cents}c >= Band {band} threshold {threshold*100}c")

        # Fee check
        if band and edge >= threshold:
            position_usd = 2400 * size_pct
            shares = int(position_usd / poly_price)
            entry_fee = shares * poly_price * TAKER_FEE_RATE
            net_edge_usd = (edge * shares) - entry_fee
            net_edge_pct = net_edge_usd / position_usd if position_usd > 0 else 0
            if net_edge_pct < threshold:
                reasons_no.append(f"fee-adjusted edge {net_edge_pct*100:.1f}c < threshold")
            else:
                reasons_yes.append(f"fee-adjusted: ${net_edge_usd:.2f} on ${position_usd:.0f}")
                reasons_yes.append(f"{shares} shares at {poly_price:.2f}")

        # Books
        books = ed.get("books_used", [])
        if len(books) < 2:
            reasons_no.append(f"only {len(books)} bookmakers")
        else:
            reasons_yes.append(f"{len(books)} bookmakers")

        if reasons_no:
            print(f"    WOULD NOT ENTER: {', '.join(reasons_no)}")
        elif reasons_yes:
            print(f"    WOULD ENTER Band {band}: {', '.join(reasons_yes)}")

    # Show today's games with edge
    print("\n" + "=" * 70)
    print(f"TODAY'S GAMES WITH EDGE ({len([g for g in today_games if g['edge_data']])})")
    print("=" * 70)

    for g in sorted(today_games, key=lambda x: abs(x["edge_data"]["edge"]) if x["edge_data"] else 0, reverse=True):
        ed = g["edge_data"]
        if not ed:
            continue
        edge_cents = round(ed["edge"] * 100, 1)
        sign = "+" if ed["edge"] > 0 else ""
        print(f"  {g['home'][:25]:25s} vs {g['away'][:25]:25s} | {g['league']:4s} | Poly: {g['price']:.2f} | Sharp: {ed['sharp_prob']:.2f} | Edge: {sign}{edge_cents}c")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    tradeable = 0
    for g in live_games + today_games:
        ed = g["edge_data"]
        if not ed:
            continue
        poly_price = g["price"]
        edge = ed["edge"]
        if poly_price < FAVORITES_FLOOR:
            continue
        if poly_price >= BAND_A_MIN_PRICE and edge >= BAND_A_MIN_EDGE:
            tradeable += 1
        elif poly_price >= BAND_B_MIN_PRICE and edge >= BAND_B_MIN_EDGE:
            tradeable += 1
        elif poly_price >= BAND_C_MIN_PRICE and edge >= BAND_C_MIN_EDGE:
            tradeable += 1

    print(f"Live games: {len(live_games)}")
    print(f"Today games with odds: {len([g for g in today_games if g['edge_data']])}")
    print(f"Games qualifying for entry: {tradeable}")
    print(f"Paper balance: $2,400")
    print(f"Band A position: ${2400 * 0.04:.0f} (4%)")
    print(f"Band B position: ${2400 * 0.025:.0f} (2.5%)")
    print(f"Band C position: ${2400 * 0.015:.0f} (1.5%)")

    await p.close()

if __name__ == "__main__":
    asyncio.run(test())
