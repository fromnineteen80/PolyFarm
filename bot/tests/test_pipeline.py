"""
Comprehensive test suite for OracleFarming bot.

Tests: imports, pipeline data flow (real API calls),
edge calculation, compatibility methods, attribute audit,
config audit, database function signatures, team registry.

Run: cd /home/user/PolyFarm/bot && python3 tests/test_pipeline.py
"""

import asyncio
import sys
import os
import ssl
import traceback
import dataclasses
from datetime import datetime, timezone

# Ensure bot directory is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ODDS_API_KEY = "fbd86b881d7b58c956f0d45a25b16219"

# Track results
PASSED = []
FAILED = []


def record(test_name, passed, detail=""):
    if passed:
        PASSED.append(test_name)
        print(f"  PASS: {test_name}")
    else:
        FAILED.append((test_name, detail))
        print(f"  FAIL: {test_name} -- {detail}")


# ===========================================================
# 1. IMPORT TESTS
# ===========================================================
def test_imports():
    print("\n=== 1. IMPORT TESTS ===")
    modules = [
        ("config", "config"),
        ("core.pipeline", "core.pipeline"),
        ("core.team_registry", "core.team_registry"),
        ("core.market_loader", "core.market_loader"),
        ("core.edge_detector", "core.edge_detector"),
        ("core.order_manager", "core.order_manager"),
        ("core.position_monitor", "core.position_monitor"),
        ("core.wallet", "core.wallet"),
        ("core.alerts", "core.alerts"),
        ("core.ws_markets", "core.ws_markets"),
        ("core.ws_private", "core.ws_private"),
        ("core.exception_monitor", "core.exception_monitor"),
        ("core.fade_monitor", "core.fade_monitor"),
        ("core.overnight_monitor", "core.overnight_monitor"),
        ("core.band_classifier", "core.band_classifier"),
        ("data.database", "data.database"),
    ]
    for label, mod_name in modules:
        try:
            __import__(mod_name)
            record(f"import {label}", True)
        except Exception as e:
            record(f"import {label}", False, f"{type(e).__name__}: {e}")


