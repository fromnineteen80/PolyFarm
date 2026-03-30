import os
import asyncio
import json
import logging
from datetime import datetime, timezone
from functools import partial
from supabase import create_client, Client

logger = logging.getLogger("polyfarm.database")

_supabase: Client = None
_last_write_ts: float = 0

def init_database():
    """
    Call once at startup in synchronous context
    before the asyncio event loop starts.
    """
    global _supabase
    _supabase = create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_KEY"]
    )
    logger.info("Supabase client initialized")

async def db_execute(func):
    """
    Run a synchronous Supabase call in a thread pool
    without blocking the asyncio event loop.
    Usage:
        result = await db_execute(
            lambda: _supabase.table("trades")
                .insert({...})
                .execute()
        )
    """
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, func)
    # Track last successful write (throttled to avoid recursion)
    global _last_write_ts
    import time
    now = time.time()
    if now - _last_write_ts > 30:
        _last_write_ts = now
        try:
            ts = datetime.now(timezone.utc).isoformat()
            await loop.run_in_executor(
                None,
                lambda: _supabase.table("bot_config")
                    .upsert({
                        "key": "supabase_last_write",
                        "value": ts,
                        "updated": ts
                    })
                    .execute()
            )
        except Exception:
            pass
    return result

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

# ─────────────────────────────────────────────────────
# BOT CONFIG
# ─────────────────────────────────────────────────────

async def get_bot_config(key: str):
    result = await db_execute(
        lambda: _supabase.table("bot_config")
            .select("value")
            .eq("key", key)
            .execute()
    )
    if result.data:
        return result.data[0]["value"]
    return None

async def set_bot_config(key: str, value):
    val = str(value) if value is not None else None
    return await db_execute(
        lambda: _supabase.table("bot_config")
            .upsert({
                "key": key,
                "value": val,
                "updated": _now()
            })
            .execute()
    )

async def seed_bot_config():
    """
    Seeds bot_config with defaults on first run.
    Safe to call on every startup — upsert only
    inserts if key does not exist.
    Checks existing value first to avoid overwriting.
    """
    defaults = [
        ("first_live_trade_date",   None),
        ("first_live_wallet_value", None),
        ("total_units_outstanding", "1000"),
        ("paper_trades_completed",  "0"),
        ("paper_win_rate",          "0.0"),
        ("phase2_enabled",          "false"),
        ("phase2_activation_date",  None),
        ("current_mode",            "paper"),
        ("dominant_teams_override", None),
    ]
    for key, default_value in defaults:
        existing = await get_bot_config(key)
        if existing is None:
            await set_bot_config(key, default_value)
    logger.info("bot_config seeded")

# ─────────────────────────────────────────────────────
# TRADES
# ─────────────────────────────────────────────────────

async def insert_trade(trade: dict) -> dict:
    result = await db_execute(
        lambda: _supabase.table("trades")
            .insert(trade)
            .execute()
    )
    return result.data[0] if result.data else {}

async def update_trade(trade_id: int,
                        updates: dict) -> dict:
    result = await db_execute(
        lambda: _supabase.table("trades")
            .update(updates)
            .eq("id", trade_id)
            .execute()
    )
    return result.data[0] if result.data else {}

async def get_open_trades(paper_mode: bool) -> list:
    result = await db_execute(
        lambda: _supabase.table("trades")
            .select("*")
            .is_("timestamp_exit", "null")
            .eq("paper_mode", paper_mode)
            .execute()
    )
    return result.data or []

async def get_paper_trade_stats() -> dict:
    result = await db_execute(
        lambda: _supabase.table("trades")
            .select("pnl")
            .eq("paper_mode", True)
            .not_.is_("timestamp_exit", "null")
            .execute()
    )
    trades = result.data or []
    if not trades:
        return {"count": 0, "win_rate": 0.0}
    wins = sum(1 for t in trades if t["pnl"] > 0)
    return {
        "count": len(trades),
        "win_rate": wins / len(trades)
    }

async def get_closed_trades_by_game(
    game_id: str
) -> list:
    result = await db_execute(
        lambda: _supabase.table("trades")
            .select("*")
            .eq("game_id", game_id)
            .not_.is_("timestamp_exit", "null")
            .execute()
    )
    return result.data or []

async def get_today_closed_trades(
    date_str: str, paper_mode: bool
) -> list:
    result = await db_execute(
        lambda: _supabase.table("trades")
            .select("*")
            .gte("timestamp_entry", date_str + "T00:00:00Z")
            .lte("timestamp_entry", date_str + "T23:59:59Z")
            .not_.is_("timestamp_exit", "null")
            .eq("paper_mode", paper_mode)
            .execute()
    )
    return result.data or []

# ─────────────────────────────────────────────────────
# SESSIONS
# ─────────────────────────────────────────────────────

