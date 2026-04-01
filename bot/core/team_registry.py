"""
OracleFarming Master Team Registry.

Every team across every league we trade, with every
name variation and both API identifiers.

The pipeline uses this as the single source of truth.
No fuzzy matching. No guessing. If a team isn't in
this registry, it doesn't get matched.
"""

# ── Approved structure per team ──────────────────────
#
# {
#     "canonical": "Juventus",
#     "mascot": "Juventus",
#     "city": "Turin",
#     "league": "sea",
#     "sport": "soccer_italy_serie_a",
#     "color": "#000000",
#
#     # Polymarket
#     "polymarket_id": 3421,
#     "polymarket_abbreviation": "juv",
#     "polymarket_name": "Juventus FC",
#     "polymarket_safe_name": "Juventus",
#     "polymarket_names": ["Juventus FC", "Juventus", "JUV"],
#
#     # Odds API
#     "odds_api_key": "soccer_italy_serie_a",
#     "odds_api_name": "Juventus",
# }

TEAM_REGISTRY = [
    # =========================================================
    # NBA (30 teams)
    # =========================================================

    # =========================================================
    # NHL (32 teams)
    # =========================================================

    # =========================================================
    # MLB (30 teams)
    # =========================================================

    # =========================================================
    # MLS (30 teams)
    # =========================================================

    # =========================================================
    # EPL (20 teams)
    # =========================================================

    # =========================================================
    # La Liga (20 teams)
    # =========================================================

    # =========================================================
    # Bundesliga (18 teams)
    # =========================================================

    # =========================================================
    # Serie A (20 teams)
    # =========================================================
]


# ── Lookup indexes ────────────────────────────────────

_BY_POLY_ID = {}     # polymarket_id -> registry entry
_BY_POLY_NAME = {}   # (league, normalized_name) -> registry entry
_BY_ODDS_NAME = {}   # (league, normalized_name) -> registry entry
_BUILT = False


def _normalize(name: str) -> str:
    """Normalize team name for comparison."""
    if not name:
        return ""
    import unicodedata
    import re
    n = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    n = n.lower().strip()
    n = re.sub(r"[^\w\s]", "", n)
    n = re.sub(r"\b(fc|sc|cf|afc|the)\s*$", "", n)
    n = re.sub(r"^the\s+", "", n)
    return n.strip()


def _build_indexes():
    global _BUILT
    for team in TEAM_REGISTRY:
        pid = team.get("polymarket_id", 0)
        if pid and pid > 0:
            _BY_POLY_ID[pid] = team
        league = team["league"]
        for pname in team.get("polymarket_names", []):
            _BY_POLY_NAME[(league, _normalize(pname))] = team
        odds_name = team.get("odds_api_name", "")
        if odds_name:
            _BY_ODDS_NAME[(league, _normalize(odds_name))] = team
    _BUILT = True


def _ensure():
    if not _BUILT:
        _build_indexes()


def lookup_by_polymarket_id(poly_id: int):
    """Primary lookup: by Polymarket team ID (unique, never ambiguous)."""
    _ensure()
    return _BY_POLY_ID.get(poly_id)


def lookup_by_polymarket_name(name: str, league: str):
    """Fallback lookup: by name within league scope."""
    _ensure()
    return _BY_POLY_NAME.get((league, _normalize(name)))


def lookup_by_odds_api_name(name: str, league: str):
    """Lookup Odds API team by name within league scope."""
    _ensure()
    return _BY_ODDS_NAME.get((league, _normalize(name)))


def get_teams_by_league(league: str) -> list:
    """Get all teams for a given league slug."""
    return [t for t in TEAM_REGISTRY if t["league"] == league]