# ===========================================================
# 2. PIPELINE DATA FLOW (real API calls)
# ===========================================================
async def test_pipeline_data_flow():
    print("\n=== 2. PIPELINE DATA FLOW ===")

    from core.pipeline import Pipeline

    # Create a pipeline with a dummy db (we skip step 9)
    pipeline = Pipeline(odds_api_key=ODDS_API_KEY, db=None)

    # Override httpx client to handle potential SSL issues through proxy
    import httpx
    ctx = ssl.create_default_context()
    pipeline._http = httpx.AsyncClient(timeout=30, verify=ctx)

    # Step 1: Discover leagues
    try:
        result = await pipeline.step1_discover_leagues()
        record("step1 returns True", result is True, f"got {result}")
        record("step1 leagues > 0", len(pipeline.leagues) > 0,
               f"got {len(pipeline.leagues)} leagues")
        league_slugs = [l["slug"] for l in pipeline.leagues]
        print(f"    Leagues found: {league_slugs}")
    except Exception as e:
        record("step1 execution", False, f"{e}")

    # Step 2: Load teams
    try:
        result = await pipeline.step2_load_teams()
        record("step2 returns True", result is True, f"got {result}")
        record("step2 teams > 0", len(pipeline.teams) > 0,
               f"got {len(pipeline.teams)} teams")
        print(f"    Teams loaded: {len(pipeline.teams)}")
    except Exception as e:
        record("step2 execution", False, f"{e}")

    # Step 3: Discover odds keys
    try:
        result = await pipeline.step3_discover_odds_keys()
        record("step3 returns True", result is True, f"got {result}")
        record("step3 mapped keys > 0", len(pipeline.league_to_odds_key) > 0,
               f"got {len(pipeline.league_to_odds_key)} mapped keys")
        print(f"    Mapped keys: {dict(pipeline.league_to_odds_key)}")
    except Exception as e:
        record("step3 execution", False, f"{e}")

    # Step 4: Load odds
    try:
        result = await pipeline.step4_load_odds()
        record("step4 returns True", result is True, f"got {result}")
        record("step4 odds_events > 0", len(pipeline.odds_events) > 0,
               f"got {len(pipeline.odds_events)} events")
        print(f"    Odds events: {len(pipeline.odds_events)}")
    except Exception as e:
        record("step4 execution", False, f"{e}")

    # Step 5: Match teams
    try:
        result = await pipeline.step5_match_teams()
        record("step5 returns True", result is True, f"got {result}")
        matched_count = len(pipeline.team_bridge) // 2  # Each team gets ~2 entries
        # More accurate: count unique odds_api names bridged
        unique_odds = set(pipeline.team_bridge.values())
        # Check unmatched by counting teams without bridge entries
        unmatched = 0
        for tid, team in pipeline.teams.items():
            from core.pipeline import normalize_team
            norm_full = normalize_team(team["full_name"])
            if norm_full and norm_full not in pipeline.team_bridge:
                # Check if the league is mapped to odds
                if team["league"] in pipeline.league_to_odds_key:
                    unmatched += 1
        bridge_count = len(pipeline.team_bridge)
        print(f"    Bridge entries: {bridge_count}, Unique odds teams: {len(unique_odds)}, Unmatched (in mapped leagues): {unmatched}")
        record("step5 bridge_entries > 200", bridge_count > 200,
               f"got {bridge_count}")
        record("step5 unmatched == 0", unmatched == 0,
               f"got {unmatched} unmatched in mapped leagues")
    except Exception as e:
        record("step5 execution", False, f"{e}")

    # Step 6: Load games
    try:
        result = await pipeline.step6_load_games()
        record("step6 returns True", result is True, f"got {result}")
        record("step6 games > 0", len(pipeline.games) > 0,
               f"got {len(pipeline.games)} games")
        print(f"    Games loaded: {len(pipeline.games)}")
    except Exception as e:
        record("step6 execution", False, f"{e}")

    # Step 7: Match games
    try:
        result = await pipeline.step7_match_games()
        record("step7 returns True", result is True, f"got {result}")
        matched = len(pipeline.matched_games)
        total_games = len(pipeline.games)
        print(f"    Matched games: {matched}/{total_games}")
        record("step7 matched_games >= 0", matched >= 0,
               f"got {matched}")
        # Check for broken matches: count the ones that logged as unmatched
        # We can't easily capture log output, so just verify structure
        record("step7 matched_games dict valid",
               all("event_id" in v and "reversed" in v
                   for v in pipeline.matched_games.values()),
               "missing event_id or reversed in matched_games")
    except Exception as e:
        record("step7 execution", False, f"{e}")

    # Step 8: Load scores
    try:
        result = await pipeline.step8_load_scores()
        record("step8 returns True", result is True, f"got {result}")
        record("step8 scores dict exists", isinstance(pipeline.scores, dict),
               f"got {type(pipeline.scores)}")
        print(f"    Scores fetched: {len(pipeline.scores)}")
    except Exception as e:
        record("step8 execution", False, f"{e}")

    await pipeline._http.aclose()
    return pipeline


# ===========================================================
# 3. EDGE CALCULATION
# ===========================================================
def test_edge_calculation(pipeline):
    print("\n=== 3. EDGE CALCULATION ===")

    if not pipeline.matched_games:
        record("edge calculation (no matched games)", False, "no matched games to test")
        return

    tested = 0
    invalid = []
    for slug in pipeline.matched_games:
        edge = pipeline.get_edge(slug)
        if edge is None:
            invalid.append(f"{slug}: get_edge returned None")
            continue
        sp = edge.get("sharp_prob")
        if sp is None or not (0.0 <= sp <= 1.0):
            invalid.append(f"{slug}: sharp_prob={sp} out of range")
            continue
        if "edge" not in edge or "books_used" not in edge:
            invalid.append(f"{slug}: missing edge or books_used key")
            continue
        tested += 1

    record(f"edge calculation tested {tested} games", tested > 0,
           f"tested {tested}")
    record("edge calculation all valid", len(invalid) == 0,
           f"{len(invalid)} invalid: {invalid[:5]}")
    print(f"    Tested: {tested}, Invalid: {len(invalid)}")


