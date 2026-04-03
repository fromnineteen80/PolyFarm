"""
OracleFarming Health & Status API
Exposes REST endpoints for Claude to monitor and diagnose the bot.

Runs as an async HTTP server on port 8080 alongside the bot.
"""
import asyncio
import json
import logging
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from aiohttp import web

ET = ZoneInfo("America/New_York")
logger = logging.getLogger("polyfarm.health")


class HealthServer:

    def __init__(self, port: int = 8080):
        self.port = port
        self.wallet = None
        self.pipeline = None
        self.position_monitor = None
        self.edge_detector = None
        self.markets_ws = None
        self.private_ws = None
        self._app = None
        self._runner = None
        self._start_time = datetime.now(timezone.utc)
        self._recent_decisions: list = []  # last 50 decisions
        self._recent_errors: list = []     # last 50 errors

    def log_decision(self, decision: dict):
        self._recent_decisions.append({
            **decision,
            "timestamp": datetime.now(ET).isoformat(),
        })
        if len(self._recent_decisions) > 50:
            self._recent_decisions = self._recent_decisions[-50:]

    def log_error(self, error: str):
        self._recent_errors.append({
            "error": error,
            "timestamp": datetime.now(ET).isoformat(),
        })
        if len(self._recent_errors) > 50:
            self._recent_errors = self._recent_errors[-50:]

    async def start(self):
        self._app = web.Application()
        self._app.router.add_get("/health", self._health)
        self._app.router.add_get("/status", self._status)
        self._app.router.add_get("/positions", self._positions)
        self._app.router.add_get("/decisions", self._decisions)
        self._app.router.add_get("/errors", self._errors)
        self._app.router.add_get("/games", self._games)
        self._app.router.add_get("/pipeline", self._pipeline_status)

        self._runner = web.AppRunner(self._app)
        await self._runner.setup()
        site = web.TCPSite(self._runner, "0.0.0.0", self.port)
        await site.start()
        logger.info(f"Health API running on port {self.port}")

    async def _health(self, request):
        """Simple health check — is the bot alive?"""
        uptime = (datetime.now(timezone.utc) - self._start_time).total_seconds()
        ws_markets_ok = False
        ws_private_ok = False

        if self.markets_ws and self.markets_ws._ws:
            ws_markets_ok = True
        if self.private_ws and self.private_ws._ws:
            ws_private_ok = True

        healthy = ws_markets_ok and ws_private_ok

        return web.json_response({
            "status": "healthy" if healthy else "degraded",
            "uptime_seconds": int(uptime),
            "websocket_markets": "connected" if ws_markets_ok else "disconnected",
            "websocket_private": "connected" if ws_private_ok else "disconnected",
            "errors_last_hour": len([
                e for e in self._recent_errors
                if (datetime.now(timezone.utc) - datetime.fromisoformat(
                    e["timestamp"]).replace(tzinfo=None).replace(
                    tzinfo=timezone.utc)).total_seconds() < 3600
            ]),
            "timestamp": datetime.now(ET).isoformat(),
        })

    async def _status(self, request):
        """Full status — balance, mode, positions, pipeline."""
        result = {"timestamp": datetime.now(ET).isoformat()}

        if self.wallet:
            w = self.wallet.state
            result["wallet"] = {
                "balance": round(w.live_portfolio_value, 2),
                "session_start": round(w.session_start_value, 2),
                "daily_gain_pct": round(w.daily_gain_pct * 100, 2),
                "realized_pnl": round(w.realized_pnl_today, 2),
                "floor": round(w.floor_value, 2),
                "profit_mode": w.profit_mode,
                "loss_mode": w.loss_mode,
                "session_locked": w.session_locked,
                "entries_halted": w.entries_halted,
            }

        if self.position_monitor:
            positions = self.position_monitor.get_all_positions()
            result["positions"] = {
                "count": len(positions),
                "details": [
                    {
                        "slug": slug,
                        "teams": getattr(p, "teams", ""),
                        "sport": getattr(p, "sport", ""),
                        "entry_price": getattr(p, "entry_price", 0),
                        "band": getattr(p, "band", ""),
                        "entry_time": str(getattr(p, "entry_time", "")),
                    }
                    for slug, p in positions.items()
                ],
            }

        if self.pipeline:
            result["pipeline"] = {
                "games": len(self.pipeline.games),
                "matched": len(self.pipeline.matched_games),
                "odds_events": len(self.pipeline.odds_events),
                "bridge_entries": len(self.pipeline.team_bridge),
                "leagues": len(self.pipeline.leagues),
            }

        if self.edge_detector:
            result["edge_detector"] = {
                "recently_exited": len(
                    self.edge_detector._recently_exited
                ),
                "has_odds_api": self.edge_detector.odds_api is not None,
                "has_ws_markets": self.edge_detector.ws_markets is not None,
                "has_order_manager": self.edge_detector.order_manager is not None,
            }

        return web.json_response(result)

    async def _positions(self, request):
        """Current open positions with full detail."""
        if not self.position_monitor:
            return web.json_response({"positions": []})

        positions = self.position_monitor.get_all_positions()
        details = []
        for slug, p in positions.items():
            # Get current price from wallet position values
            val = {}
            if self.wallet:
                val = self.wallet._position_values.get(slug, {})

            # Get game state from pipeline
            game = {}
            game_state = {}
            if self.pipeline:
                game = self.pipeline.games.get(slug, {})

            current_bid = val.get("current_bid", 0)
            entry = getattr(p, "entry_price", 0)
            gain = ((current_bid - entry) / entry * 100) if entry > 0 else 0

            details.append({
                "slug": slug,
                "teams": getattr(p, "teams", ""),
                "sport": getattr(p, "sport", ""),
                "band": getattr(p, "band", ""),
                "entry_price": entry,
                "current_bid": current_bid,
                "gain_pct": round(gain, 2),
                "shares": getattr(p, "shares", 0),
                "entry_time": str(getattr(p, "entry_time", "")),
                "game_score": game.get("game_score", ""),
                "game_period": game.get("game_period", ""),
                "game_elapsed": game.get("game_elapsed", ""),
                "is_live": game.get("is_live", False),
            })

        return web.json_response({"positions": details})

    async def _decisions(self, request):
        """Recent trading decisions with reasoning."""
        return web.json_response({
            "decisions": self._recent_decisions[-20:],
        })

    async def _errors(self, request):
        """Recent errors."""
        return web.json_response({
            "errors": self._recent_errors[-20:],
        })

    async def _games(self, request):
        """Live games with edge data."""
        if not self.pipeline:
            return web.json_response({"games": []})

        games = []
        for slug, game in self.pipeline.games.items():
            if not game.get("is_live"):
                continue
            edge = self.pipeline.get_edge(slug)
            games.append({
                "slug": slug,
                "home": game["home_team"],
                "away": game["away_team"],
                "league": game["league"],
                "price": game["yes_price"],
                "score": game.get("game_score", ""),
                "period": game.get("game_period", ""),
                "elapsed": game.get("game_elapsed", ""),
                "sharp_prob": edge["sharp_prob"] if edge else None,
                "edge": round(edge["edge"] * 100, 2) if edge else None,
                "matched": slug in self.pipeline.matched_games,
            })

        return web.json_response({"games": games})

    async def _pipeline_status(self, request):
        """Pipeline health and stats."""
        if not self.pipeline:
            return web.json_response({"status": "not initialized"})

        # Count by bucket
        buckets = {"live": 0, "today": 0, "upcoming": 0, "historical": 0}
        for game in self.pipeline.games.values():
            b = game.get("game_bucket", "upcoming")
            buckets[b] = buckets.get(b, 0) + 1

        return web.json_response({
            "leagues": len(self.pipeline.leagues),
            "teams": len(self.pipeline.teams),
            "games": len(self.pipeline.games),
            "matched": len(self.pipeline.matched_games),
            "odds_events": len(self.pipeline.odds_events),
            "scores": len(self.pipeline.scores),
            "buckets": buckets,
        })
