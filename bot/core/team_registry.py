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
    # NBA
    # =========================================================
    {
        "canonical": "Atlanta Hawks",
        "mascot": "Hawks",
        "city": "Atlanta",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#e21937",

        # Polymarket
        "polymarket_id": 25,
        "polymarket_abbreviation": "atl",
        "polymarket_name": "Hawks",
        "polymarket_safe_name": "Atlanta",
        "polymarket_names": ["Hawks", "Atlanta Hawks", "Atlanta", "ATL"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Atlanta Hawks",
    },
    {
        "canonical": "Boston Celtics",
        "mascot": "Celtics",
        "city": "Boston",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#009941",

        # Polymarket
        "polymarket_id": 17,
        "polymarket_abbreviation": "bos",
        "polymarket_name": "Celtics",
        "polymarket_safe_name": "Boston",
        "polymarket_names": ["Celtics", "Boston Celtics", "Boston", "BOS"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Boston Celtics",
    },
    {
        "canonical": "Brooklyn Nets",
        "mascot": "Nets",
        "city": "Brooklyn",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#334a57",

        # Polymarket
        "polymarket_id": 22,
        "polymarket_abbreviation": "bkn",
        "polymarket_name": "Nets",
        "polymarket_safe_name": "Brooklyn",
        "polymarket_names": ["Nets", "Brooklyn Nets", "Brooklyn", "BKN"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Brooklyn Nets",
    },
    {
        "canonical": "Charlotte Hornets",
        "mascot": "Hornets",
        "city": "Charlotte",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#1d98b9",

        # Polymarket
        "polymarket_id": 16,
        "polymarket_abbreviation": "cha",
        "polymarket_name": "Hornets",
        "polymarket_safe_name": "Charlotte",
        "polymarket_names": ["Hornets", "Charlotte Hornets", "Charlotte", "CHA"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Charlotte Hornets",
    },
    {
        "canonical": "Chicago Bulls",
        "mascot": "Bulls",
        "city": "Chicago",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#d5021f",

        # Polymarket
        "polymarket_id": 37,
        "polymarket_abbreviation": "chi",
        "polymarket_name": "Bulls",
        "polymarket_safe_name": "Chicago",
        "polymarket_names": ["Bulls", "Chicago Bulls", "Chicago", "CHI"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Chicago Bulls",
    },
    {
        "canonical": "Cleveland Cavaliers",
        "mascot": "Cavaliers",
        "city": "Cleveland",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#b31445",

        # Polymarket
        "polymarket_id": 38,
        "polymarket_abbreviation": "cle",
        "polymarket_name": "Cavaliers",
        "polymarket_safe_name": "Cleveland",
        "polymarket_names": ["Cavaliers", "Cleveland Cavaliers", "Cleveland", "CLE"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Cleveland Cavaliers",
    },
    {
        "canonical": "Dallas Mavericks",
        "mascot": "Mavericks",
        "city": "Dallas",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#0b6dda",

        # Polymarket
        "polymarket_id": 39,
        "polymarket_abbreviation": "dal",
        "polymarket_name": "Mavericks",
        "polymarket_safe_name": "Dallas",
        "polymarket_names": ["Mavericks", "Dallas Mavericks", "Dallas", "DAL"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Dallas Mavericks",
    },
    {
        "canonical": "Denver Nuggets",
        "mascot": "Nuggets",
        "city": "Denver",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#255fb5",

        # Polymarket
        "polymarket_id": 40,
        "polymarket_abbreviation": "den",
        "polymarket_name": "Nuggets",
        "polymarket_safe_name": "Denver",
        "polymarket_names": ["Nuggets", "Denver Nuggets", "Denver", "DEN"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Denver Nuggets",
    },
    {
        "canonical": "Detroit Pistons",
        "mascot": "Pistons",
        "city": "Detroit",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#006bcc",

        # Polymarket
        "polymarket_id": 23,
        "polymarket_abbreviation": "det",
        "polymarket_name": "Pistons",
        "polymarket_safe_name": "Detroit",
        "polymarket_names": ["Pistons", "Detroit Pistons", "Detroit", "DET"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Detroit Pistons",
    },
    {
        "canonical": "Golden State Warriors",
        "mascot": "Warriors",
        "city": "Golden State",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#dea821",

        # Polymarket
        "polymarket_id": 47,
        "polymarket_abbreviation": "gs",
        "polymarket_name": "Warriors",
        "polymarket_safe_name": "Golden State",
        "polymarket_names": ["Warriors", "Golden State Warriors", "Golden State", "GS"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Golden State Warriors",
    },
    {
        "canonical": "Houston Rockets",
        "mascot": "Rockets",
        "city": "Houston",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#d93025",

        # Polymarket
        "polymarket_id": 18,
        "polymarket_abbreviation": "hou",
        "polymarket_name": "Rockets",
        "polymarket_safe_name": "Houston",
        "polymarket_names": ["Rockets", "Houston Rockets", "Houston", "HOU"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Houston Rockets",
    },
    {
        "canonical": "Indiana Pacers",
        "mascot": "Pacers",
        "city": "Indiana",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#e4a00c",

        # Polymarket
        "polymarket_id": 19,
        "polymarket_abbreviation": "ind",
        "polymarket_name": "Pacers",
        "polymarket_safe_name": "Indiana",
        "polymarket_names": ["Pacers", "Indiana Pacers", "Indiana", "IND"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Indiana Pacers",
    },
    {
        "canonical": "Los Angeles Clippers",
        "mascot": "Clippers",
        "city": "Los Angeles",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#d90233",

        # Polymarket
        "polymarket_id": 20,
        "polymarket_abbreviation": "lac",
        "polymarket_name": "Clippers",
        "polymarket_safe_name": "Los Angeles C",
        "polymarket_names": ["Clippers", "Los Angeles Clippers", "Los Angeles C", "LAC"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Los Angeles Clippers",
    },
    {
        "canonical": "Los Angeles Lakers",
        "mascot": "Lakers",
        "city": "Los Angeles",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#862edc",

        # Polymarket
        "polymarket_id": 24,
        "polymarket_abbreviation": "lal",
        "polymarket_name": "Lakers",
        "polymarket_safe_name": "Los Angeles L",
        "polymarket_names": ["Lakers", "Los Angeles Lakers", "Los Angeles L", "LAL"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Los Angeles Lakers",
    },
    {
        "canonical": "Memphis Grizzlies",
        "mascot": "Grizzlies",
        "city": "Memphis",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#4b75af",

        # Polymarket
        "polymarket_id": 21,
        "polymarket_abbreviation": "mem",
        "polymarket_name": "Grizzlies",
        "polymarket_safe_name": "Memphis",
        "polymarket_names": ["Grizzlies", "Memphis Grizzlies", "Memphis", "MEM"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Memphis Grizzlies",
    },
    {
        "canonical": "Miami Heat",
        "mascot": "Heat",
        "city": "Miami",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#bd0038",

        # Polymarket
        "polymarket_id": 14,
        "polymarket_abbreviation": "mia",
        "polymarket_name": "Heat",
        "polymarket_safe_name": "Miami",
        "polymarket_names": ["Heat", "Miami Heat", "Miami", "MIA"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Miami Heat",
    },
    {
        "canonical": "Milwaukee Bucks",
        "mascot": "Bucks",
        "city": "Milwaukee",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#247b36",

        # Polymarket
        "polymarket_id": 41,
        "polymarket_abbreviation": "mil",
        "polymarket_name": "Bucks",
        "polymarket_safe_name": "Milwaukee",
        "polymarket_names": ["Bucks", "Milwaukee Bucks", "Milwaukee", "MIL"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Milwaukee Bucks",
    },
    {
        "canonical": "Minnesota Timberwolves",
        "mascot": "Timberwolves",
        "city": "Minnesota",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#2e7dbc",

        # Polymarket
        "polymarket_id": 15,
        "polymarket_abbreviation": "min",
        "polymarket_name": "Timberwolves",
        "polymarket_safe_name": "Minnesota",
        "polymarket_names": ["Timberwolves", "Minnesota Timberwolves", "Minnesota", "MIN"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Minnesota Timberwolves",
    },
    {
        "canonical": "New Orleans Pelicans",
        "mascot": "Pelicans",
        "city": "New Orleans",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#0f56af",

        # Polymarket
        "polymarket_id": 42,
        "polymarket_abbreviation": "no",
        "polymarket_name": "Pelicans",
        "polymarket_safe_name": "New Orleans",
        "polymarket_names": ["Pelicans", "New Orleans Pelicans", "New Orleans", "NO"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "New Orleans Pelicans",
    },
    {
        "canonical": "New York Knicks",
        "mascot": "Knicks",
        "city": "New York",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#ee760c",

        # Polymarket
        "polymarket_id": 43,
        "polymarket_abbreviation": "ny",
        "polymarket_name": "Knicks",
        "polymarket_safe_name": "New York",
        "polymarket_names": ["Knicks", "New York Knicks", "New York", "NY"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "New York Knicks",
    },
    {
        "canonical": "Oklahoma City Thunder",
        "mascot": "Thunder",
        "city": "Oklahoma City",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#007cc3",

        # Polymarket
        "polymarket_id": 27,
        "polymarket_abbreviation": "okc",
        "polymarket_name": "Thunder",
        "polymarket_safe_name": "Oklahoma City",
        "polymarket_names": ["Thunder", "Oklahoma City Thunder", "Oklahoma City", "OKC"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Oklahoma City Thunder",
    },
    {
        "canonical": "Orlando Magic",
        "mascot": "Magic",
        "city": "Orlando",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#007cc6",

        # Polymarket
        "polymarket_id": 28,
        "polymarket_abbreviation": "orl",
        "polymarket_name": "Magic",
        "polymarket_safe_name": "Orlando",
        "polymarket_names": ["Magic", "Orlando Magic", "Orlando", "ORL"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Orlando Magic",
    },
    {
        "canonical": "Philadelphia 76ers",
        "mascot": "76ers",
        "city": "Philadelphia",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#eb174c",

        # Polymarket
        "polymarket_id": 29,
        "polymarket_abbreviation": "phi",
        "polymarket_name": "76ers",
        "polymarket_safe_name": "Philadelphia",
        "polymarket_names": ["76ers", "Philadelphia 76ers", "Philadelphia", "PHI"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Philadelphia 76ers",
    },
    {
        "canonical": "Phoenix Suns",
        "mascot": "Suns",
        "city": "Phoenix",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#4c2ff0",

        # Polymarket
        "polymarket_id": 30,
        "polymarket_abbreviation": "pho",
        "polymarket_name": "Suns",
        "polymarket_safe_name": "Phoenix",
        "polymarket_names": ["Suns", "Phoenix Suns", "Phoenix", "PHO"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Phoenix Suns",
    },
    {
        "canonical": "Portland Trail Blazers",
        "mascot": "Trail Blazers",
        "city": "Portland",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#d02131",

        # Polymarket
        "polymarket_id": 31,
        "polymarket_abbreviation": "por",
        "polymarket_name": "Trail Blazers",
        "polymarket_safe_name": "Portland",
        "polymarket_names": ["Trail Blazers", "Portland Trail Blazers", "Portland", "POR"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Portland Trail Blazers",
    },
    {
        "canonical": "Sacramento Kings",
        "mascot": "Kings",
        "city": "Sacramento",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#6c318b",

        # Polymarket
        "polymarket_id": 32,
        "polymarket_abbreviation": "sac",
        "polymarket_name": "Kings",
        "polymarket_safe_name": "Sacramento",
        "polymarket_names": ["Kings", "Sacramento Kings", "Sacramento", "SAC"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Sacramento Kings",
    },
    {
        "canonical": "San Antonio Spurs",
        "mascot": "Spurs",
        "city": "San Antonio",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#8492a4",

        # Polymarket
        "polymarket_id": 33,
        "polymarket_abbreviation": "sa",
        "polymarket_name": "Spurs",
        "polymarket_safe_name": "San Antonio",
        "polymarket_names": ["Spurs", "San Antonio Spurs", "San Antonio", "SA"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "San Antonio Spurs",
    },
    {
        "canonical": "Toronto Raptors",
        "mascot": "Raptors",
        "city": "Toronto",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#dc201e",

        # Polymarket
        "polymarket_id": 34,
        "polymarket_abbreviation": "tor",
        "polymarket_name": "Raptors",
        "polymarket_safe_name": "Toronto",
        "polymarket_names": ["Raptors", "Toronto Raptors", "Toronto", "TOR"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Toronto Raptors",
    },
    {
        "canonical": "Utah Jazz",
        "mascot": "Jazz",
        "city": "Utah",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#4f0190",

        # Polymarket
        "polymarket_id": 35,
        "polymarket_abbreviation": "uta",
        "polymarket_name": "Jazz",
        "polymarket_safe_name": "Utah",
        "polymarket_names": ["Jazz", "Utah Jazz", "Utah", "UTA"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Utah Jazz",
    },
    {
        "canonical": "Washington Wizards",
        "mascot": "Wizards",
        "city": "Washington",
        "league": "nba",
        "sport": "basketball_nba",
        "color": "#e20e38",

        # Polymarket
        "polymarket_id": 36,
        "polymarket_abbreviation": "was",
        "polymarket_name": "Wizards",
        "polymarket_safe_name": "Washington",
        "polymarket_names": ["Wizards", "Washington Wizards", "Washington", "WAS"],

        # Odds API
        "odds_api_key": "basketball_nba",
        "odds_api_name": "Washington Wizards",
    },

    # =========================================================
    # NHL
    # =========================================================

    # =========================================================
    # MLB
    # =========================================================

    # =========================================================
    # NFL
    # =========================================================

    # =========================================================
    # MLS
    # =========================================================

    # =========================================================
    # EPL
    # =========================================================

    # =========================================================
    # La Liga
    # =========================================================

    # =========================================================
    # Bundesliga
    # =========================================================

    # =========================================================
    # Serie A
    # =========================================================

    # =========================================================
    # UCL
    # =========================================================

    # =========================================================
    # CBB
    # =========================================================

    # =========================================================
    # CFB
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