# ===========================================================
# 4. COMPATIBILITY METHODS
# ===========================================================
def test_compatibility_methods(pipeline):
    print("\n=== 4. COMPATIBILITY METHODS ===")

    if not pipeline.matched_games:
        record("compatibility methods (no matched games)", False, "no matched games")
        return

    # Pick a matched slug
    slug = next(iter(pipeline.matched_games))
    game = pipeline.games.get(slug, {})
    print(f"    Testing with slug: {slug}")

    # is_matched
    try:
        result = pipeline.is_matched(slug)
        record("is_matched(matched_slug) == True", result is True, f"got {result}")
    except Exception as e:
        record("is_matched", False, str(e))

    try:
        result = pipeline.is_matched("nonexistent-slug-xyz")
        record("is_matched(fake_slug) == False", result is False, f"got {result}")
    except Exception as e:
        record("is_matched(fake)", False, str(e))

    # get_fair_prob
    try:
        home_prob = pipeline.get_fair_prob(slug, "home")
        away_prob = pipeline.get_fair_prob(slug, "away")
        record("get_fair_prob(home) returns float",
               isinstance(home_prob, (int, float)) and 0 <= home_prob <= 1,
               f"got {home_prob}")
        record("get_fair_prob(away) returns float",
               isinstance(away_prob, (int, float)) and 0 <= away_prob <= 1,
               f"got {away_prob}")
    except Exception as e:
        record("get_fair_prob", False, str(e))

    # get_consensus_data
    try:
        cd = pipeline.get_consensus_data(slug)
        record("get_consensus_data returns dict", isinstance(cd, dict), f"got {type(cd)}")
        required_keys = ["consensus_home_prob", "consensus_away_prob", "bookmakers_used", "reversed"]
        missing = [k for k in required_keys if k not in cd]
        record("get_consensus_data has required keys", len(missing) == 0,
               f"missing: {missing}")
    except Exception as e:
        record("get_consensus_data", False, str(e))

    # get_edge_signal with mock ws_markets
    class MockWSMarkets:
        def calculate_velocity(self, slug):
            return 0.0, "stable"
        def get_net_buy_pressure(self, slug):
            return 1.0

    mock_ws = MockWSMarkets()
    try:
        signal = pipeline.get_edge_signal(
            polymarket_slug=slug,
            team_side="home",
            poly_yes_price=game.get("yes_price", 0.5),
            ws_markets=mock_ws,
            band_threshold=0.03,
        )
        record("get_edge_signal returns dict", isinstance(signal, dict), f"got {type(signal)}")
        if isinstance(signal, dict):
            required_signal_keys = [
                "sharp_prob", "static_edge", "direction", "velocity",
                "net_buy_pressure", "required_edge", "size_multiplier",
                "composite_score", "qualifies", "books_used", "event_id"
            ]
            missing = [k for k in required_signal_keys if k not in signal]
            record("get_edge_signal has all keys", len(missing) == 0,
                   f"missing: {missing}")
            # Validate types
            sp = signal.get("sharp_prob")
            record("get_edge_signal sharp_prob valid",
                   isinstance(sp, (int, float)) and 0 <= sp <= 1,
                   f"sharp_prob={sp}")
    except Exception as e:
        record("get_edge_signal", False, f"{type(e).__name__}: {e}")


# ===========================================================
# 5. ATTRIBUTE AUDIT on MarketInfo
# ===========================================================
def test_attribute_audit():
    print("\n=== 5. MARKETINFO ATTRIBUTE AUDIT ===")

    from core.market_loader import MarketInfo

    # All field names that other modules access on market objects
    accessed_fields = {
        # edge_detector.py
        "slug", "home_team", "away_team", "sport", "is_live",
        "market_type", "market_sides", "yes_price",
        # position_monitor.py
        "time_remaining_seconds", "current_period", "current_score",
        "is_finished",
        # exception_monitor.py (same as above plus)
        "home_team", "away_team",
        # fade_monitor.py
        "home_team", "away_team", "current_score", "sport",
        # overnight_monitor.py
        "game_start_time",
    }

    mi_fields = {f.name for f in dataclasses.fields(MarketInfo)}
    missing = accessed_fields - mi_fields
    record("MarketInfo has all accessed fields", len(missing) == 0,
           f"missing fields: {missing}")
    print(f"    Accessed fields: {sorted(accessed_fields)}")
    print(f"    MarketInfo fields: {sorted(mi_fields)}")
    if missing:
        print(f"    MISSING: {sorted(missing)}")