async def insert_session(session: dict) -> dict:
    result = await db_execute(
        lambda: _supabase.table("sessions")
            .insert(session)
            .execute()
    )
    return result.data[0] if result.data else {}

async def update_session(session_id: int,
                          updates: dict) -> dict:
    result = await db_execute(
        lambda: _supabase.table("sessions")
            .update(updates)
            .eq("id", session_id)
            .execute()
    )
    return result.data[0] if result.data else {}

# ─────────────────────────────────────────────────────
# DAILY SNAPSHOTS AND STATS
# ─────────────────────────────────────────────────────

async def write_daily_snapshot(snapshot: dict):
    return await db_execute(
        lambda: _supabase.table("daily_snapshots")
            .upsert(snapshot, on_conflict="date")
            .execute()
    )

async def write_daily_stats(stats: dict):
    return await db_execute(
        lambda: _supabase.table("daily_stats")
            .upsert(stats, on_conflict="date")
            .execute()
    )

async def get_daily_snapshots(limit: int = 365):
    result = await db_execute(
        lambda: _supabase.table("daily_snapshots")
            .select("*")
            .order("date", desc=False)
            .limit(limit)
            .execute()
    )
    return result.data or []

# ─────────────────────────────────────────────────────
# MARKET MAPPINGS
# ─────────────────────────────────────────────────────

async def upsert_market_mapping(mapping: dict):
    return await db_execute(
        lambda: _supabase.table("market_mappings")
            .upsert(
                mapping,
                on_conflict="polymarket_slug"
            )
            .execute()
    )

async def get_market_mappings(
    status: str = None
) -> list:
    query = _supabase.table("market_mappings").select("*")
    if status:
        query = query.eq("mapping_status", status)
    result = await db_execute(lambda: query.execute())
    return result.data or []

# ─────────────────────────────────────────────────────
# CAPITAL EVENTS AND INVESTORS
# ─────────────────────────────────────────────────────

async def insert_capital_event(event: dict) -> dict:
    result = await db_execute(
        lambda: _supabase.table("capital_events")
            .insert(event)
            .execute()
    )
    return result.data[0] if result.data else {}

async def get_investors() -> list:
    result = await db_execute(
        lambda: _supabase.table("investors")
            .select("*")
            .eq("is_active", True)
            .execute()
    )
    return result.data or []

async def upsert_investor(investor: dict) -> dict:
    result = await db_execute(
        lambda: _supabase.table("investors")
            .upsert(investor)
            .execute()
    )
    return result.data[0] if result.data else {}

# ─────────────────────────────────────────────────────
# INCENTIVE LOG
# ─────────────────────────────────────────────────────

async def log_incentive(entry: dict):
    return await db_execute(
        lambda: _supabase.table("incentive_log")
            .insert(entry)
            .execute()
    )

# ─────────────────────────────────────────────────────
# SYSTEM EVENTS
# ─────────────────────────────────────────────────────

async def log_system_event(
    event_type: str,
    description: str,
    metadata: dict = None
):
    return await db_execute(
        lambda: _supabase.table("system_events")
            .insert({
                "timestamp": _now(),
                "event_type": event_type,
                "description": description,
                "metadata": json.dumps(metadata or {})
            })
            .execute()
    )

# ─────────────────────────────────────────────────────
# RESEARCH SIGNALS
# ─────────────────────────────────────────────────────

async def insert_research_signal(signal: dict) -> dict:
    result = await db_execute(
        lambda: _supabase.table("research_signals")
            .insert(signal)
            .execute()
    )
    return result.data[0] if result.data else {}

# ─────────────────────────────────────────────────────
# ODDSPAPI TABLES
# ─────────────────────────────────────────────────────

async def upsert_pinnacle_odds(data: dict):
    return await db_execute(
        lambda: _supabase.table("pinnacle_odds")
            .upsert(data, on_conflict="oddspapi_fixture_id")
            .execute()
    )

async def update_pinnacle_odds_slug(fixture_id: str, polymarket_slug: str):
    return await db_execute(
        lambda: _supabase.table("pinnacle_odds")
            .update({"polymarket_slug": polymarket_slug})
            .eq("oddspapi_fixture_id", fixture_id)
            .execute()
    )

async def upsert_fixture_mapping(data: dict):
    return await db_execute(
        lambda: _supabase.table("oddspapi_fixture_mappings")
            .upsert(data, on_conflict="polymarket_slug")
            .execute()
    )

async def upsert_tournament(data: dict):
    return await db_execute(
        lambda: _supabase.table("oddspapi_tournaments")
            .upsert(data, on_conflict="tournament_id")
            .execute()
    )

async def upsert_participant(data: dict):
    return await db_execute(
        lambda: _supabase.table("oddspapi_participants")
            .upsert(data, on_conflict="sport_id,participant_id")
            .execute()
    )