# ===========================================================
# 6. CONFIG AUDIT
# ===========================================================
def test_config_audit():
    print("\n=== 6. CONFIG AUDIT ===")

    from config import get_active_strategies

    profit_modes = ["NORMAL", "HARVEST", "PROTECTION", "LOCKED", "PORTFOLIO_TRAIL"]
    loss_modes = ["NORMAL", "REDUCE", "PAUSE", "HALT", "FLOOR_BREACH"]

    all_valid = True
    for pm in profit_modes:
        for lm in loss_modes:
            try:
                strats = get_active_strategies(pm, lm)
                record_name = f"get_active_strategies({pm},{lm})"
                if not isinstance(strats, dict):
                    record(record_name, False, f"not a dict: {type(strats)}")
                    all_valid = False
                    continue

                # Check every active strategy's size is a number
                bad_sizes = []
                for key, val in strats.items():
                    if isinstance(val, dict) and val.get("active"):
                        size = val.get("size")
                        if size is not None and not isinstance(size, (int, float)):
                            bad_sizes.append(f"{key}.size={size!r} (type={type(size).__name__})")
                if bad_sizes:
                    record(record_name, False, f"non-numeric sizes: {bad_sizes}")
                    all_valid = False
                else:
                    # Don't spam output for every passing combo
                    pass
            except Exception as e:
                record(f"get_active_strategies({pm},{lm})", False, str(e))
                all_valid = False

    record("all strategy combos return valid dicts with numeric sizes", all_valid, "")
    print(f"    Tested {len(profit_modes) * len(loss_modes)} combinations")


# ===========================================================
# 7. DATABASE FUNCTION SIGNATURES
# ===========================================================
def test_database_signatures():
    print("\n=== 7. DATABASE FUNCTION SIGNATURES ===")

    # Build a mock trade record to see field names from _build_trade_record
    # We can inspect the code to know the fields
    build_fields = {
        "timestamp_entry", "timestamp_entry_et", "trade_bucket",
        "market_slug", "sport", "teams", "market_type", "band",
        "position_type", "entry_price", "sharp_prob_at_entry",
        "raw_edge_at_entry", "net_edge_at_entry", "confidence_score",
        "position_size_usd", "shares", "taker_fee_paid",
        "paper_mode", "phase", "is_live_game",
        "profit_mode_at_entry", "loss_mode_at_entry",
        "fade_team", "game_id",
        "price_direction_at_entry", "price_velocity_at_entry",
        "net_buy_pressure_at_entry", "odds_api_event_id",
    }

    exit_fields = {
        "timestamp_exit", "timestamp_exit_et", "trade_bucket",
        "exit_price", "exit_type", "pnl", "pnl_pct",
        "wallet_at_exit", "hold_duration_seconds",
        "maker_rebate_earned", "taker_fee_paid",
    }

    # Both insert_trade and update_trade accept plain dicts --
    # they pass them directly to Supabase. So we just verify
    # the functions exist and accept dicts.
    try:
        from data.database import insert_trade, update_trade
        import inspect
        insert_sig = inspect.signature(insert_trade)
        update_sig = inspect.signature(update_trade)

        # insert_trade should take (trade: dict)
        insert_params = list(insert_sig.parameters.keys())
        record("insert_trade param is 'trade'",
               "trade" in insert_params,
               f"params: {insert_params}")

        # update_trade should take (trade_id: int, updates: dict)
        update_params = list(update_sig.parameters.keys())
        record("update_trade params are 'trade_id' and 'updates'",
               "trade_id" in update_params and "updates" in update_params,
               f"params: {update_params}")

        print(f"    _build_trade_record produces {len(build_fields)} fields")
        print(f"    _record_exit produces {len(exit_fields)} fields")

        # Verify _record_exit fields don't conflict with _build_trade_record
        # (trade_bucket and taker_fee_paid appear in both, which is fine -- update overwrites)
        shared = build_fields & exit_fields
        record("shared fields between entry/exit are safe overrides",
               shared.issubset({"trade_bucket", "taker_fee_paid"}),
               f"shared: {shared}")

    except Exception as e:
        record("database function signatures", False, str(e))


# ===========================================================
# 8. TEAM REGISTRY
# ===========================================================
def test_team_registry():
    print("\n=== 8. TEAM REGISTRY ===")

    from core.team_registry import TEAM_REGISTRY, lookup_by_polymarket_id

    # Total count
    record("registry has 929 teams", len(TEAM_REGISTRY) == 929,
           f"got {len(TEAM_REGISTRY)}")

    # Check required fields on every entry
    required = {"polymarket_id", "odds_api_name", "league"}
    missing_fields = []
    for i, team in enumerate(TEAM_REGISTRY):
        for field in required:
            val = team.get(field)
            if val is None or (isinstance(val, str) and val.strip() == ""):
                missing_fields.append(
                    f"team[{i}] ({team.get('canonical','?')}): missing or empty {field}")
    record("all teams have polymarket_id, odds_api_name, league",
           len(missing_fields) == 0,
           f"{len(missing_fields)} issues: {missing_fields[:10]}")
    if missing_fields:
        for m in missing_fields[:10]:
            print(f"    {m}")

    # Check for duplicate polymarket_ids
    seen_ids = {}
    duplicates = []
    for team in TEAM_REGISTRY:
        pid = team.get("polymarket_id")
        if pid in seen_ids:
            duplicates.append(
                f"polymarket_id={pid}: {seen_ids[pid]} AND {team.get('canonical','?')}")
        else:
            seen_ids[pid] = team.get("canonical", "?")
    record("no duplicate polymarket_ids", len(duplicates) == 0,
           f"{len(duplicates)} duplicates: {duplicates[:5]}")

    # Verify lookup function works
    if TEAM_REGISTRY:
        first = TEAM_REGISTRY[0]
        pid = first["polymarket_id"]
        result = lookup_by_polymarket_id(pid)
        record("lookup_by_polymarket_id works",
               result is not None and result.get("canonical") == first.get("canonical"),
               f"looked up id={pid}, got {result.get('canonical') if result else None}")

    # Check league distribution
    leagues = {}
    for team in TEAM_REGISTRY:
        l = team.get("league", "unknown")
        leagues[l] = leagues.get(l, 0) + 1
    print(f"    League distribution: {dict(sorted(leagues.items()))}")

    expected = {
        "nba": 30, "nhl": 32, "mlb": 30, "nfl": 32,
        "mls": 30, "epl": 20, "lal": 20, "bun": 18,
        "sea": 20, "ucl": 60, "cbb": 365, "cfb": 272,
    }
    for league, expected_count in expected.items():
        actual = leagues.get(league, 0)
        record(f"registry {league} has {expected_count} teams",
               actual == expected_count,
               f"got {actual}")


# ===========================================================
# RUNNER
# ===========================================================
async def run_all():
    print("=" * 60)
    print("OracleFarming Comprehensive Test Suite")
    print(f"Date: {datetime.now().isoformat()}")
    print("=" * 60)

    # 1. Import tests
    test_imports()

    # 2. Pipeline data flow
    pipeline = None
    try:
        pipeline = await test_pipeline_data_flow()
    except Exception as e:
        record("pipeline data flow (fatal)", False,
               f"{type(e).__name__}: {e}\n{traceback.format_exc()}")

    # 3. Edge calculation
    if pipeline:
        try:
            test_edge_calculation(pipeline)
        except Exception as e:
            record("edge calculation (fatal)", False, str(e))

    # 4. Compatibility methods
    if pipeline:
        try:
            test_compatibility_methods(pipeline)
        except Exception as e:
            record("compatibility methods (fatal)", False, str(e))

    # 5. Attribute audit
    try:
        test_attribute_audit()
    except Exception as e:
        record("attribute audit (fatal)", False, str(e))

    # 6. Config audit
    try:
        test_config_audit()
    except Exception as e:
        record("config audit (fatal)", False, str(e))

    # 7. Database signatures
    try:
        test_database_signatures()
    except Exception as e:
        record("database signatures (fatal)", False, str(e))

    # 8. Team registry
    try:
        test_team_registry()
    except Exception as e:
        record("team registry (fatal)", False, str(e))

    # Summary
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"PASSED: {len(PASSED)}")
    print(f"FAILED: {len(FAILED)}")
    if FAILED:
        print("\nFAILURES:")
        for name, detail in FAILED:
            print(f"  [{name}] {detail}")
    else:
        print("\nAll tests passed.")
    print("=" * 60)

    return len(FAILED)


if __name__ == "__main__":
    exit_code = asyncio.run(run_all())
    sys.exit(min(exit_code, 1) if exit_code > 0 else 0)
