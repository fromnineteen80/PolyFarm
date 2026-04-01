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
    {
        "canonical": "Anaheim Ducks",
        "mascot": "Ducks",
        "city": "Anaheim",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#e73708",

        # Polymarket
        "polymarket_id": 1512,
        "polymarket_abbreviation": "ana",
        "polymarket_name": "Ducks",
        "polymarket_safe_name": "ANA Ducks",
        "polymarket_names": ["Ducks", "Anaheim Ducks", "ANA Ducks", "ANA"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Anaheim Ducks",
    },
    {
        "canonical": "Boston Bruins",
        "mascot": "Bruins",
        "city": "Boston",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#e99802",

        # Polymarket
        "polymarket_id": 1484,
        "polymarket_abbreviation": "bos",
        "polymarket_name": "Bruins",
        "polymarket_safe_name": "BOS Bruins",
        "polymarket_names": ["Bruins", "Boston Bruins", "BOS Bruins", "BOS"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Boston Bruins",
    },
    {
        "canonical": "Buffalo Sabres",
        "mascot": "Sabres",
        "city": "Buffalo",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#0257bb",

        # Polymarket
        "polymarket_id": 1485,
        "polymarket_abbreviation": "buf",
        "polymarket_name": "Sabres",
        "polymarket_safe_name": "BUF Sabres",
        "polymarket_names": ["Sabres", "Buffalo Sabres", "BUF Sabres", "BUF"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Buffalo Sabres",
    },
    {
        "canonical": "Calgary Flames",
        "mascot": "Flames",
        "city": "Calgary",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#c8102e",

        # Polymarket
        "polymarket_id": 1507,
        "polymarket_abbreviation": "cgy",
        "polymarket_name": "Flames",
        "polymarket_safe_name": "CGY Flames",
        "polymarket_names": ["Flames", "Calgary Flames", "CGY Flames", "CGY"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Calgary Flames",
    },
    {
        "canonical": "Carolina Hurricanes",
        "mascot": "Hurricanes",
        "city": "Carolina",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#ed2e32",

        # Polymarket
        "polymarket_id": 1492,
        "polymarket_abbreviation": "car",
        "polymarket_name": "Hurricanes",
        "polymarket_safe_name": "CAR Hurricanes",
        "polymarket_names": ["Hurricanes", "Carolina Hurricanes", "CAR Hurricanes", "CAR"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Carolina Hurricanes",
    },
    {
        "canonical": "Chicago Blackhawks",
        "mascot": "Blackhawks",
        "city": "Chicago",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#d3020e",

        # Polymarket
        "polymarket_id": 1500,
        "polymarket_abbreviation": "chi",
        "polymarket_name": "Blackhawks",
        "polymarket_safe_name": "CHI Blackhawks",
        "polymarket_names": ["Blackhawks", "Chicago Blackhawks", "CHI Blackhawks", "CHI"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Chicago Blackhawks",
    },
    {
        "canonical": "Colorado Avalanche",
        "mascot": "Avalanche",
        "city": "Colorado",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#ca164e",

        # Polymarket
        "polymarket_id": 1502,
        "polymarket_abbreviation": "col",
        "polymarket_name": "Avalanche",
        "polymarket_safe_name": "COL Avalanche",
        "polymarket_names": ["Avalanche", "Colorado Avalanche", "COL Avalanche", "COL"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Colorado Avalanche",
    },
    {
        "canonical": "Columbus Blue Jackets",
        "mascot": "Blue Jackets",
        "city": "Columbus",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#0258ca",

        # Polymarket
        "polymarket_id": 1499,
        "polymarket_abbreviation": "cbj",
        "polymarket_name": "Blue Jackets",
        "polymarket_safe_name": "CBJ Blue Jackets",
        "polymarket_names": ["Blue Jackets", "Columbus Blue Jackets", "CBJ Blue Jackets", "CBJ"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Columbus Blue Jackets",
    },
    {
        "canonical": "Dallas Stars",
        "mascot": "Stars",
        "city": "Dallas",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#00843d",

        # Polymarket
        "polymarket_id": 1501,
        "polymarket_abbreviation": "dal",
        "polymarket_name": "Stars",
        "polymarket_safe_name": "DAL Stars",
        "polymarket_names": ["Stars", "Dallas Stars", "DAL Stars", "DAL"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Dallas Stars",
    },
    {
        "canonical": "Detroit Red Wings",
        "mascot": "Red Wings",
        "city": "Detroit",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#ec1f26",

        # Polymarket
        "polymarket_id": 1486,
        "polymarket_abbreviation": "det",
        "polymarket_name": "Red Wings",
        "polymarket_safe_name": "DET Red Wings",
        "polymarket_names": ["Red Wings", "Detroit Red Wings", "DET Red Wings", "DET"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Detroit Red Wings",
    },
    {
        "canonical": "Edmonton Oilers",
        "mascot": "Oilers",
        "city": "Edmonton",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#005ecc",

        # Polymarket
        "polymarket_id": 1508,
        "polymarket_abbreviation": "edm",
        "polymarket_name": "Oilers",
        "polymarket_safe_name": "EDM Oilers",
        "polymarket_names": ["Oilers", "Edmonton Oilers", "EDM Oilers", "EDM"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Edmonton Oilers",
    },
    {
        "canonical": "Florida Panthers",
        "mascot": "Panthers",
        "city": "Florida",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#ec0727",

        # Polymarket
        "polymarket_id": 1491,
        "polymarket_abbreviation": "fla",
        "polymarket_name": "Panthers",
        "polymarket_safe_name": "FLA Panthers",
        "polymarket_names": ["Panthers", "Florida Panthers", "FLA Panthers", "FLA"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Florida Panthers",
    },
    {
        "canonical": "Los Angeles Kings",
        "mascot": "Kings",
        "city": "Los Angeles",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#737e82",

        # Polymarket
        "polymarket_id": 1509,
        "polymarket_abbreviation": "la",
        "polymarket_name": "Kings",
        "polymarket_safe_name": "LA Kings",
        "polymarket_names": ["Kings", "Los Angeles Kings", "LA Kings", "LA"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Los Angeles Kings",
    },
    {
        "canonical": "Minnesota Wild",
        "mascot": "Wild",
        "city": "Minnesota",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#008a54",

        # Polymarket
        "polymarket_id": 1506,
        "polymarket_abbreviation": "min",
        "polymarket_name": "Wild",
        "polymarket_safe_name": "MIN Wild",
        "polymarket_names": ["Wild", "Minnesota Wild", "MIN Wild", "MIN"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Minnesota Wild",
    },
    {
        "canonical": "Montreal Canadiens",
        "mascot": "Canadiens",
        "city": "Montreal",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#d71823",

        # Polymarket
        "polymarket_id": 1487,
        "polymarket_abbreviation": "mon",
        "polymarket_name": "Canadiens",
        "polymarket_safe_name": "MON Canadiens",
        "polymarket_names": ["Canadiens", "Montreal Canadiens", "MON Canadiens", "MON"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Montréal Canadiens",
    },
    {
        "canonical": "Nashville Predators",
        "mascot": "Predators",
        "city": "Nashville",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#E5A800",

        # Polymarket
        "polymarket_id": 1504,
        "polymarket_abbreviation": "nas",
        "polymarket_name": "Predators",
        "polymarket_safe_name": "NAS Predators",
        "polymarket_names": ["Predators", "Nashville Predators", "NAS Predators", "NAS"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Nashville Predators",
    },
    {
        "canonical": "New Jersey Devils",
        "mascot": "Devils",
        "city": "New Jersey",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#f4272b",

        # Polymarket
        "polymarket_id": 1493,
        "polymarket_abbreviation": "nj",
        "polymarket_name": "Devils",
        "polymarket_safe_name": "NJ Devils",
        "polymarket_names": ["Devils", "New Jersey Devils", "NJ Devils", "NJ"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "New Jersey Devils",
    },
    {
        "canonical": "New York Islanders",
        "mascot": "Islanders",
        "city": "New York",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#fa661c",

        # Polymarket
        "polymarket_id": 1494,
        "polymarket_abbreviation": "nyi",
        "polymarket_name": "Islanders",
        "polymarket_safe_name": "NYI Islanders",
        "polymarket_names": ["Islanders", "New York Islanders", "NYI Islanders", "NYI"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "New York Islanders",
    },
    {
        "canonical": "New York Rangers",
        "mascot": "Rangers",
        "city": "New York",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#0071d6",

        # Polymarket
        "polymarket_id": 1495,
        "polymarket_abbreviation": "nyr",
        "polymarket_name": "Rangers",
        "polymarket_safe_name": "NYR Rangers",
        "polymarket_names": ["Rangers", "New York Rangers", "NYR Rangers", "NYR"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "New York Rangers",
    },
    {
        "canonical": "Ottawa Senators",
        "mascot": "Senators",
        "city": "Ottawa",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#e5172f",

        # Polymarket
        "polymarket_id": 1488,
        "polymarket_abbreviation": "ott",
        "polymarket_name": "Senators",
        "polymarket_safe_name": "OTT Senators",
        "polymarket_names": ["Senators", "Ottawa Senators", "OTT Senators", "OTT"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Ottawa Senators",
    },
    {
        "canonical": "Philadelphia Flyers",
        "mascot": "Flyers",
        "city": "Philadelphia",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#fa6115",

        # Polymarket
        "polymarket_id": 1496,
        "polymarket_abbreviation": "phi",
        "polymarket_name": "Flyers",
        "polymarket_safe_name": "PHI Flyers",
        "polymarket_names": ["Flyers", "Philadelphia Flyers", "PHI Flyers", "PHI"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Philadelphia Flyers",
    },
    {
        "canonical": "Pittsburgh Penguins",
        "mascot": "Penguins",
        "city": "Pittsburgh",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#e5ad2f",

        # Polymarket
        "polymarket_id": 1497,
        "polymarket_abbreviation": "pit",
        "polymarket_name": "Penguins",
        "polymarket_safe_name": "PIT Penguins",
        "polymarket_names": ["Penguins", "Pittsburgh Penguins", "PIT Penguins", "PIT"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Pittsburgh Penguins",
    },
    {
        "canonical": "San Jose Sharks",
        "mascot": "Sharks",
        "city": "San Jose",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#00778b",

        # Polymarket
        "polymarket_id": 1510,
        "polymarket_abbreviation": "sj",
        "polymarket_name": "Sharks",
        "polymarket_safe_name": "SJ Sharks",
        "polymarket_names": ["Sharks", "San Jose Sharks", "SJ Sharks", "SJ"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "San Jose Sharks",
    },
    {
        "canonical": "Seattle Kraken",
        "mascot": "Kraken",
        "city": "Seattle",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#3d94b3",

        # Polymarket
        "polymarket_id": 1514,
        "polymarket_abbreviation": "sea",
        "polymarket_name": "Kraken",
        "polymarket_safe_name": "SEA Kraken",
        "polymarket_names": ["Kraken", "Seattle Kraken", "SEA Kraken", "SEA"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Seattle Kraken",
    },
    {
        "canonical": "St. Louis Blues",
        "mascot": "Blues",
        "city": "St. Louis",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#006ac6",

        # Polymarket
        "polymarket_id": 1503,
        "polymarket_abbreviation": "stl",
        "polymarket_name": "Blues",
        "polymarket_safe_name": "STL Blues",
        "polymarket_names": ["Blues", "St. Louis Blues", "STL Blues", "STL"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "St Louis Blues",
    },
    {
        "canonical": "Tampa Bay Lightning",
        "mascot": "Lightning",
        "city": "Tampa Bay",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#2429f4",

        # Polymarket
        "polymarket_id": 1489,
        "polymarket_abbreviation": "tb",
        "polymarket_name": "Lightning",
        "polymarket_safe_name": "TB Lightning",
        "polymarket_names": ["Lightning", "Tampa Bay Lightning", "TB Lightning", "TB"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Tampa Bay Lightning",
    },
    {
        "canonical": "Toronto Maple Leafs",
        "mascot": "Maple Leafs",
        "city": "Toronto",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#383cf5",

        # Polymarket
        "polymarket_id": 1490,
        "polymarket_abbreviation": "tor",
        "polymarket_name": "Maple Leafs",
        "polymarket_safe_name": "TOR Maple Leafs",
        "polymarket_names": ["Maple Leafs", "Toronto Maple Leafs", "TOR Maple Leafs", "TOR"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Toronto Maple Leafs",
    },
    {
        "canonical": "Utah Mammoth",
        "mascot": "Mammoth",
        "city": "Utah",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#3695e7",

        # Polymarket
        "polymarket_id": 1515,
        "polymarket_abbreviation": "uta",
        "polymarket_name": "Mammoth",
        "polymarket_safe_name": "UTA Mammoth",
        "polymarket_names": ["Mammoth", "Utah Mammoth", "UTA Mammoth", "UTA"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Utah Mammoth",
    },
    {
        "canonical": "Vancouver Canucks",
        "mascot": "Canucks",
        "city": "Vancouver",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#0e63d8",

        # Polymarket
        "polymarket_id": 1511,
        "polymarket_abbreviation": "van",
        "polymarket_name": "Canucks",
        "polymarket_safe_name": "VAN Canucks",
        "polymarket_names": ["Canucks", "Vancouver Canucks", "VAN Canucks", "VAN"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Vancouver Canucks",
    },
    {
        "canonical": "Vegas Golden Knights",
        "mascot": "Golden Knights",
        "city": "Vegas",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#b9975b",

        # Polymarket
        "polymarket_id": 1513,
        "polymarket_abbreviation": "veg",
        "polymarket_name": "Golden Knights",
        "polymarket_safe_name": "VEG Golden Knights",
        "polymarket_names": ["Golden Knights", "Vegas Golden Knights", "VEG Golden Knights", "VEG"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Vegas Golden Knights",
    },
    {
        "canonical": "Washington Capitals",
        "mascot": "Capitals",
        "city": "Washington",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#cf142b",

        # Polymarket
        "polymarket_id": 1498,
        "polymarket_abbreviation": "was",
        "polymarket_name": "Capitals",
        "polymarket_safe_name": "WAS Capitals",
        "polymarket_names": ["Capitals", "Washington Capitals", "WAS Capitals", "WAS"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Washington Capitals",
    },
    {
        "canonical": "Winnipeg Jets",
        "mascot": "Jets",
        "city": "Winnipeg",
        "league": "nhl",
        "sport": "icehockey_nhl",
        "color": "#067aee",

        # Polymarket
        "polymarket_id": 1505,
        "polymarket_abbreviation": "wpg",
        "polymarket_name": "Jets",
        "polymarket_safe_name": "WPG Jets",
        "polymarket_names": ["Jets", "Winnipeg Jets", "WPG Jets", "WPG"],

        # Odds API
        "odds_api_key": "icehockey_nhl",
        "odds_api_name": "Winnipeg Jets",
    },

    # =========================================================
    # MLB
    # =========================================================

    {
        "canonical": "Arizona Diamondbacks",
        "mascot": "Diamondbacks",
        "city": "Arizona",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#A71930",

        # Polymarket
        "polymarket_id": 3002,
        "polymarket_abbreviation": "az",
        "polymarket_name": "Arizona Diamondbacks",
        "polymarket_safe_name": "Arizona Diamondbacks",
        "polymarket_names": ["Arizona Diamondbacks", "AZ"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Arizona Diamondbacks",
    },
    {
        "canonical": "Athletics",
        "mascot": "Athletics",
        "city": "Sacramento",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#208273",

        # Polymarket
        "polymarket_id": 3000,
        "polymarket_abbreviation": "ath",
        "polymarket_name": "Athletics",
        "polymarket_safe_name": "Athletics",
        "polymarket_names": ["Athletics", "ATH"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Athletics",
    },
    {
        "canonical": "Atlanta Braves",
        "mascot": "Braves",
        "city": "Atlanta",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#CE1141",

        # Polymarket
        "polymarket_id": 3001,
        "polymarket_abbreviation": "atl",
        "polymarket_name": "Atlanta Braves",
        "polymarket_safe_name": "Atlanta Braves",
        "polymarket_names": ["Atlanta Braves", "ATL"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Atlanta Braves",
    },
    {
        "canonical": "Baltimore Orioles",
        "mascot": "Orioles",
        "city": "Baltimore",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#D94000",

        # Polymarket
        "polymarket_id": 3003,
        "polymarket_abbreviation": "bal",
        "polymarket_name": "Baltimore Orioles",
        "polymarket_safe_name": "Baltimore Orioles",
        "polymarket_names": ["Baltimore Orioles", "BAL"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Baltimore Orioles",
    },
    {
        "canonical": "Boston Red Sox",
        "mascot": "Red Sox",
        "city": "Boston",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#BD3039",

        # Polymarket
        "polymarket_id": 3004,
        "polymarket_abbreviation": "bos",
        "polymarket_name": "Boston Red Sox",
        "polymarket_safe_name": "Boston Red Sox",
        "polymarket_names": ["Boston Red Sox", "BOS"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Boston Red Sox",
    },
    {
        "canonical": "Chicago Cubs",
        "mascot": "Cubs",
        "city": "Chicago",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#CC3433",

        # Polymarket
        "polymarket_id": 3005,
        "polymarket_abbreviation": "chc",
        "polymarket_name": "Chicago Cubs",
        "polymarket_safe_name": "Chicago Cubs",
        "polymarket_names": ["Chicago Cubs", "CHC"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Chicago Cubs",
    },
    {
        "canonical": "Chicago White Sox",
        "mascot": "White Sox",
        "city": "Chicago",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#868FA8",

        # Polymarket
        "polymarket_id": 3009,
        "polymarket_abbreviation": "cws",
        "polymarket_name": "Chicago White Sox",
        "polymarket_safe_name": "Chicago White Sox",
        "polymarket_names": ["Chicago White Sox", "CWS"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Chicago White Sox",
    },
    {
        "canonical": "Cincinnati Reds",
        "mascot": "Reds",
        "city": "Cincinnati",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#C6011F",

        # Polymarket
        "polymarket_id": 3006,
        "polymarket_abbreviation": "cin",
        "polymarket_name": "Cincinnati Reds",
        "polymarket_safe_name": "Cincinnati Reds",
        "polymarket_names": ["Cincinnati Reds", "CIN"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Cincinnati Reds",
    },
    {
        "canonical": "Cleveland Guardians",
        "mascot": "Guardians",
        "city": "Cleveland",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#F60017",

        # Polymarket
        "polymarket_id": 3007,
        "polymarket_abbreviation": "cle",
        "polymarket_name": "Cleveland Guardians",
        "polymarket_safe_name": "Cleveland Guardians",
        "polymarket_names": ["Cleveland Guardians", "CLE"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Cleveland Guardians",
    },
    {
        "canonical": "Colorado Rockies",
        "mascot": "Rockies",
        "city": "Colorado",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#333366",

        # Polymarket
        "polymarket_id": 3008,
        "polymarket_abbreviation": "col",
        "polymarket_name": "Colorado Rockies",
        "polymarket_safe_name": "Colorado Rockies",
        "polymarket_names": ["Colorado Rockies", "COL"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Colorado Rockies",
    },
    {
        "canonical": "Detroit Tigers",
        "mascot": "Tigers",
        "city": "Detroit",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#0C2C56",

        # Polymarket
        "polymarket_id": 3010,
        "polymarket_abbreviation": "det",
        "polymarket_name": "Detroit Tigers",
        "polymarket_safe_name": "Detroit Tigers",
        "polymarket_names": ["Detroit Tigers", "DET"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Detroit Tigers",
    },
    {
        "canonical": "Houston Astros",
        "mascot": "Astros",
        "city": "Houston",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#1D5AA1",

        # Polymarket
        "polymarket_id": 3011,
        "polymarket_abbreviation": "hou",
        "polymarket_name": "Houston Astros",
        "polymarket_safe_name": "Houston Astros",
        "polymarket_names": ["Houston Astros", "HOU"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Houston Astros",
    },
    {
        "canonical": "Kansas City Royals",
        "mascot": "Royals",
        "city": "Kansas City",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#004687",

        # Polymarket
        "polymarket_id": 3012,
        "polymarket_abbreviation": "kc",
        "polymarket_name": "Kansas City Royals",
        "polymarket_safe_name": "Kansas City Royals",
        "polymarket_names": ["Kansas City Royals", "KC"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Kansas City Royals",
    },
    {
        "canonical": "Los Angeles Angels",
        "mascot": "Angels",
        "city": "Los Angeles",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#BA0021",

        # Polymarket
        "polymarket_id": 3013,
        "polymarket_abbreviation": "laa",
        "polymarket_name": "Los Angeles Angels",
        "polymarket_safe_name": "Los Angeles Angels",
        "polymarket_names": ["Los Angeles Angels", "LAA"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Los Angeles Angels",
    },
    {
        "canonical": "Los Angeles Dodgers",
        "mascot": "Dodgers",
        "city": "Los Angeles",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#005A9C",

        # Polymarket
        "polymarket_id": 3014,
        "polymarket_abbreviation": "lad",
        "polymarket_name": "Los Angeles Dodgers",
        "polymarket_safe_name": "Los Angeles Dodgers",
        "polymarket_names": ["Los Angeles Dodgers", "LAD"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Los Angeles Dodgers",
    },
    {
        "canonical": "Miami Marlins",
        "mascot": "Marlins",
        "city": "Miami",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#FF6600",

        # Polymarket
        "polymarket_id": 3015,
        "polymarket_abbreviation": "mia",
        "polymarket_name": "Miami Marlins",
        "polymarket_safe_name": "Miami Marlins",
        "polymarket_names": ["Miami Marlins", "MIA"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Miami Marlins",
    },
    {
        "canonical": "Milwaukee Brewers",
        "mascot": "Brewers",
        "city": "Milwaukee",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#BD9000",

        # Polymarket
        "polymarket_id": 3016,
        "polymarket_abbreviation": "mil",
        "polymarket_name": "Milwaukee Brewers",
        "polymarket_safe_name": "Milwaukee Brewers",
        "polymarket_names": ["Milwaukee Brewers", "MIL"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Milwaukee Brewers",
    },
    {
        "canonical": "Minnesota Twins",
        "mascot": "Twins",
        "city": "Minnesota",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#29568A",

        # Polymarket
        "polymarket_id": 3017,
        "polymarket_abbreviation": "min",
        "polymarket_name": "Minnesota Twins",
        "polymarket_safe_name": "Minnesota Twins",
        "polymarket_names": ["Minnesota Twins", "MIN"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Minnesota Twins",
    },
    {
        "canonical": "New York Mets",
        "mascot": "Mets",
        "city": "New York",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#FF5910",

        # Polymarket
        "polymarket_id": 3018,
        "polymarket_abbreviation": "nym",
        "polymarket_name": "New York Mets",
        "polymarket_safe_name": "New York Mets",
        "polymarket_names": ["New York Mets", "NYM"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "New York Mets",
    },
    {
        "canonical": "New York Yankees",
        "mascot": "Yankees",
        "city": "New York",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#29568A",

        # Polymarket
        "polymarket_id": 3019,
        "polymarket_abbreviation": "nyy",
        "polymarket_name": "New York Yankees",
        "polymarket_safe_name": "New York Yankees",
        "polymarket_names": ["New York Yankees", "NYY"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "New York Yankees",
    },
    {
        "canonical": "Philadelphia Phillies",
        "mascot": "Phillies",
        "city": "Philadelphia",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#284898",

        # Polymarket
        "polymarket_id": 3020,
        "polymarket_abbreviation": "phi",
        "polymarket_name": "Philadelphia Phillies",
        "polymarket_safe_name": "Philadelphia Phillies",
        "polymarket_names": ["Philadelphia Phillies", "PHI"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Philadelphia Phillies",
    },
    {
        "canonical": "Pittsburgh Pirates",
        "mascot": "Pirates",
        "city": "Pittsburgh",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#FDB827",

        # Polymarket
        "polymarket_id": 3021,
        "polymarket_abbreviation": "pit",
        "polymarket_name": "Pittsburgh Pirates",
        "polymarket_safe_name": "Pittsburgh Pirates",
        "polymarket_names": ["Pittsburgh Pirates", "PIT"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Pittsburgh Pirates",
    },
    {
        "canonical": "San Diego Padres",
        "mascot": "Padres",
        "city": "San Diego",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#F5AF05",

        # Polymarket
        "polymarket_id": 3022,
        "polymarket_abbreviation": "sd",
        "polymarket_name": "San Diego Padres",
        "polymarket_safe_name": "San Diego Padres",
        "polymarket_names": ["San Diego Padres", "SD"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "San Diego Padres",
    },
    {
        "canonical": "San Francisco Giants",
        "mascot": "Giants",
        "city": "San Francisco",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#FD5A1E",

        # Polymarket
        "polymarket_id": 3024,
        "polymarket_abbreviation": "sf",
        "polymarket_name": "San Francisco Giants",
        "polymarket_safe_name": "San Francisco Giants",
        "polymarket_names": ["San Francisco Giants", "SF"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "San Francisco Giants",
    },
    {
        "canonical": "Seattle Mariners",
        "mascot": "Mariners",
        "city": "Seattle",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#2D5D9D",

        # Polymarket
        "polymarket_id": 3023,
        "polymarket_abbreviation": "sea",
        "polymarket_name": "Seattle Mariners",
        "polymarket_safe_name": "Seattle Mariners",
        "polymarket_names": ["Seattle Mariners", "SEA"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Seattle Mariners",
    },
    {
        "canonical": "St. Louis Cardinals",
        "mascot": "Cardinals",
        "city": "St. Louis",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#C41E3A",

        # Polymarket
        "polymarket_id": 3025,
        "polymarket_abbreviation": "stl",
        "polymarket_name": "St. Louis Cardinals",
        "polymarket_safe_name": "St. Louis Cardinals",
        "polymarket_names": ["St. Louis Cardinals", "STL"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "St. Louis Cardinals",
    },
    {
        "canonical": "Tampa Bay Rays",
        "mascot": "Rays",
        "city": "Tampa Bay",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#8FBCE6",

        # Polymarket
        "polymarket_id": 3026,
        "polymarket_abbreviation": "tb",
        "polymarket_name": "Tampa Bay Rays",
        "polymarket_safe_name": "Tampa Bay Rays",
        "polymarket_names": ["Tampa Bay Rays", "TB"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Tampa Bay Rays",
    },
    {
        "canonical": "Texas Rangers",
        "mascot": "Rangers",
        "city": "Texas",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#C0111F",

        # Polymarket
        "polymarket_id": 3027,
        "polymarket_abbreviation": "tex",
        "polymarket_name": "Texas Rangers",
        "polymarket_safe_name": "Texas Rangers",
        "polymarket_names": ["Texas Rangers", "TEX"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Texas Rangers",
    },
    {
        "canonical": "Toronto Blue Jays",
        "mascot": "Blue Jays",
        "city": "Toronto",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#134A8E",

        # Polymarket
        "polymarket_id": 3028,
        "polymarket_abbreviation": "tor",
        "polymarket_name": "Toronto Blue Jays",
        "polymarket_safe_name": "Toronto Blue Jays",
        "polymarket_names": ["Toronto Blue Jays", "TOR"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Toronto Blue Jays",
    },
    {
        "canonical": "Washington Nationals",
        "mascot": "Nationals",
        "city": "Washington",
        "league": "mlb",
        "sport": "baseball_mlb",
        "color": "#AB0003",

        # Polymarket
        "polymarket_id": 3029,
        "polymarket_abbreviation": "wsh",
        "polymarket_name": "Washington Nationals",
        "polymarket_safe_name": "Washington Nationals",
        "polymarket_names": ["Washington Nationals", "WSH"],

        # Odds API
        "odds_api_key": "baseball_mlb",
        "odds_api_name": "Washington Nationals",
    },

    # =========================================================
    # NFL
    # =========================================================

    {
        "canonical": "Arizona Cardinals",
        "mascot": "Cardinals",
        "city": "Arizona",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#a12d48",

        # Polymarket
        "polymarket_id": 48,
        "polymarket_abbreviation": "ari",
        "polymarket_name": "Arizona Cardinals",
        "polymarket_safe_name": "Arizona",
        "polymarket_names": ["Arizona Cardinals", "Arizona", "ARI"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Arizona Cardinals",
    },
    {
        "canonical": "Atlanta Falcons",
        "mascot": "Falcons",
        "city": "Atlanta",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#b31f37",

        # Polymarket
        "polymarket_id": 49,
        "polymarket_abbreviation": "atl",
        "polymarket_name": "Atlanta Falcons",
        "polymarket_safe_name": "Atlanta",
        "polymarket_names": ["Atlanta Falcons", "Atlanta", "ATL"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Atlanta Falcons",
    },
    {
        "canonical": "Baltimore Ravens",
        "mascot": "Ravens",
        "city": "Baltimore",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#5340bb",

        # Polymarket
        "polymarket_id": 50,
        "polymarket_abbreviation": "bal",
        "polymarket_name": "Baltimore Ravens",
        "polymarket_safe_name": "Baltimore",
        "polymarket_names": ["Baltimore Ravens", "Baltimore", "BAL"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Baltimore Ravens",
    },
    {
        "canonical": "Buffalo Bills",
        "mascot": "Bills",
        "city": "Buffalo",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#1e57cc",

        # Polymarket
        "polymarket_id": 51,
        "polymarket_abbreviation": "buf",
        "polymarket_name": "Buffalo Bills",
        "polymarket_safe_name": "Buffalo",
        "polymarket_names": ["Buffalo Bills", "Buffalo", "BUF"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Buffalo Bills",
    },
    {
        "canonical": "Carolina Panthers",
        "mascot": "Panthers",
        "city": "Carolina",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#0994d6",

        # Polymarket
        "polymarket_id": 52,
        "polymarket_abbreviation": "car",
        "polymarket_name": "Carolina Panthers",
        "polymarket_safe_name": "Carolina",
        "polymarket_names": ["Carolina Panthers", "Carolina", "CAR"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Carolina Panthers",
    },
    {
        "canonical": "Chicago Bears",
        "mascot": "Bears",
        "city": "Chicago",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#1f3f97",

        # Polymarket
        "polymarket_id": 53,
        "polymarket_abbreviation": "chi",
        "polymarket_name": "Chicago Bears",
        "polymarket_safe_name": "Chicago",
        "polymarket_names": ["Chicago Bears", "Chicago", "CHI"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Chicago Bears",
    },
    {
        "canonical": "Cincinnati Bengals",
        "mascot": "Bengals",
        "city": "Cincinnati",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#fb4e06",

        # Polymarket
        "polymarket_id": 54,
        "polymarket_abbreviation": "cin",
        "polymarket_name": "Cincinnati Bengals",
        "polymarket_safe_name": "Cincinnati",
        "polymarket_names": ["Cincinnati Bengals", "Cincinnati", "CIN"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Cincinnati Bengals",
    },
    {
        "canonical": "Cleveland Browns",
        "mascot": "Browns",
        "city": "Cleveland",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#f73802",

        # Polymarket
        "polymarket_id": 55,
        "polymarket_abbreviation": "cle",
        "polymarket_name": "Cleveland Browns",
        "polymarket_safe_name": "Cleveland",
        "polymarket_names": ["Cleveland Browns", "Cleveland", "CLE"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Cleveland Browns",
    },
    {
        "canonical": "Dallas Cowboys",
        "mascot": "Cowboys",
        "city": "Dallas",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#0c489e",

        # Polymarket
        "polymarket_id": 56,
        "polymarket_abbreviation": "dal",
        "polymarket_name": "Dallas Cowboys",
        "polymarket_safe_name": "Dallas",
        "polymarket_names": ["Dallas Cowboys", "Dallas", "DAL"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Dallas Cowboys",
    },
    {
        "canonical": "Denver Broncos",
        "mascot": "Broncos",
        "city": "Denver",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#f34c10",

        # Polymarket
        "polymarket_id": 57,
        "polymarket_abbreviation": "den",
        "polymarket_name": "Denver Broncos",
        "polymarket_safe_name": "Denver",
        "polymarket_names": ["Denver Broncos", "Denver", "DEN"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Denver Broncos",
    },
    {
        "canonical": "Detroit Lions",
        "mascot": "Lions",
        "city": "Detroit",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#1290d7",

        # Polymarket
        "polymarket_id": 58,
        "polymarket_abbreviation": "det",
        "polymarket_name": "Detroit Lions",
        "polymarket_safe_name": "Detroit",
        "polymarket_names": ["Detroit Lions", "Detroit", "DET"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Detroit Lions",
    },
    {
        "canonical": "Green Bay Packers",
        "mascot": "Packers",
        "city": "Green Bay",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#306456",

        # Polymarket
        "polymarket_id": 59,
        "polymarket_abbreviation": "gb",
        "polymarket_name": "Green Bay Packers",
        "polymarket_safe_name": "Green Bay",
        "polymarket_names": ["Green Bay Packers", "Green Bay", "GB"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Green Bay Packers",
    },
    {
        "canonical": "Houston Texans",
        "mascot": "Texans",
        "city": "Houston",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#1f3f97",

        # Polymarket
        "polymarket_id": 60,
        "polymarket_abbreviation": "hou",
        "polymarket_name": "Houston Texans",
        "polymarket_safe_name": "Houston",
        "polymarket_names": ["Houston Texans", "Houston", "HOU"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Houston Texans",
    },
    {
        "canonical": "Indianapolis Colts",
        "mascot": "Colts",
        "city": "Indianapolis",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#0e56a3",

        # Polymarket
        "polymarket_id": 61,
        "polymarket_abbreviation": "ind",
        "polymarket_name": "Indianapolis Colts",
        "polymarket_safe_name": "Indianapolis",
        "polymarket_names": ["Indianapolis Colts", "Indianapolis", "IND"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Indianapolis Colts",
    },
    {
        "canonical": "Jacksonville Jaguars",
        "mascot": "Jaguars",
        "city": "Jacksonville",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#158bb6",

        # Polymarket
        "polymarket_id": 62,
        "polymarket_abbreviation": "jax",
        "polymarket_name": "Jacksonville Jaguars",
        "polymarket_safe_name": "Jacksonville",
        "polymarket_names": ["Jacksonville Jaguars", "Jacksonville", "JAX"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Jacksonville Jaguars",
    },
    {
        "canonical": "Kansas City Chiefs",
        "mascot": "Chiefs",
        "city": "Kansas City",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#db1619",

        # Polymarket
        "polymarket_id": 63,
        "polymarket_abbreviation": "kc",
        "polymarket_name": "Kansas City Chiefs",
        "polymarket_safe_name": "Kansas City",
        "polymarket_names": ["Kansas City Chiefs", "Kansas City", "KC"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Kansas City Chiefs",
    },
    {
        "canonical": "Las Vegas Raiders",
        "mascot": "Raiders",
        "city": "Las Vegas",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#6e7881",

        # Polymarket
        "polymarket_id": 66,
        "polymarket_abbreviation": "lv",
        "polymarket_name": "Las Vegas Raiders",
        "polymarket_safe_name": "Las Vegas",
        "polymarket_names": ["Las Vegas Raiders", "Las Vegas", "LV"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Las Vegas Raiders",
    },
    {
        "canonical": "Los Angeles Chargers",
        "mascot": "Chargers",
        "city": "Los Angeles",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#007cc5",

        # Polymarket
        "polymarket_id": 65,
        "polymarket_abbreviation": "lac",
        "polymarket_name": "Los Angeles Chargers",
        "polymarket_safe_name": "Los Angeles C",
        "polymarket_names": ["Los Angeles Chargers", "Los Angeles C", "LAC"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Los Angeles Chargers",
    },
    {
        "canonical": "Los Angeles Rams",
        "mascot": "Rams",
        "city": "Los Angeles",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#155eab",

        # Polymarket
        "polymarket_id": 64,
        "polymarket_abbreviation": "lar",
        "polymarket_name": "Los Angeles Rams",
        "polymarket_safe_name": "Los Angeles R",
        "polymarket_names": ["Los Angeles Rams", "Los Angeles R", "LAR"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Los Angeles Rams",
    },
    {
        "canonical": "Miami Dolphins",
        "mascot": "Dolphins",
        "city": "Miami",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#008991",

        # Polymarket
        "polymarket_id": 67,
        "polymarket_abbreviation": "mia",
        "polymarket_name": "Miami Dolphins",
        "polymarket_safe_name": "Miami",
        "polymarket_names": ["Miami Dolphins", "Miami", "MIA"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Miami Dolphins",
    },
    {
        "canonical": "Minnesota Vikings",
        "mascot": "Vikings",
        "city": "Minnesota",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#623599",

        # Polymarket
        "polymarket_id": 68,
        "polymarket_abbreviation": "min",
        "polymarket_name": "Minnesota Vikings",
        "polymarket_safe_name": "Minnesota",
        "polymarket_names": ["Minnesota Vikings", "Minnesota", "MIN"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Minnesota Vikings",
    },
    {
        "canonical": "New England Patriots",
        "mascot": "Patriots",
        "city": "New England",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#c60c30",

        # Polymarket
        "polymarket_id": 69,
        "polymarket_abbreviation": "ne",
        "polymarket_name": "New England Patriots",
        "polymarket_safe_name": "New England",
        "polymarket_names": ["New England Patriots", "New England", "NE"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "New England Patriots",
    },
    {
        "canonical": "New Orleans Saints",
        "mascot": "Saints",
        "city": "New Orleans",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#cda96f",

        # Polymarket
        "polymarket_id": 70,
        "polymarket_abbreviation": "no",
        "polymarket_name": "New Orleans Saints",
        "polymarket_safe_name": "New Orleans",
        "polymarket_names": ["New Orleans Saints", "New Orleans", "NO"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "New Orleans Saints",
    },
    {
        "canonical": "New York Giants",
        "mascot": "Giants",
        "city": "New York",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#2545a4",

        # Polymarket
        "polymarket_id": 71,
        "polymarket_abbreviation": "nyg",
        "polymarket_name": "New York Giants",
        "polymarket_safe_name": "New York G",
        "polymarket_names": ["New York Giants", "New York G", "NYG"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "New York Giants",
    },
    {
        "canonical": "New York Jets",
        "mascot": "Jets",
        "city": "New York",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#1a654d",

        # Polymarket
        "polymarket_id": 72,
        "polymarket_abbreviation": "nyj",
        "polymarket_name": "New York Jets",
        "polymarket_safe_name": "New York J",
        "polymarket_names": ["New York Jets", "New York J", "NYJ"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "New York Jets",
    },
    {
        "canonical": "Philadelphia Eagles",
        "mascot": "Eagles",
        "city": "Philadelphia",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#11687f",

        # Polymarket
        "polymarket_id": 73,
        "polymarket_abbreviation": "phi",
        "polymarket_name": "Philadelphia Eagles",
        "polymarket_safe_name": "Philadelphia",
        "polymarket_names": ["Philadelphia Eagles", "Philadelphia", "PHI"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Philadelphia Eagles",
    },
    {
        "canonical": "Pittsburgh Steelers",
        "mascot": "Steelers",
        "city": "Pittsburgh",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#e5ad2f",

        # Polymarket
        "polymarket_id": 74,
        "polymarket_abbreviation": "pit",
        "polymarket_name": "Pittsburgh Steelers",
        "polymarket_safe_name": "Pittsburgh",
        "polymarket_names": ["Pittsburgh Steelers", "Pittsburgh", "PIT"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Pittsburgh Steelers",
    },
    {
        "canonical": "San Francisco 49ers",
        "mascot": "49ers",
        "city": "San Francisco",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#c11512",

        # Polymarket
        "polymarket_id": 76,
        "polymarket_abbreviation": "sf",
        "polymarket_name": "San Francisco 49ers",
        "polymarket_safe_name": "San Francisco",
        "polymarket_names": ["San Francisco 49ers", "San Francisco", "SF"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "San Francisco 49ers",
    },
    {
        "canonical": "Seattle Seahawks",
        "mascot": "Seahawks",
        "city": "Seattle",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#1d4e9b",

        # Polymarket
        "polymarket_id": 75,
        "polymarket_abbreviation": "sea",
        "polymarket_name": "Seattle Seahawks",
        "polymarket_safe_name": "Seattle",
        "polymarket_names": ["Seattle Seahawks", "Seattle", "SEA"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Seattle Seahawks",
    },
    {
        "canonical": "Tampa Bay Buccaneers",
        "mascot": "Buccaneers",
        "city": "Tampa Bay",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#c12d2f",

        # Polymarket
        "polymarket_id": 77,
        "polymarket_abbreviation": "tb",
        "polymarket_name": "Tampa Bay Buccaneers",
        "polymarket_safe_name": "Tampa Bay",
        "polymarket_names": ["Tampa Bay Buccaneers", "Tampa Bay", "TB"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Tampa Bay Buccaneers",
    },
    {
        "canonical": "Tennessee Titans",
        "mascot": "Titans",
        "city": "Tennessee",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#50a3e3",

        # Polymarket
        "polymarket_id": 78,
        "polymarket_abbreviation": "ten",
        "polymarket_name": "Tennessee Titans",
        "polymarket_safe_name": "Tennessee",
        "polymarket_names": ["Tennessee Titans", "Tennessee", "TEN"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Tennessee Titans",
    },
    {
        "canonical": "Washington Commanders",
        "mascot": "Commanders",
        "city": "Washington",
        "league": "nfl",
        "sport": "americanfootball_nfl",
        "color": "#841f1f",

        # Polymarket
        "polymarket_id": 79,
        "polymarket_abbreviation": "was",
        "polymarket_name": "Washington Commanders",
        "polymarket_safe_name": "Washington",
        "polymarket_names": ["Washington Commanders", "Washington", "WAS"],

        # Odds API
        "odds_api_key": "americanfootball_nfl",
        "odds_api_name": "Washington Commanders",
    },

    # =========================================================
    # MLS
    # =========================================================
    {
        "canonical": "Atlanta United FC",
        "mascot": "Atlanta United FC",
        "city": "Atlanta",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#80000A",

        # Polymarket
        "polymarket_id": 2283,
        "polymarket_abbreviation": "atl",
        "polymarket_name": "Atlanta United FC",
        "polymarket_safe_name": "Atlanta United FC",
        "polymarket_names": ["Atlanta United FC", "ATL"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "Atlanta United FC",
    },
    {
        "canonical": "Austin FC",
        "mascot": "Austin FC",
        "city": "Austin",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#00B140",

        # Polymarket
        "polymarket_id": 2289,
        "polymarket_abbreviation": "aus",
        "polymarket_name": "Austin FC",
        "polymarket_safe_name": "Austin FC",
        "polymarket_names": ["Austin FC", "AUS"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "Austin FC",
    },
    {
        "canonical": "CF Montreal",
        "mascot": "CF Montreal",
        "city": "Montreal",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#06209A",

        # Polymarket
        "polymarket_id": 2270,
        "polymarket_abbreviation": "mim",
        "polymarket_name": "CF Montréal",
        "polymarket_safe_name": "CF Montreal",
        "polymarket_names": ["CF Montréal", "CF Montreal", "MIM"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "CF Montreal",
    },
    {
        "canonical": "Charlotte FC",
        "mascot": "Charlotte FC",
        "city": "Charlotte",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#367EBB",

        # Polymarket
        "polymarket_id": 2290,
        "polymarket_abbreviation": "clt",
        "polymarket_name": "Charlotte FC",
        "polymarket_safe_name": "Charlotte FC",
        "polymarket_names": ["Charlotte FC", "CLT"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "Charlotte FC",
    },
    {
        "canonical": "Chicago Fire FC",
        "mascot": "Fire",
        "city": "Chicago",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#5FC1EA",

        # Polymarket
        "polymarket_id": 2263,
        "polymarket_abbreviation": "chi",
        "polymarket_name": "Chicago Fire FC",
        "polymarket_safe_name": "Chicago Fire FC",
        "polymarket_names": ["Chicago Fire FC", "Chicago Fire", "CHI"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "Chicago Fire",
    },
    {
        "canonical": "Colorado Rapids",
        "mascot": "Rapids",
        "city": "Colorado",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#960A2C",

        # Polymarket
        "polymarket_id": 2264,
        "polymarket_abbreviation": "col",
        "polymarket_name": "Colorado Rapids SC",
        "polymarket_safe_name": "Colorado Rapids SC",
        "polymarket_names": ["Colorado Rapids SC", "Colorado Rapids", "COL"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "Colorado Rapids",
    },
    {
        "canonical": "Columbus Crew",
        "mascot": "Crew",
        "city": "Columbus",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#2B2707",

        # Polymarket
        "polymarket_id": 2265,
        "polymarket_abbreviation": "clb",
        "polymarket_name": "Columbus Crew",
        "polymarket_safe_name": "Columbus Crew",
        "polymarket_names": ["Columbus Crew", "Columbus Crew SC", "CLB"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "Columbus Crew SC",
    },
    {
        "canonical": "D.C. United",
        "mascot": "United",
        "city": "Washington",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#EB0029",

        # Polymarket
        "polymarket_id": 2266,
        "polymarket_abbreviation": "dcu",
        "polymarket_name": "D.C. United SC",
        "polymarket_safe_name": "D.C. United SC",
        "polymarket_names": ["D.C. United SC", "D.C. United", "DCU"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "D.C. United",
    },
    {
        "canonical": "FC Cincinnati",
        "mascot": "FC Cincinnati",
        "city": "Cincinnati",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#FE5000",

        # Polymarket
        "polymarket_id": 2286,
        "polymarket_abbreviation": "fcc",
        "polymarket_name": "FC Cincinnati",
        "polymarket_safe_name": "FC Cincinnati",
        "polymarket_names": ["FC Cincinnati", "FCC"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "FC Cincinnati",
    },
    {
        "canonical": "FC Dallas",
        "mascot": "FC Dallas",
        "city": "Dallas",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#C6093B",

        # Polymarket
        "polymarket_id": 2267,
        "polymarket_abbreviation": "dal",
        "polymarket_name": "FC Dallas",
        "polymarket_safe_name": "FC Dallas",
        "polymarket_names": ["FC Dallas", "DAL"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "FC Dallas",
    },
    {
        "canonical": "Houston Dynamo",
        "mascot": "Dynamo",
        "city": "Houston",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#FF6B00",

        # Polymarket
        "polymarket_id": 2268,
        "polymarket_abbreviation": "hou",
        "polymarket_name": "Houston Dynamo",
        "polymarket_safe_name": "Houston Dynamo",
        "polymarket_names": ["Houston Dynamo", "HOU"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "Houston Dynamo",
    },
    {
        "canonical": "Inter Miami CF",
        "mascot": "Inter Miami CF",
        "city": "Miami",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#EB84A9",

        # Polymarket
        "polymarket_id": 2287,
        "polymarket_abbreviation": "mia",
        "polymarket_name": "Inter Miami CF",
        "polymarket_safe_name": "Inter Miami CF",
        "polymarket_names": ["Inter Miami CF", "MIA"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "Inter Miami CF",
    },
    {
        "canonical": "LA Galaxy",
        "mascot": "Galaxy",
        "city": "Los Angeles",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#00245D",

        # Polymarket
        "polymarket_id": 2269,
        "polymarket_abbreviation": "lag",
        "polymarket_name": "Los Angeles Galaxy",
        "polymarket_safe_name": "Los Angeles Galaxy",
        "polymarket_names": ["Los Angeles Galaxy", "LA Galaxy", "LAG"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "LA Galaxy",
    },
    {
        "canonical": "Los Angeles FC",
        "mascot": "Los Angeles FC",
        "city": "Los Angeles",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#C39E6D",

        # Polymarket
        "polymarket_id": 2285,
        "polymarket_abbreviation": "laf",
        "polymarket_name": "Los Angeles FC",
        "polymarket_safe_name": "Los Angeles FC",
        "polymarket_names": ["Los Angeles FC", "LAFC", "LAF"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "Los Angeles FC",
    },
    {
        "canonical": "Minnesota United FC",
        "mascot": "Loons",
        "city": "Minneapolis",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#8CD2F4",

        # Polymarket
        "polymarket_id": 2284,
        "polymarket_abbreviation": "min",
        "polymarket_name": "Minnesota United FC",
        "polymarket_safe_name": "Minnesota United FC",
        "polymarket_names": ["Minnesota United FC", "Minnesota United", "MIN"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "Minnesota United FC",
    },
    {
        "canonical": "Nashville SC",
        "mascot": "Nashville SC",
        "city": "Nashville",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#1F1646",

        # Polymarket
        "polymarket_id": 2288,
        "polymarket_abbreviation": "nas",
        "polymarket_name": "Nashville SC",
        "polymarket_safe_name": "Nashville SC",
        "polymarket_names": ["Nashville SC", "NAS"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "Nashville SC",
    },
    {
        "canonical": "New England Revolution",
        "mascot": "Revolution",
        "city": "Boston",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#CE0E2D",

        # Polymarket
        "polymarket_id": 2271,
        "polymarket_abbreviation": "ner",
        "polymarket_name": "New England Revolution",
        "polymarket_safe_name": "New England Revolution",
        "polymarket_names": ["New England Revolution", "NER"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "New England Revolution",
    },
    {
        "canonical": "New York City FC",
        "mascot": "New York City FC",
        "city": "New York",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#6CACE4",

        # Polymarket
        "polymarket_id": 2272,
        "polymarket_abbreviation": "nyc",
        "polymarket_name": "New York City FC",
        "polymarket_safe_name": "New York City FC",
        "polymarket_names": ["New York City FC", "NYCFC", "NYC"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "New York City FC",
    },
    {
        "canonical": "New York Red Bulls",
        "mascot": "Red Bulls",
        "city": "New York",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#ED1E36",

        # Polymarket
        "polymarket_id": 2273,
        "polymarket_abbreviation": "nyr",
        "polymarket_name": "New York Red Bulls",
        "polymarket_safe_name": "New York Red Bulls",
        "polymarket_names": ["New York Red Bulls", "NYRB", "NYR"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "New York Red Bulls",
    },
    {
        "canonical": "Orlando City SC",
        "mascot": "Lions",
        "city": "Orlando",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#633492",

        # Polymarket
        "polymarket_id": 2274,
        "polymarket_abbreviation": "orl",
        "polymarket_name": "Orlando City SC",
        "polymarket_safe_name": "Orlando City SC",
        "polymarket_names": ["Orlando City SC", "Orlando City", "ORL"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "Orlando City SC",
    },
    {
        "canonical": "Philadelphia Union",
        "mascot": "Union",
        "city": "Philadelphia",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#3A8DDE",

        # Polymarket
        "polymarket_id": 2275,
        "polymarket_abbreviation": "phi",
        "polymarket_name": "Philadelphia Union",
        "polymarket_safe_name": "Philadelphia Union",
        "polymarket_names": ["Philadelphia Union", "PHI"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "Philadelphia Union",
    },
    {
        "canonical": "Portland Timbers",
        "mascot": "Timbers",
        "city": "Portland",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#00482B",

        # Polymarket
        "polymarket_id": 2276,
        "polymarket_abbreviation": "por",
        "polymarket_name": "Portland Timbers",
        "polymarket_safe_name": "Portland Timbers",
        "polymarket_names": ["Portland Timbers", "POR"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "Portland Timbers",
    },
    {
        "canonical": "Real Salt Lake",
        "mascot": "Real Salt Lake",
        "city": "Salt Lake City",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#B30838",

        # Polymarket
        "polymarket_id": 2277,
        "polymarket_abbreviation": "rsl",
        "polymarket_name": "Real Salt Lake",
        "polymarket_safe_name": "Real Salt Lake",
        "polymarket_names": ["Real Salt Lake", "RSL"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "Real Salt Lake",
    },
    {
        "canonical": "San Diego FC",
        "mascot": "San Diego FC",
        "city": "San Diego",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#071528",

        # Polymarket
        "polymarket_id": 2292,
        "polymarket_abbreviation": "sdg",
        "polymarket_name": "San Diego FC",
        "polymarket_safe_name": "San Diego FC",
        "polymarket_names": ["San Diego FC", "SDG"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "San Diego FC",
    },
    {
        "canonical": "San Jose Earthquakes",
        "mascot": "Earthquakes",
        "city": "San Jose",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#003DA6",

        # Polymarket
        "polymarket_id": 2278,
        "polymarket_abbreviation": "sje",
        "polymarket_name": "San Jose Earthquakes",
        "polymarket_safe_name": "San Jose Earthquakes",
        "polymarket_names": ["San Jose Earthquakes", "SJE"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "San Jose Earthquakes",
    },
    {
        "canonical": "Seattle Sounders FC",
        "mascot": "Sounders",
        "city": "Seattle",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#4FB84F",

        # Polymarket
        "polymarket_id": 2279,
        "polymarket_abbreviation": "sea",
        "polymarket_name": "Seattle Sounders FC",
        "polymarket_safe_name": "Seattle Sounders FC",
        "polymarket_names": ["Seattle Sounders FC", "Seattle Sounders", "SEA"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "Seattle Sounders FC",
    },
    {
        "canonical": "Sporting Kansas City",
        "mascot": "Sporting Kansas City",
        "city": "Kansas City",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#002F65",

        # Polymarket
        "polymarket_id": 2280,
        "polymarket_abbreviation": "skc",
        "polymarket_name": "Sporting Kansas City",
        "polymarket_safe_name": "Sporting Kansas City",
        "polymarket_names": ["Sporting Kansas City", "SKC"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "Sporting Kansas City",
    },
    {
        "canonical": "St. Louis City SC",
        "mascot": "St. Louis City SC",
        "city": "St. Louis",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#EC1458",

        # Polymarket
        "polymarket_id": 2291,
        "polymarket_abbreviation": "stl",
        "polymarket_name": "St. Louis City SC",
        "polymarket_safe_name": "St. Louis City SC",
        "polymarket_names": ["St. Louis City SC", "STL"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "St. Louis City SC",
    },
    {
        "canonical": "Toronto FC",
        "mascot": "Toronto FC",
        "city": "Toronto",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#AA182C",

        # Polymarket
        "polymarket_id": 2281,
        "polymarket_abbreviation": "tor",
        "polymarket_name": "Toronto FC",
        "polymarket_safe_name": "Toronto FC",
        "polymarket_names": ["Toronto FC", "TOR"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "Toronto FC",
    },
    {
        "canonical": "Vancouver Whitecaps FC",
        "mascot": "Whitecaps",
        "city": "Vancouver",
        "league": "mls",
        "sport": "soccer_usa_mls",
        "color": "#00245E",

        # Polymarket
        "polymarket_id": 2282,
        "polymarket_abbreviation": "vwh",
        "polymarket_name": "Vancouver Whitecaps FC",
        "polymarket_safe_name": "Vancouver Whitecaps FC",
        "polymarket_names": ["Vancouver Whitecaps FC", "Vancouver Whitecaps", "VWH"],

        # Odds API
        "odds_api_key": "soccer_usa_mls",
        "odds_api_name": "Vancouver Whitecaps FC",
    },

    # =========================================================
    # EPL
    # =========================================================
    {
        "canonical": "Arsenal",
        "mascot": "Arsenal",
        "city": "London",
        "league": "epl",
        "sport": "soccer_epl",
        "color": "#EF0007",

        # Polymarket
        "polymarket_id": 2686,
        "polymarket_abbreviation": "ars",
        "polymarket_name": "Arsenal FC",
        "polymarket_safe_name": "Arsenal",
        "polymarket_names": ["Arsenal FC", "Arsenal", "ARS"],

        # Odds API
        "odds_api_key": "soccer_epl",
        "odds_api_name": "Arsenal",
    },
    {
        "canonical": "Aston Villa",
        "mascot": "Aston Villa",
        "city": "Birmingham",
        "league": "epl",
        "sport": "soccer_epl",
        "color": "#670E36",

        # Polymarket
        "polymarket_id": 2687,
        "polymarket_abbreviation": "ast",
        "polymarket_name": "Aston Villa FC",
        "polymarket_safe_name": "Aston Villa",
        "polymarket_names": ["Aston Villa FC", "Aston Villa", "AST"],

        # Odds API
        "odds_api_key": "soccer_epl",
        "odds_api_name": "Aston Villa",
    },
    {
        "canonical": "Bournemouth",
        "mascot": "Bournemouth",
        "city": "Bournemouth",
        "league": "epl",
        "sport": "soccer_epl",
        "color": "#E62333",

        # Polymarket
        "polymarket_id": 2685,
        "polymarket_abbreviation": "bor",
        "polymarket_name": "AFC Bournemouth",
        "polymarket_safe_name": "Bournemouth",
        "polymarket_names": ["AFC Bournemouth", "Bournemouth", "BOR"],

        # Odds API
        "odds_api_key": "soccer_epl",
        "odds_api_name": "Bournemouth",
    },
    {
        "canonical": "Brentford",
        "mascot": "Brentford",
        "city": "London",
        "league": "epl",
        "sport": "soccer_epl",
        "color": "#E30613",

        # Polymarket
        "polymarket_id": 2714,
        "polymarket_abbreviation": "bre",
        "polymarket_name": "Brentford FC",
        "polymarket_safe_name": "Brentford",
        "polymarket_names": ["Brentford FC", "Brentford", "BRE"],

        # Odds API
        "odds_api_key": "soccer_epl",
        "odds_api_name": "Brentford",
    },
    {
        "canonical": "Brighton & Hove Albion",
        "mascot": "Brighton & Hove Albion",
        "city": "Brighton",
        "league": "epl",
        "sport": "soccer_epl",
        "color": "#0055A9",

        # Polymarket
        "polymarket_id": 2708,
        "polymarket_abbreviation": "bha",
        "polymarket_name": "Brighton & Hove Albion FC",
        "polymarket_safe_name": "Brighton & Hove Albion",
        "polymarket_names": ["Brighton & Hove Albion FC", "Brighton & Hove Albion", "Brighton and Hove Albion", "BHA"],

        # Odds API
        "odds_api_key": "soccer_epl",
        "odds_api_name": "Brighton and Hove Albion",
    },
    {
        "canonical": "Burnley",
        "mascot": "Burnley",
        "city": "Burnley",
        "league": "epl",
        "sport": "soccer_epl",
        "color": "#8CCCE5",

        # Polymarket
        "polymarket_id": 2705,
        "polymarket_abbreviation": "bur",
        "polymarket_name": "Burnley FC",
        "polymarket_safe_name": "Burnley",
        "polymarket_names": ["Burnley FC", "Burnley", "BUR"],

        # Odds API
        "odds_api_key": "soccer_epl",
        "odds_api_name": "Burnley",
    },
    {
        "canonical": "Chelsea",
        "mascot": "Chelsea",
        "city": "London",
        "league": "epl",
        "sport": "soccer_epl",
        "color": "#034694",

        # Polymarket
        "polymarket_id": 2688,
        "polymarket_abbreviation": "cfc",
        "polymarket_name": "Chelsea FC",
        "polymarket_safe_name": "Chelsea",
        "polymarket_names": ["Chelsea FC", "Chelsea", "CFC"],

        # Odds API
        "odds_api_key": "soccer_epl",
        "odds_api_name": "Chelsea",
    },
    {
        "canonical": "Crystal Palace",
        "mascot": "Crystal Palace",
        "city": "London",
        "league": "epl",
        "sport": "soccer_epl",
        "color": "#1B458F",

        # Polymarket
        "polymarket_id": 2689,
        "polymarket_abbreviation": "cry",
        "polymarket_name": "Crystal Palace FC",
        "polymarket_safe_name": "Crystal Palace",
        "polymarket_names": ["Crystal Palace FC", "Crystal Palace", "CRY"],

        # Odds API
        "odds_api_key": "soccer_epl",
        "odds_api_name": "Crystal Palace",
    },
    {
        "canonical": "Everton",
        "mascot": "Everton",
        "city": "Liverpool",
        "league": "epl",
        "sport": "soccer_epl",
        "color": "#274488",

        # Polymarket
        "polymarket_id": 2690,
        "polymarket_abbreviation": "eve",
        "polymarket_name": "Everton FC",
        "polymarket_safe_name": "Everton",
        "polymarket_names": ["Everton FC", "Everton", "EVE"],

        # Odds API
        "odds_api_key": "soccer_epl",
        "odds_api_name": "Everton",
    },
    {
        "canonical": "Fulham",
        "mascot": "Fulham",
        "city": "London",
        "league": "epl",
        "sport": "soccer_epl",
        "color": "#CC0100",

        # Polymarket
        "polymarket_id": 2711,
        "polymarket_abbreviation": "ful",
        "polymarket_name": "Fulham FC",
        "polymarket_safe_name": "Fulham",
        "polymarket_names": ["Fulham FC", "Fulham", "FUL"],

        # Odds API
        "odds_api_key": "soccer_epl",
        "odds_api_name": "Fulham",
    },
    {
        "canonical": "Leeds United",
        "mascot": "Leeds United",
        "city": "Leeds",
        "league": "epl",
        "sport": "soccer_epl",
        "color": "#034694",

        # Polymarket
        "polymarket_id": 2716,
        "polymarket_abbreviation": "lee",
        "polymarket_name": "Leeds United FC",
        "polymarket_safe_name": "Leeds United",
        "polymarket_names": ["Leeds United FC", "Leeds United", "LEE"],

        # Odds API
        "odds_api_key": "soccer_epl",
        "odds_api_name": "Leeds United",
    },
    {
        "canonical": "Liverpool",
        "mascot": "Liverpool",
        "city": "Liverpool",
        "league": "epl",
        "sport": "soccer_epl",
        "color": "#00857B",

        # Polymarket
        "polymarket_id": 2692,
        "polymarket_abbreviation": "liv",
        "polymarket_name": "Liverpool FC",
        "polymarket_safe_name": "Liverpool",
        "polymarket_names": ["Liverpool FC", "Liverpool", "LIV"],

        # Odds API
        "odds_api_key": "soccer_epl",
        "odds_api_name": "Liverpool",
    },
    {
        "canonical": "Manchester City",
        "mascot": "Manchester City",
        "city": "Manchester",
        "league": "epl",
        "sport": "soccer_epl",
        "color": "#98C5E9",

        # Polymarket
        "polymarket_id": 2693,
        "polymarket_abbreviation": "mnc",
        "polymarket_name": "Manchester City FC",
        "polymarket_safe_name": "Manchester City",
        "polymarket_names": ["Manchester City FC", "Manchester City", "MNC"],

        # Odds API
        "odds_api_key": "soccer_epl",
        "odds_api_name": "Manchester City",
    },
    {
        "canonical": "Manchester United",
        "mascot": "Manchester United",
        "city": "Manchester",
        "league": "epl",
        "sport": "soccer_epl",
        "color": "#DA020E",

        # Polymarket
        "polymarket_id": 2694,
        "polymarket_abbreviation": "mnu",
        "polymarket_name": "Manchester United FC",
        "polymarket_safe_name": "Manchester United",
        "polymarket_names": ["Manchester United FC", "Manchester United", "MNU"],

        # Odds API
        "odds_api_key": "soccer_epl",
        "odds_api_name": "Manchester United",
    },
    {
        "canonical": "Newcastle United",
        "mascot": "Newcastle United",
        "city": "Newcastle upon Tyne",
        "league": "epl",
        "sport": "soccer_epl",
        "color": "#274488",

        # Polymarket
        "polymarket_id": 2695,
        "polymarket_abbreviation": "new",
        "polymarket_name": "Newcastle United FC",
        "polymarket_safe_name": "Newcastle United",
        "polymarket_names": ["Newcastle United FC", "Newcastle United", "NEW"],

        # Odds API
        "odds_api_key": "soccer_epl",
        "odds_api_name": "Newcastle United",
    },
    {
        "canonical": "Nottingham Forest",
        "mascot": "Nottingham Forest",
        "city": "Nottingham",
        "league": "epl",
        "sport": "soccer_epl",
        "color": "#E22E30",

        # Polymarket
        "polymarket_id": 2718,
        "polymarket_abbreviation": "not",
        "polymarket_name": "Nottingham Forest FC",
        "polymarket_safe_name": "Nottingham Forest",
        "polymarket_names": ["Nottingham Forest FC", "Nottingham Forest", "NOT"],

        # Odds API
        "odds_api_key": "soccer_epl",
        "odds_api_name": "Nottingham Forest",
    },
    {
        "canonical": "Sunderland",
        "mascot": "Sunderland",
        "city": "Sunderland",
        "league": "epl",
        "sport": "soccer_epl",
        "color": "#EF0000",

        # Polymarket
        "polymarket_id": 2699,
        "polymarket_abbreviation": "sun",
        "polymarket_name": "Sunderland AFC",
        "polymarket_safe_name": "Sunderland",
        "polymarket_names": ["Sunderland AFC", "Sunderland", "SUN"],

        # Odds API
        "odds_api_key": "soccer_epl",
        "odds_api_name": "Sunderland",
    },
    {
        "canonical": "Tottenham Hotspur",
        "mascot": "Tottenham Hotspur",
        "city": "London",
        "league": "epl",
        "sport": "soccer_epl",
        "color": "#001C58",

        # Polymarket
        "polymarket_id": 2701,
        "polymarket_abbreviation": "tot",
        "polymarket_name": "Tottenham Hotspur FC",
        "polymarket_safe_name": "Tottenham Hotspur",
        "polymarket_names": ["Tottenham Hotspur FC", "Tottenham Hotspur", "TOT"],

        # Odds API
        "odds_api_key": "soccer_epl",
        "odds_api_name": "Tottenham Hotspur",
    },
    {
        "canonical": "West Ham United",
        "mascot": "West Ham United",
        "city": "London",
        "league": "epl",
        "sport": "soccer_epl",
        "color": "#902239",

        # Polymarket
        "polymarket_id": 2704,
        "polymarket_abbreviation": "whu",
        "polymarket_name": "West Ham United FC",
        "polymarket_safe_name": "West Ham United",
        "polymarket_names": ["West Ham United FC", "West Ham United", "WHU"],

        # Odds API
        "odds_api_key": "soccer_epl",
        "odds_api_name": "West Ham United",
    },
    {
        "canonical": "Wolverhampton Wanderers",
        "mascot": "Wolverhampton Wanderers",
        "city": "Wolverhampton",
        "league": "epl",
        "sport": "soccer_epl",
        "color": "#034694",

        # Polymarket
        "polymarket_id": 2712,
        "polymarket_abbreviation": "wol",
        "polymarket_name": "Wolverhampton Wanderers FC",
        "polymarket_safe_name": "Wolverhampton Wanderers",
        "polymarket_names": ["Wolverhampton Wanderers FC", "Wolverhampton Wanderers", "WOL"],

        # Odds API
        "odds_api_key": "soccer_epl",
        "odds_api_name": "Wolverhampton Wanderers",
    },

    # =========================================================
    # La Liga
    # =========================================================

    {
        "canonical": "Alavés",
        "mascot": "Alavés",
        "city": "Vitoria-Gasteiz",
        "league": "lal",
        "sport": "soccer_spain_la_liga",
        "color": "#0761AF",

        # Polymarket
        "polymarket_id": 3455,
        "polymarket_abbreviation": "ala",
        "polymarket_name": "Deportivo Alavés",
        "polymarket_safe_name": "Deportivo Alavés",
        "polymarket_names": ["Deportivo Alavés", "Alavés", "ALA"],

        # Odds API
        "odds_api_key": "soccer_spain_la_liga",
        "odds_api_name": "Alavés",
    },

    {
        "canonical": "Athletic Bilbao",
        "mascot": "Athletic Bilbao",
        "city": "Bilbao",
        "league": "lal",
        "sport": "soccer_spain_la_liga",
        "color": "#E91D1E",

        # Polymarket
        "polymarket_id": 3445,
        "polymarket_abbreviation": "ath",
        "polymarket_name": "Athletic Club",
        "polymarket_safe_name": "Athletic Club",
        "polymarket_names": ["Athletic Club", "Athletic Bilbao", "ATH"],

        # Odds API
        "odds_api_key": "soccer_spain_la_liga",
        "odds_api_name": "Athletic Bilbao",
    },

    {
        "canonical": "Atletico Madrid",
        "mascot": "Atletico Madrid",
        "city": "Madrid",
        "league": "lal",
        "sport": "soccer_spain_la_liga",
        "color": "#CB3524",

        # Polymarket
        "polymarket_id": 3440,
        "polymarket_abbreviation": "atm",
        "polymarket_name": "Club Atlético de Madrid",
        "polymarket_safe_name": "Club Atlético de Madrid",
        "polymarket_names": ["Club Atlético de Madrid", "Atletico Madrid", "Atlético Madrid", "ATM"],

        # Odds API
        "odds_api_key": "soccer_spain_la_liga",
        "odds_api_name": "Atlético Madrid",
    },

    {
        "canonical": "Barcelona",
        "mascot": "Barcelona",
        "city": "Barcelona",
        "league": "lal",
        "sport": "soccer_spain_la_liga",
        "color": "#004D98",

        # Polymarket
        "polymarket_id": 3441,
        "polymarket_abbreviation": "fcb",
        "polymarket_name": "FC Barcelona",
        "polymarket_safe_name": "FC Barcelona",
        "polymarket_names": ["FC Barcelona", "Barcelona", "FCB"],

        # Odds API
        "odds_api_key": "soccer_spain_la_liga",
        "odds_api_name": "Barcelona",
    },

    {
        "canonical": "CA Osasuna",
        "mascot": "CA Osasuna",
        "city": "Pamplona",
        "league": "lal",
        "sport": "soccer_spain_la_liga",
        "color": "#0A346F",

        # Polymarket
        "polymarket_id": 3454,
        "polymarket_abbreviation": "osa",
        "polymarket_name": "CA Osasuna",
        "polymarket_safe_name": "CA Osasuna",
        "polymarket_names": ["CA Osasuna", "Osasuna", "OSA"],

        # Odds API
        "odds_api_key": "soccer_spain_la_liga",
        "odds_api_name": "CA Osasuna",
    },

    {
        "canonical": "Celta Vigo",
        "mascot": "Celta Vigo",
        "city": "Vigo",
        "league": "lal",
        "sport": "soccer_spain_la_liga",
        "color": "#578FB7",

        # Polymarket
        "polymarket_id": 3449,
        "polymarket_abbreviation": "cel",
        "polymarket_name": "RC Celta de Vigo",
        "polymarket_safe_name": "RC Celta de Vigo",
        "polymarket_names": ["RC Celta de Vigo", "Celta Vigo", "CEL"],

        # Odds API
        "odds_api_key": "soccer_spain_la_liga",
        "odds_api_name": "Celta Vigo",
    },

    {
        "canonical": "Elche CF",
        "mascot": "Elche CF",
        "city": "Elche",
        "league": "lal",
        "sport": "soccer_spain_la_liga",
        "color": "#05642C",

        # Polymarket
        "polymarket_id": 3458,
        "polymarket_abbreviation": "elc",
        "polymarket_name": "Elche CF",
        "polymarket_safe_name": "Elche",
        "polymarket_names": ["Elche CF", "Elche", "ELC"],

        # Odds API
        "odds_api_key": "soccer_spain_la_liga",
        "odds_api_name": "Elche CF",
    },

    {
        "canonical": "Espanyol",
        "mascot": "Espanyol",
        "city": "Barcelona",
        "league": "lal",
        "sport": "soccer_spain_la_liga",
        "color": "#007CC4",

        # Polymarket
        "polymarket_id": 3450,
        "polymarket_abbreviation": "esp",
        "polymarket_name": "RCD Espanyol de Barcelona",
        "polymarket_safe_name": "RCD Espanyol de Barcelona",
        "polymarket_names": ["RCD Espanyol de Barcelona", "Espanyol", "ESP"],

        # Odds API
        "odds_api_key": "soccer_spain_la_liga",
        "odds_api_name": "Espanyol",
    },

    {
        "canonical": "Getafe",
        "mascot": "Getafe",
        "city": "Getafe",
        "league": "lal",
        "sport": "soccer_spain_la_liga",
        "color": "#005999",

        # Polymarket
        "polymarket_id": 3446,
        "polymarket_abbreviation": "get",
        "polymarket_name": "Getafe CF",
        "polymarket_safe_name": "Getafe",
        "polymarket_names": ["Getafe CF", "Getafe", "GET"],

        # Odds API
        "odds_api_key": "soccer_spain_la_liga",
        "odds_api_name": "Getafe",
    },

    {
        "canonical": "Girona",
        "mascot": "Girona",
        "city": "Girona",
        "league": "lal",
        "sport": "soccer_spain_la_liga",
        "color": "#CD2534",

        # Polymarket
        "polymarket_id": 3456,
        "polymarket_abbreviation": "gir",
        "polymarket_name": "Girona FC",
        "polymarket_safe_name": "Girona",
        "polymarket_names": ["Girona FC", "Girona", "GIR"],

        # Odds API
        "odds_api_key": "soccer_spain_la_liga",
        "odds_api_name": "Girona",
    },

    {
        "canonical": "Levante",
        "mascot": "Levante",
        "city": "Valencia",
        "league": "lal",
        "sport": "soccer_spain_la_liga",
        "color": "#B3013D",

        # Polymarket
        "polymarket_id": 3447,
        "polymarket_abbreviation": "lev",
        "polymarket_name": "Levante UD",
        "polymarket_safe_name": "Levante UD",
        "polymarket_names": ["Levante UD", "Levante", "LEV"],

        # Odds API
        "odds_api_key": "soccer_spain_la_liga",
        "odds_api_name": "Levante",
    },

    {
        "canonical": "Mallorca",
        "mascot": "Mallorca",
        "city": "Palma",
        "league": "lal",
        "sport": "soccer_spain_la_liga",
        "color": "#E20613",

        # Polymarket
        "polymarket_id": 3457,
        "polymarket_abbreviation": "mall",
        "polymarket_name": "RCD Mallorca",
        "polymarket_safe_name": "RCD Mallorca",
        "polymarket_names": ["RCD Mallorca", "Mallorca", "MALL"],

        # Odds API
        "odds_api_key": "soccer_spain_la_liga",
        "odds_api_name": "Mallorca",
    },

    {
        "canonical": "Rayo Vallecano",
        "mascot": "Rayo Vallecano",
        "city": "Madrid",
        "league": "lal",
        "sport": "soccer_spain_la_liga",
        "color": "#E32D25",

        # Polymarket
        "polymarket_id": 3448,
        "polymarket_abbreviation": "ray",
        "polymarket_name": "Rayo Vallecano de Madrid",
        "polymarket_safe_name": "Rayo Vallecano de Madrid",
        "polymarket_names": ["Rayo Vallecano de Madrid", "Rayo Vallecano", "RAY"],

        # Odds API
        "odds_api_key": "soccer_spain_la_liga",
        "odds_api_name": "Rayo Vallecano",
    },

    {
        "canonical": "Real Betis",
        "mascot": "Real Betis",
        "city": "Seville",
        "league": "lal",
        "sport": "soccer_spain_la_liga",
        "color": "#0BB363",

        # Polymarket
        "polymarket_id": 3451,
        "polymarket_abbreviation": "bet",
        "polymarket_name": "Real Betis Balompié",
        "polymarket_safe_name": "Real Betis Balompié",
        "polymarket_names": ["Real Betis Balompié", "Real Betis", "BET"],

        # Odds API
        "odds_api_key": "soccer_spain_la_liga",
        "odds_api_name": "Real Betis",
    },

    {
        "canonical": "Real Madrid",
        "mascot": "Real Madrid",
        "city": "Madrid",
        "league": "lal",
        "sport": "soccer_spain_la_liga",
        "color": "#00529F",

        # Polymarket
        "polymarket_id": 3442,
        "polymarket_abbreviation": "rma",
        "polymarket_name": "Real Madrid CF",
        "polymarket_safe_name": "Real Madrid",
        "polymarket_names": ["Real Madrid CF", "Real Madrid", "RMA"],

        # Odds API
        "odds_api_key": "soccer_spain_la_liga",
        "odds_api_name": "Real Madrid",
    },

    {
        "canonical": "Real Oviedo",
        "mascot": "Real Oviedo",
        "city": "Oviedo",
        "league": "lal",
        "sport": "soccer_spain_la_liga",
        "color": "#004393",

        # Polymarket
        "polymarket_id": 3459,
        "polymarket_abbreviation": "ovi",
        "polymarket_name": "Real Oviedo",
        "polymarket_safe_name": "Real Oviedo",
        "polymarket_names": ["Real Oviedo", "Oviedo", "OVI"],

        # Odds API
        "odds_api_key": "soccer_spain_la_liga",
        "odds_api_name": "Oviedo",
    },

    {
        "canonical": "Real Sociedad",
        "mascot": "Real Sociedad",
        "city": "San Sebastián",
        "league": "lal",
        "sport": "soccer_spain_la_liga",
        "color": "#0067B1",

        # Polymarket
        "polymarket_id": 3452,
        "polymarket_abbreviation": "rso",
        "polymarket_name": "Real Sociedad de Fútbol",
        "polymarket_safe_name": "Real Sociedad de Fútbol",
        "polymarket_names": ["Real Sociedad de Fútbol", "Real Sociedad", "RSO"],

        # Odds API
        "odds_api_key": "soccer_spain_la_liga",
        "odds_api_name": "Real Sociedad",
    },

    {
        "canonical": "Sevilla",
        "mascot": "Sevilla",
        "city": "Seville",
        "league": "lal",
        "sport": "soccer_spain_la_liga",
        "color": "#E72227",

        # Polymarket
        "polymarket_id": 3443,
        "polymarket_abbreviation": "sev",
        "polymarket_name": "Sevilla FC",
        "polymarket_safe_name": "Sevilla",
        "polymarket_names": ["Sevilla FC", "Sevilla", "SEV"],

        # Odds API
        "odds_api_key": "soccer_spain_la_liga",
        "odds_api_name": "Sevilla",
    },

    {
        "canonical": "Valencia",
        "mascot": "Valencia",
        "city": "Valencia",
        "league": "lal",
        "sport": "soccer_spain_la_liga",
        "color": "#FF671F",

        # Polymarket
        "polymarket_id": 3444,
        "polymarket_abbreviation": "val",
        "polymarket_name": "Valencia CF",
        "polymarket_safe_name": "Valencia",
        "polymarket_names": ["Valencia CF", "Valencia", "VAL"],

        # Odds API
        "odds_api_key": "soccer_spain_la_liga",
        "odds_api_name": "Valencia",
    },

    {
        "canonical": "Villarreal",
        "mascot": "Villarreal",
        "city": "Villarreal",
        "league": "lal",
        "sport": "soccer_spain_la_liga",
        "color": "#005187",

        # Polymarket
        "polymarket_id": 3453,
        "polymarket_abbreviation": "vil",
        "polymarket_name": "Villarreal CF",
        "polymarket_safe_name": "Villarreal",
        "polymarket_names": ["Villarreal CF", "Villarreal", "VIL"],

        # Odds API
        "odds_api_key": "soccer_spain_la_liga",
        "odds_api_name": "Villarreal",
    },

    # =========================================================
    # Bundesliga
    # =========================================================
    {
        "canonical": "Augsburg",
        "mascot": "Augsburg",
        "city": "Augsburg",
        "league": "bun",
        "sport": "soccer_germany_bundesliga",
        "color": "#BA3733",

        # Polymarket
        "polymarket_id": 3408,
        "polymarket_abbreviation": "aug",
        "polymarket_name": "FC Augsburg",
        "polymarket_safe_name": "FC Augsburg",
        "polymarket_names": ["FC Augsburg", "Augsburg", "AUG"],

        # Odds API
        "odds_api_key": "soccer_germany_bundesliga",
        "odds_api_name": "Augsburg",
    },
    {
        "canonical": "Bayern Munich",
        "mascot": "Bayern Munich",
        "city": "Munich",
        "league": "bun",
        "sport": "soccer_germany_bundesliga",
        "color": "#DC052D",

        # Polymarket
        "polymarket_id": 3409,
        "polymarket_abbreviation": "fcb",
        "polymarket_name": "FC Bayern München",
        "polymarket_safe_name": "FC Bayern München",
        "polymarket_names": ["FC Bayern München", "Bayern Munich", "FCB"],

        # Odds API
        "odds_api_key": "soccer_germany_bundesliga",
        "odds_api_name": "Bayern Munich",
    },
    {
        "canonical": "Bayer Leverkusen",
        "mascot": "Bayer Leverkusen",
        "city": "Leverkusen",
        "league": "bun",
        "sport": "soccer_germany_bundesliga",
        "color": "#E32221",

        # Polymarket
        "polymarket_id": 3404,
        "polymarket_abbreviation": "lev",
        "polymarket_name": "Bayer 04 Leverkusen",
        "polymarket_safe_name": "Bayer 04 Leverkusen",
        "polymarket_names": ["Bayer 04 Leverkusen", "Bayer Leverkusen", "LEV"],

        # Odds API
        "odds_api_key": "soccer_germany_bundesliga",
        "odds_api_name": "Bayer Leverkusen",
    },
    {
        "canonical": "Borussia Dortmund",
        "mascot": "Borussia Dortmund",
        "city": "Dortmund",
        "league": "bun",
        "sport": "soccer_germany_bundesliga",
        "color": "#E1C500",

        # Polymarket
        "polymarket_id": 3406,
        "polymarket_abbreviation": "bvb",
        "polymarket_name": "BV Borussia 09 Dortmund",
        "polymarket_safe_name": "BV Borussia 09 Dortmund",
        "polymarket_names": ["BV Borussia 09 Dortmund", "Borussia Dortmund", "BVB"],

        # Odds API
        "odds_api_key": "soccer_germany_bundesliga",
        "odds_api_name": "Borussia Dortmund",
    },
    {
        "canonical": "Borussia Monchengladbach",
        "mascot": "Borussia Monchengladbach",
        "city": "Monchengladbach",
        "league": "bun",
        "sport": "soccer_germany_bundesliga",
        "color": "#000000",

        # Polymarket
        "polymarket_id": 3405,
        "polymarket_abbreviation": "bmg",
        "polymarket_name": "Borussia Mönchengladbach",
        "polymarket_safe_name": "Borussia Mönchengladbach",
        "polymarket_names": ["Borussia Mönchengladbach", "Borussia Monchengladbach", "BMG"],

        # Odds API
        "odds_api_key": "soccer_germany_bundesliga",
        "odds_api_name": "Borussia Monchengladbach",
    },
    {
        "canonical": "Eintracht Frankfurt",
        "mascot": "Eintracht Frankfurt",
        "city": "Frankfurt",
        "league": "bun",
        "sport": "soccer_germany_bundesliga",
        "color": "#E1000F",

        # Polymarket
        "polymarket_id": 3407,
        "polymarket_abbreviation": "fra",
        "polymarket_name": "Eintracht Frankfurt",
        "polymarket_safe_name": "Eintracht Frankfurt",
        "polymarket_names": ["Eintracht Frankfurt", "FRA"],

        # Odds API
        "odds_api_key": "soccer_germany_bundesliga",
        "odds_api_name": "Eintracht Frankfurt",
    },
    {
        "canonical": "Freiburg",
        "mascot": "Freiburg",
        "city": "Freiburg",
        "league": "bun",
        "sport": "soccer_germany_bundesliga",
        "color": "#f77729",

        # Polymarket
        "polymarket_id": 3416,
        "polymarket_abbreviation": "scf",
        "polymarket_name": "SC Freiburg",
        "polymarket_safe_name": "SC Freiburg",
        "polymarket_names": ["SC Freiburg", "Freiburg", "SCF"],

        # Odds API
        "odds_api_key": "soccer_germany_bundesliga",
        "odds_api_name": "SC Freiburg",
    },
    {
        "canonical": "Hamburger SV",
        "mascot": "Hamburger SV",
        "city": "Hamburg",
        "league": "bun",
        "sport": "soccer_germany_bundesliga",
        "color": "#0A3F86",

        # Polymarket
        "polymarket_id": 3410,
        "polymarket_abbreviation": "hsv",
        "polymarket_name": "Hamburger SV",
        "polymarket_safe_name": "Hamburger SV",
        "polymarket_names": ["Hamburger SV", "HSV"],

        # Odds API
        "odds_api_key": "soccer_germany_bundesliga",
        "odds_api_name": "Hamburger SV",
    },
    {
        "canonical": "Heidenheim",
        "mascot": "Heidenheim",
        "city": "Heidenheim",
        "league": "bun",
        "sport": "soccer_germany_bundesliga",
        "color": "#E2001A",

        # Polymarket
        "polymarket_id": 3418,
        "polymarket_abbreviation": "hei",
        "polymarket_name": "1. FC Heidenheim 1846",
        "polymarket_safe_name": "FC Heidenheim 1846",
        "polymarket_names": ["1. FC Heidenheim 1846", "FC Heidenheim 1846", "1. FC Heidenheim", "Heidenheim", "HEI"],

        # Odds API
        "odds_api_key": "soccer_germany_bundesliga",
        "odds_api_name": "1. FC Heidenheim",
    },
    {
        "canonical": "Hoffenheim",
        "mascot": "Hoffenheim",
        "city": "Sinsheim",
        "league": "bun",
        "sport": "soccer_germany_bundesliga",
        "color": "#1961B5",

        # Polymarket
        "polymarket_id": 3412,
        "polymarket_abbreviation": "hof",
        "polymarket_name": "TSG 1899 Hoffenheim",
        "polymarket_safe_name": "TSG 1899 Hoffenheim",
        "polymarket_names": ["TSG 1899 Hoffenheim", "TSG Hoffenheim", "Hoffenheim", "HOF"],

        # Odds API
        "odds_api_key": "soccer_germany_bundesliga",
        "odds_api_name": "TSG Hoffenheim",
    },
    {
        "canonical": "Koln",
        "mascot": "Koln",
        "city": "Cologne",
        "league": "bun",
        "sport": "soccer_germany_bundesliga",
        "color": "#EB1722",

        # Polymarket
        "polymarket_id": 3403,
        "polymarket_abbreviation": "koe",
        "polymarket_name": "1. FC Köln",
        "polymarket_safe_name": "FC Köln",
        "polymarket_names": ["1. FC Köln", "FC Köln", "Koln", "KOE"],

        # Odds API
        "odds_api_key": "soccer_germany_bundesliga",
        "odds_api_name": "1. FC Köln",
    },
    {
        "canonical": "Mainz 05",
        "mascot": "Mainz 05",
        "city": "Mainz",
        "league": "bun",
        "sport": "soccer_germany_bundesliga",
        "color": "#C3141E",

        # Polymarket
        "polymarket_id": 3402,
        "polymarket_abbreviation": "mai",
        "polymarket_name": "1. FSV Mainz 05",
        "polymarket_safe_name": "FSV Mainz 05",
        "polymarket_names": ["1. FSV Mainz 05", "FSV Mainz 05", "Mainz 05", "MAI"],

        # Odds API
        "odds_api_key": "soccer_germany_bundesliga",
        "odds_api_name": "FSV Mainz 05",
    },
    {
        "canonical": "RB Leipzig",
        "mascot": "RB Leipzig",
        "city": "Leipzig",
        "league": "bun",
        "sport": "soccer_germany_bundesliga",
        "color": "#DD013F",

        # Polymarket
        "polymarket_id": 3415,
        "polymarket_abbreviation": "rbl",
        "polymarket_name": "RB Leipzig",
        "polymarket_safe_name": "RB Leipzig",
        "polymarket_names": ["RB Leipzig", "RBL"],

        # Odds API
        "odds_api_key": "soccer_germany_bundesliga",
        "odds_api_name": "RB Leipzig",
    },
    {
        "canonical": "St. Pauli",
        "mascot": "St. Pauli",
        "city": "Hamburg",
        "league": "bun",
        "sport": "soccer_germany_bundesliga",
        "color": "#624839",

        # Polymarket
        "polymarket_id": 3419,
        "polymarket_abbreviation": "stp",
        "polymarket_name": "FC St. Pauli 1910",
        "polymarket_safe_name": "FC St. Pauli 1910",
        "polymarket_names": ["FC St. Pauli 1910", "FC St. Pauli", "St. Pauli", "STP"],

        # Odds API
        "odds_api_key": "soccer_germany_bundesliga",
        "odds_api_name": "FC St. Pauli",
    },
    {
        "canonical": "Stuttgart",
        "mascot": "Stuttgart",
        "city": "Stuttgart",
        "league": "bun",
        "sport": "soccer_germany_bundesliga",
        "color": "#E32219",

        # Polymarket
        "polymarket_id": 3413,
        "polymarket_abbreviation": "stu",
        "polymarket_name": "VfB Stuttgart",
        "polymarket_safe_name": "VfB Stuttgart",
        "polymarket_names": ["VfB Stuttgart", "Stuttgart", "STU"],

        # Odds API
        "odds_api_key": "soccer_germany_bundesliga",
        "odds_api_name": "VfB Stuttgart",
    },
    {
        "canonical": "Union Berlin",
        "mascot": "Union Berlin",
        "city": "Berlin",
        "league": "bun",
        "sport": "soccer_germany_bundesliga",
        "color": "#EA1822",

        # Polymarket
        "polymarket_id": 3417,
        "polymarket_abbreviation": "unb",
        "polymarket_name": "1. FC Union Berlin",
        "polymarket_safe_name": "FC Union Berlin",
        "polymarket_names": ["1. FC Union Berlin", "FC Union Berlin", "Union Berlin", "UNB"],

        # Odds API
        "odds_api_key": "soccer_germany_bundesliga",
        "odds_api_name": "Union Berlin",
    },
    {
        "canonical": "Werder Bremen",
        "mascot": "Werder Bremen",
        "city": "Bremen",
        "league": "bun",
        "sport": "soccer_germany_bundesliga",
        "color": "#0D884C",

        # Polymarket
        "polymarket_id": 3411,
        "polymarket_abbreviation": "bre",
        "polymarket_name": "SV Werder Bremen",
        "polymarket_safe_name": "SV Werder Bremen",
        "polymarket_names": ["SV Werder Bremen", "Werder Bremen", "BRE"],

        # Odds API
        "odds_api_key": "soccer_germany_bundesliga",
        "odds_api_name": "Werder Bremen",
    },
    {
        "canonical": "Wolfsburg",
        "mascot": "Wolfsburg",
        "city": "Wolfsburg",
        "league": "bun",
        "sport": "soccer_germany_bundesliga",
        "color": "#65B32E",

        # Polymarket
        "polymarket_id": 3414,
        "polymarket_abbreviation": "wob",
        "polymarket_name": "VfL Wolfsburg",
        "polymarket_safe_name": "VfL Wolfsburg",
        "polymarket_names": ["VfL Wolfsburg", "Wolfsburg", "WOB"],

        # Odds API
        "odds_api_key": "soccer_germany_bundesliga",
        "odds_api_name": "VfL Wolfsburg",
    },

    # =========================================================
    # Serie A
    # =========================================================

    {
        "canonical": "AC Milan",
        "mascot": "AC Milan",
        "city": "Milan",
        "league": "sea",
        "sport": "soccer_italy_serie_a",
        "color": "#ef0000",

        # Polymarket
        "polymarket_id": 3423,
        "polymarket_abbreviation": "mil",
        "polymarket_name": "AC Milan",
        "polymarket_safe_name": "AC Milan",
        "polymarket_names": ["AC Milan", "MIL"],

        # Odds API
        "odds_api_key": "soccer_italy_serie_a",
        "odds_api_name": "AC Milan",
    },
    {
        "canonical": "AS Roma",
        "mascot": "AS Roma",
        "city": "Rome",
        "league": "sea",
        "sport": "soccer_italy_serie_a",
        "color": "#8E1F2F",

        # Polymarket
        "polymarket_id": 3420,
        "polymarket_abbreviation": "rom",
        "polymarket_name": "AS Roma",
        "polymarket_safe_name": "AS Roma",
        "polymarket_names": ["AS Roma", "ROM"],

        # Odds API
        "odds_api_key": "soccer_italy_serie_a",
        "odds_api_name": "AS Roma",
    },
    {
        "canonical": "Atalanta",
        "mascot": "Atalanta",
        "city": "Bergamo",
        "league": "sea",
        "sport": "soccer_italy_serie_a",
        "color": "#1E71B8",

        # Polymarket
        "polymarket_id": 3425,
        "polymarket_abbreviation": "ata",
        "polymarket_name": "Atalanta BC",
        "polymarket_safe_name": "Atalanta BC",
        "polymarket_names": ["Atalanta BC", "Atalanta", "ATA"],

        # Odds API
        "odds_api_key": "soccer_italy_serie_a",
        "odds_api_name": "Atalanta BC",
    },
    {
        "canonical": "Bologna",
        "mascot": "Bologna",
        "city": "Bologna",
        "league": "sea",
        "sport": "soccer_italy_serie_a",
        "color": "#A21C26",

        # Polymarket
        "polymarket_id": 3426,
        "polymarket_abbreviation": "bol",
        "polymarket_name": "Bologna FC 1909",
        "polymarket_safe_name": "Bologna FC 1909",
        "polymarket_names": ["Bologna FC 1909", "Bologna", "BOL"],

        # Odds API
        "odds_api_key": "soccer_italy_serie_a",
        "odds_api_name": "Bologna",
    },
    {
        "canonical": "Cagliari",
        "mascot": "Cagliari",
        "city": "Cagliari",
        "league": "sea",
        "sport": "soccer_italy_serie_a",
        "color": "#002350",

        # Polymarket
        "polymarket_id": 3434,
        "polymarket_abbreviation": "cag",
        "polymarket_name": "Cagliari Calcio",
        "polymarket_safe_name": "Cagliari Calcio",
        "polymarket_names": ["Cagliari Calcio", "Cagliari", "CAG"],

        # Odds API
        "odds_api_key": "soccer_italy_serie_a",
        "odds_api_name": "Cagliari",
    },
    {
        "canonical": "Como",
        "mascot": "Como",
        "city": "Como",
        "league": "sea",
        "sport": "soccer_italy_serie_a",
        "color": "#114169",

        # Polymarket
        "polymarket_id": 3439,
        "polymarket_abbreviation": "com",
        "polymarket_name": "Como 1907",
        "polymarket_safe_name": "Como 1907",
        "polymarket_names": ["Como 1907", "Como", "COM"],

        # Odds API
        "odds_api_key": "soccer_italy_serie_a",
        "odds_api_name": "Como",
    },
    {
        "canonical": "Cremonese",
        "mascot": "Cremonese",
        "city": "Cremona",
        "league": "sea",
        "sport": "soccer_italy_serie_a",
        "color": "#EB1722",

        # Polymarket
        "polymarket_id": 3437,
        "polymarket_abbreviation": "cre",
        "polymarket_name": "US Cremonese",
        "polymarket_safe_name": "US Cremonese",
        "polymarket_names": ["US Cremonese", "Cremonese", "CRE"],

        # Odds API
        "odds_api_key": "soccer_italy_serie_a",
        "odds_api_name": "Cremonese",
    },
    {
        "canonical": "Fiorentina",
        "mascot": "Fiorentina",
        "city": "Florence",
        "league": "sea",
        "sport": "soccer_italy_serie_a",
        "color": "#482E92",

        # Polymarket
        "polymarket_id": 3424,
        "polymarket_abbreviation": "fio",
        "polymarket_name": "ACF Fiorentina",
        "polymarket_safe_name": "ACF Fiorentina",
        "polymarket_names": ["ACF Fiorentina", "Fiorentina", "FIO"],

        # Odds API
        "odds_api_key": "soccer_italy_serie_a",
        "odds_api_name": "Fiorentina",
    },
    {
        "canonical": "Genoa",
        "mascot": "Genoa",
        "city": "Genoa",
        "league": "sea",
        "sport": "soccer_italy_serie_a",
        "color": "#AD1919",

        # Polymarket
        "polymarket_id": 3428,
        "polymarket_abbreviation": "gen",
        "polymarket_name": "Genoa CFC",
        "polymarket_safe_name": "Genoa CFC",
        "polymarket_names": ["Genoa CFC", "Genoa", "GEN"],

        # Odds API
        "odds_api_key": "soccer_italy_serie_a",
        "odds_api_name": "Genoa",
    },
    {
        "canonical": "Hellas Verona",
        "mascot": "Hellas Verona",
        "city": "Verona",
        "league": "sea",
        "sport": "soccer_italy_serie_a",
        "color": "#005395",

        # Polymarket
        "polymarket_id": 3429,
        "polymarket_abbreviation": "ver",
        "polymarket_name": "Hellas Verona FC",
        "polymarket_safe_name": "Hellas Verona",
        "polymarket_names": ["Hellas Verona FC", "Hellas Verona", "VER"],

        # Odds API
        "odds_api_key": "soccer_italy_serie_a",
        "odds_api_name": "Hellas Verona",
    },
    {
        "canonical": "Inter Milan",
        "mascot": "Inter Milan",
        "city": "Milan",
        "league": "sea",
        "sport": "soccer_italy_serie_a",
        "color": "#010E80",

        # Polymarket
        "polymarket_id": 3427,
        "polymarket_abbreviation": "int",
        "polymarket_name": "FC Internazionale Milano",
        "polymarket_safe_name": "FC Internazionale Milano",
        "polymarket_names": ["FC Internazionale Milano", "Inter Milan", "Internazionale", "INT"],

        # Odds API
        "odds_api_key": "soccer_italy_serie_a",
        "odds_api_name": "Inter Milan",
    },
    {
        "canonical": "Juventus",
        "mascot": "Juventus",
        "city": "Turin",
        "league": "sea",
        "sport": "soccer_italy_serie_a",
        "color": "#000000",

        # Polymarket
        "polymarket_id": 3421,
        "polymarket_abbreviation": "juv",
        "polymarket_name": "Juventus FC",
        "polymarket_safe_name": "Juventus",
        "polymarket_names": ["Juventus FC", "Juventus", "JUV"],

        # Odds API
        "odds_api_key": "soccer_italy_serie_a",
        "odds_api_name": "Juventus",
    },
    {
        "canonical": "Lazio",
        "mascot": "Lazio",
        "city": "Rome",
        "league": "sea",
        "sport": "soccer_italy_serie_a",
        "color": "#64BBDC",

        # Polymarket
        "polymarket_id": 3422,
        "polymarket_abbreviation": "laz",
        "polymarket_name": "SS Lazio",
        "polymarket_safe_name": "SS Lazio",
        "polymarket_names": ["SS Lazio", "Lazio", "LAZ"],

        # Odds API
        "odds_api_key": "soccer_italy_serie_a",
        "odds_api_name": "Lazio",
    },
    {
        "canonical": "Lecce",
        "mascot": "Lecce",
        "city": "Lecce",
        "league": "sea",
        "sport": "soccer_italy_serie_a",
        "color": "#D7C900",

        # Polymarket
        "polymarket_id": 3438,
        "polymarket_abbreviation": "lec",
        "polymarket_name": "US Lecce",
        "polymarket_safe_name": "US Lecce",
        "polymarket_names": ["US Lecce", "Lecce", "LEC"],

        # Odds API
        "odds_api_key": "soccer_italy_serie_a",
        "odds_api_name": "Lecce",
    },
    {
        "canonical": "Napoli",
        "mascot": "Napoli",
        "city": "Naples",
        "league": "sea",
        "sport": "soccer_italy_serie_a",
        "color": "#12A0D7",

        # Polymarket
        "polymarket_id": 3430,
        "polymarket_abbreviation": "nap",
        "polymarket_name": "SSC Napoli",
        "polymarket_safe_name": "SSC Napoli",
        "polymarket_names": ["SSC Napoli", "Napoli", "NAP"],

        # Odds API
        "odds_api_key": "soccer_italy_serie_a",
        "odds_api_name": "Napoli",
    },
    {
        "canonical": "Parma",
        "mascot": "Parma",
        "city": "Parma",
        "league": "sea",
        "sport": "soccer_italy_serie_a",
        "color": "#1B4094",

        # Polymarket
        "polymarket_id": 3436,
        "polymarket_abbreviation": "par",
        "polymarket_name": "Parma Calcio 1913",
        "polymarket_safe_name": "Parma Calcio 1913",
        "polymarket_names": ["Parma Calcio 1913", "Parma", "PAR"],

        # Odds API
        "odds_api_key": "soccer_italy_serie_a",
        "odds_api_name": "Parma",
    },
    {
        "canonical": "Pisa",
        "mascot": "Pisa",
        "city": "Pisa",
        "league": "sea",
        "sport": "soccer_italy_serie_a",
        "color": "#0072B4",

        # Polymarket
        "polymarket_id": 3435,
        "polymarket_abbreviation": "pis",
        "polymarket_name": "Pisa SC",
        "polymarket_safe_name": "Pisa",
        "polymarket_names": ["Pisa SC", "Pisa", "PIS"],

        # Odds API
        "odds_api_key": "soccer_italy_serie_a",
        "odds_api_name": "Pisa",
    },
    {
        "canonical": "Sassuolo",
        "mascot": "Sassuolo",
        "city": "Sassuolo",
        "league": "sea",
        "sport": "soccer_italy_serie_a",
        "color": "#1EA351",

        # Polymarket
        "polymarket_id": 3433,
        "polymarket_abbreviation": "sas",
        "polymarket_name": "US Sassuolo Calcio",
        "polymarket_safe_name": "US Sassuolo Calcio",
        "polymarket_names": ["US Sassuolo Calcio", "Sassuolo", "SAS"],

        # Odds API
        "odds_api_key": "soccer_italy_serie_a",
        "odds_api_name": "Sassuolo",
    },
    {
        "canonical": "Torino",
        "mascot": "Torino",
        "city": "Turin",
        "league": "sea",
        "sport": "soccer_italy_serie_a",
        "color": "#8A1E03",

        # Polymarket
        "polymarket_id": 3431,
        "polymarket_abbreviation": "tor",
        "polymarket_name": "Torino FC",
        "polymarket_safe_name": "Torino",
        "polymarket_names": ["Torino FC", "Torino", "TOR"],

        # Odds API
        "odds_api_key": "soccer_italy_serie_a",
        "odds_api_name": "Torino",
    },
    {
        "canonical": "Udinese",
        "mascot": "Udinese",
        "city": "Udine",
        "league": "sea",
        "sport": "soccer_italy_serie_a",
        "color": "#000000",

        # Polymarket
        "polymarket_id": 3432,
        "polymarket_abbreviation": "udi",
        "polymarket_name": "Udinese Calcio",
        "polymarket_safe_name": "Udinese Calcio",
        "polymarket_names": ["Udinese Calcio", "Udinese", "UDI"],

        # Odds API
        "odds_api_key": "soccer_italy_serie_a",
        "odds_api_name": "Udinese",
    },

    # =========================================================
    # UCL
    # =========================================================

    {
        "canonical": "AFC Ajax",
        "mascot": "AFC Ajax",
        "city": "Amsterdam",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#D2122E",

        # Polymarket
        "polymarket_id": 2738,
        "polymarket_abbreviation": "aja",
        "polymarket_name": "AFC Ajax",
        "polymarket_safe_name": "Ajax",
        "polymarket_names": ["AFC Ajax", "Ajax", "AJA"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Ajax",
    },
    {
        "canonical": "Arsenal",
        "mascot": "Arsenal",
        "city": "London",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#EF0007",

        # Polymarket
        "polymarket_id": 2719,
        "polymarket_abbreviation": "ars",
        "polymarket_name": "Arsenal FC",
        "polymarket_safe_name": "Arsenal",
        "polymarket_names": ["Arsenal FC", "Arsenal", "ARS"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Arsenal",
    },
    {
        "canonical": "AS Monaco",
        "mascot": "AS Monaco",
        "city": "Monaco",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#E51B22",

        # Polymarket
        "polymarket_id": 2740,
        "polymarket_abbreviation": "asm",
        "polymarket_name": "AS Monaco FC",
        "polymarket_safe_name": "AS Monaco",
        "polymarket_names": ["AS Monaco FC", "AS Monaco", "ASM"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "AS Monaco",
    },
    {
        "canonical": "Atalanta",
        "mascot": "Atalanta",
        "city": "Bergamo",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#2D5CAE",

        # Polymarket
        "polymarket_id": 2811,
        "polymarket_abbreviation": "ata",
        "polymarket_name": "Atalanta BC",
        "polymarket_safe_name": "Atalanta BC",
        "polymarket_names": ["Atalanta BC", "Atalanta", "ATA"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Atalanta BC",
    },
    {
        "canonical": "Athletic Club",
        "mascot": "Athletic Club",
        "city": "Bilbao",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#EC1412",

        # Polymarket
        "polymarket_id": 2807,
        "polymarket_abbreviation": "ath",
        "polymarket_name": "Athletic Club",
        "polymarket_safe_name": "Athletic Club",
        "polymarket_names": ["Athletic Club", "Athletic Bilbao", "ATH"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Athletic Bilbao",
    },
    {
        "canonical": "Atletico Madrid",
        "mascot": "Atletico Madrid",
        "city": "Madrid",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#CB3524",

        # Polymarket
        "polymarket_id": 2745,
        "polymarket_abbreviation": "atm",
        "polymarket_name": "Club Atlético de Madrid",
        "polymarket_safe_name": "Club Atlético de Madrid",
        "polymarket_names": ["Club Atlético de Madrid", "Atlético Madrid", "Atletico Madrid", "ATM"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Atlético Madrid",
    },
    {
        "canonical": "Barcelona",
        "mascot": "Barcelona",
        "city": "Barcelona",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#A50044",

        # Polymarket
        "polymarket_id": 2750,
        "polymarket_abbreviation": "fcb",
        "polymarket_name": "FC Barcelona",
        "polymarket_safe_name": "FC Barcelona",
        "polymarket_names": ["FC Barcelona", "Barcelona", "FCB"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Barcelona",
    },
    {
        "canonical": "Bayer Leverkusen",
        "mascot": "Bayer Leverkusen",
        "city": "Leverkusen",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#E32221",

        # Polymarket
        "polymarket_id": 2728,
        "polymarket_abbreviation": "lev",
        "polymarket_name": "Bayer 04 Leverkusen",
        "polymarket_safe_name": "Bayer 04 Leverkusen",
        "polymarket_names": ["Bayer 04 Leverkusen", "Bayer Leverkusen", "LEV"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Bayer Leverkusen",
    },
    {
        "canonical": "Bayern Munich",
        "mascot": "Bayern Munich",
        "city": "Munich",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#DC052D",

        # Polymarket
        "polymarket_id": 2732,
        "polymarket_abbreviation": "bay",
        "polymarket_name": "FC Bayern München",
        "polymarket_safe_name": "FC Bayern München",
        "polymarket_names": ["FC Bayern München", "Bayern Munich", "FC Bayern Munich", "BAY"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Bayern Munich",
    },
    {
        "canonical": "Benfica",
        "mascot": "Benfica",
        "city": "Lisbon",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#CC0000",

        # Polymarket
        "polymarket_id": 2799,
        "polymarket_abbreviation": "ben",
        "polymarket_name": "Sport Lisboa e Benfica",
        "polymarket_safe_name": "Sport Lisboa e Benfica",
        "polymarket_names": ["Sport Lisboa e Benfica", "Benfica", "BEN"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Benfica",
    },
    {
        "canonical": "Bodo/Glimt",
        "mascot": "Bodo/Glimt",
        "city": "Bodo",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#8B7500",

        # Polymarket
        "polymarket_id": 2944,
        "polymarket_abbreviation": "bog",
        "polymarket_name": "FK Bodø/Glimt",
        "polymarket_safe_name": "FK Bodø/Glimt",
        "polymarket_names": ["FK Bodø/Glimt", "Bodø/Glimt", "Bodo/Glimt", "BOG"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Bodø/Glimt",
    },
    {
        "canonical": "Borussia Dortmund",
        "mascot": "Borussia Dortmund",
        "city": "Dortmund",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#867700",

        # Polymarket
        "polymarket_id": 2730,
        "polymarket_abbreviation": "bvb",
        "polymarket_name": "BV Borussia 09 Dortmund",
        "polymarket_safe_name": "BV Borussia 09 Dortmund",
        "polymarket_names": ["BV Borussia 09 Dortmund", "Borussia Dortmund", "BVB"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Borussia Dortmund",
    },
    {
        "canonical": "Breiðablik",
        "mascot": "Breiðablik",
        "city": "Kópavogur",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#006A2E",

        # Polymarket
        "polymarket_id": 2893,
        "polymarket_abbreviation": "bre",
        "polymarket_name": "UMF Breiðablik",
        "polymarket_safe_name": "UMF Breiðablik",
        "polymarket_names": ["UMF Breiðablik", "Breiðablik", "BRE"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Breiðablik",
    },
    {
        "canonical": "Budućnost Podgorica",
        "mascot": "Budućnost Podgorica",
        "city": "Podgorica",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#003087",

        # Polymarket
        "polymarket_id": 2839,
        "polymarket_abbreviation": "bud",
        "polymarket_name": "FK Budućnost Podgorica",
        "polymarket_safe_name": "FK Budućnost Podgorica",
        "polymarket_names": ["FK Budućnost Podgorica", "Budućnost Podgorica", "BUD"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Budućnost Podgorica",
    },
    {
        "canonical": "Celtic",
        "mascot": "Celtic",
        "city": "Glasgow",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#00843D",

        # Polymarket
        "polymarket_id": 2744,
        "polymarket_abbreviation": "cel",
        "polymarket_name": "Celtic FC",
        "polymarket_safe_name": "Celtic",
        "polymarket_names": ["Celtic FC", "Celtic", "CEL"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Celtic",
    },
    {
        "canonical": "Chelsea",
        "mascot": "Chelsea",
        "city": "London",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#034694",

        # Polymarket
        "polymarket_id": 2721,
        "polymarket_abbreviation": "cfc",
        "polymarket_name": "Chelsea FC",
        "polymarket_safe_name": "Chelsea",
        "polymarket_names": ["Chelsea FC", "Chelsea", "CFC"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Chelsea",
    },
    {
        "canonical": "Club Brugge",
        "mascot": "Club Brugge",
        "city": "Bruges",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#0078BF",

        # Polymarket
        "polymarket_id": 2746,
        "polymarket_abbreviation": "bru",
        "polymarket_name": "Club Brugge KV",
        "polymarket_safe_name": "Club Brugge KV",
        "polymarket_names": ["Club Brugge KV", "Club Brugge", "BRU"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Club Brugge",
    },
    {
        "canonical": "Eintracht Frankfurt",
        "mascot": "Eintracht Frankfurt",
        "city": "Frankfurt",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#E1000F",

        # Polymarket
        "polymarket_id": 2731,
        "polymarket_abbreviation": "fra",
        "polymarket_name": "Eintracht Frankfurt",
        "polymarket_safe_name": "Eintracht Frankfurt",
        "polymarket_names": ["Eintracht Frankfurt", "FRA"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Eintracht Frankfurt",
    },
    {
        "canonical": "FC Basel",
        "mascot": "FC Basel",
        "city": "Basel",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#E62020",

        # Polymarket
        "polymarket_id": 2751,
        "polymarket_abbreviation": "bas",
        "polymarket_name": "FC Basel 1893",
        "polymarket_safe_name": "FC Basel 1893",
        "polymarket_names": ["FC Basel 1893", "FC Basel", "BAS"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "FC Basel",
    },
    {
        "canonical": "FC Copenhagen",
        "mascot": "FC Copenhagen",
        "city": "Copenhagen",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#BF2126",

        # Polymarket
        "polymarket_id": 2833,
        "polymarket_abbreviation": "kob",
        "polymarket_name": "FC København",
        "polymarket_safe_name": "FC København",
        "polymarket_names": ["FC København", "FC Copenhagen", "KOB"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "FC Copenhagen",
    },
    {
        "canonical": "FC Déifferdeng 03",
        "mascot": "FC Déifferdeng 03",
        "city": "Differdange",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#006A2E",

        # Polymarket
        "polymarket_id": 2829,
        "polymarket_abbreviation": "dif",
        "polymarket_name": "FC Déifferdeng 03",
        "polymarket_safe_name": "FC Déifferdeng 03",
        "polymarket_names": ["FC Déifferdeng 03", "FC Differdange 03", "FC Differdange", "DIF"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "FC Differdange 03",
    },
    {
        "canonical": "FC Drita",
        "mascot": "FC Drita",
        "city": "Gjilan",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#1B2F6B",

        # Polymarket
        "polymarket_id": 2922,
        "polymarket_abbreviation": "dgj",
        "polymarket_name": "FC Drita",
        "polymarket_safe_name": "FC Drita",
        "polymarket_names": ["FC Drita", "DGJ"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "FC Drita",
    },
    {
        "canonical": "FC Iberia 1999",
        "mascot": "FC Iberia 1999",
        "city": "Tbilisi",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#CC0000",

        # Polymarket
        "polymarket_id": 2933,
        "polymarket_abbreviation": "sab",
        "polymarket_name": "SK Iberia 1999",
        "polymarket_safe_name": "SK Iberia 1999",
        "polymarket_names": ["SK Iberia 1999", "FC Iberia 1999", "SAB"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "FC Iberia 1999",
    },
    {
        "canonical": "FCI Levadia",
        "mascot": "FCI Levadia",
        "city": "Tallinn",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#8B7500",

        # Polymarket
        "polymarket_id": 2753,
        "polymarket_abbreviation": "fcil",
        "polymarket_name": "FCI Levadia",
        "polymarket_safe_name": "FCI Levadia",
        "polymarket_names": ["FCI Levadia", "FCIL"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "FCI Levadia",
    },
    {
        "canonical": "FCSB",
        "mascot": "FCSB",
        "city": "Bucharest",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#EC1412",

        # Polymarket
        "polymarket_id": 2760,
        "polymarket_abbreviation": "ste",
        "polymarket_name": "FCSB",
        "polymarket_safe_name": "FCSB",
        "polymarket_names": ["FCSB", "STE"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "FCSB",
    },
    {
        "canonical": "Fenerbahçe",
        "mascot": "Fenerbahçe",
        "city": "Istanbul",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#827900",

        # Polymarket
        "polymarket_id": 2763,
        "polymarket_abbreviation": "fen",
        "polymarket_name": "Fenerbahçe SK",
        "polymarket_safe_name": "Fenerbahçe SK",
        "polymarket_names": ["Fenerbahçe SK", "Fenerbahçe", "Fenerbahce", "FEN"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Fenerbahce",
    },
    {
        "canonical": "Ferencváros",
        "mascot": "Ferencváros",
        "city": "Budapest",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#006A2E",

        # Polymarket
        "polymarket_id": 2837,
        "polymarket_abbreviation": "ftc",
        "polymarket_name": "Ferencvárosi TC",
        "polymarket_safe_name": "Ferencvárosi TC",
        "polymarket_names": ["Ferencvárosi TC", "Ferencváros TC", "Ferencváros", "FTC"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Ferencváros TC",
    },
    {
        "canonical": "FK Crvena zvezda",
        "mascot": "FK Crvena zvezda",
        "city": "Belgrade",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#EB1623",

        # Polymarket
        "polymarket_id": 2840,
        "polymarket_abbreviation": "crv",
        "polymarket_name": "FK Crvena zvezda",
        "polymarket_safe_name": "FK Crvena zvezda",
        "polymarket_names": ["FK Crvena zvezda", "Red Star Belgrade", "CRV"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Red Star Belgrade",
    },
    {
        "canonical": "FK Dynama-Minsk",
        "mascot": "FK Dynama-Minsk",
        "city": "Minsk",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#0038A8",

        # Polymarket
        "polymarket_id": 2841,
        "polymarket_abbreviation": "fkdy",
        "polymarket_name": "FK Dynama-Minsk",
        "polymarket_safe_name": "FK Dynama-Minsk",
        "polymarket_names": ["FK Dynama-Minsk", "FC Dinamo Minsk", "FKDY"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "FC Dinamo Minsk",
    },
    {
        "canonical": "FK Milsami Orhei",
        "mascot": "FK Milsami Orhei",
        "city": "Orhei",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#907300",

        # Polymarket
        "polymarket_id": 2755,
        "polymarket_abbreviation": "mil",
        "polymarket_name": "FC Milsami Orhei",
        "polymarket_safe_name": "FC Milsami Orhei",
        "polymarket_names": ["FC Milsami Orhei", "Milsami Orhei", "MIL"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Milsami Orhei",
    },
    {
        "canonical": "FK Žalgiris",
        "mascot": "FK Žalgiris",
        "city": "Vilnius",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#006A2E",

        # Polymarket
        "polymarket_id": 2762,
        "polymarket_abbreviation": "zal",
        "polymarket_name": "FK Žalgiris Vilnius",
        "polymarket_safe_name": "FK Žalgiris Vilnius",
        "polymarket_names": ["FK Žalgiris Vilnius", "FK Žalgiris", "ZAL"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "FK Žalgiris",
    },
    {
        "canonical": "Galatasaray",
        "mascot": "Galatasaray",
        "city": "Istanbul",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#A90432",

        # Polymarket
        "polymarket_id": 2775,
        "polymarket_abbreviation": "gal",
        "polymarket_name": "Galatasaray SK",
        "polymarket_safe_name": "Galatasaray SK",
        "polymarket_names": ["Galatasaray SK", "Galatasaray", "GAL"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Galatasaray",
    },
    {
        "canonical": "HNK Rijeka",
        "mascot": "HNK Rijeka",
        "city": "Rijeka",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#003366",

        # Polymarket
        "polymarket_id": 2854,
        "polymarket_abbreviation": "rij",
        "polymarket_name": "HNK Rijeka",
        "polymarket_safe_name": "HNK Rijeka",
        "polymarket_names": ["HNK Rijeka", "Rijeka", "RIJ"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "HNK Rijeka",
    },
    {
        "canonical": "HŠK Zrinjski Mostar",
        "mascot": "HŠK Zrinjski Mostar",
        "city": "Mostar",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#CC0000",

        # Polymarket
        "polymarket_id": 2855,
        "polymarket_abbreviation": "zri",
        "polymarket_name": "HŠK Zrinjski Mostar",
        "polymarket_safe_name": "HŠK Zrinjski Mostar",
        "polymarket_names": ["HŠK Zrinjski Mostar", "Zrinjski Mostar", "ZRI"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "HŠK Zrinjski Mostar",
    },
    {
        "canonical": "Inter Milan",
        "mascot": "Inter Milan",
        "city": "Milan",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#010E80",

        # Polymarket
        "polymarket_id": 2813,
        "polymarket_abbreviation": "int",
        "polymarket_name": "FC Internazionale Milano",
        "polymarket_safe_name": "FC Internazionale Milano",
        "polymarket_names": ["FC Internazionale Milano", "Inter Milan", "Internazionale", "INT"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Inter Milan",
    },
    {
        "canonical": "Juventus",
        "mascot": "Juventus",
        "city": "Turin",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#000000",

        # Polymarket
        "polymarket_id": 2779,
        "polymarket_abbreviation": "juv",
        "polymarket_name": "Juventus FC",
        "polymarket_safe_name": "Juventus",
        "polymarket_names": ["Juventus FC", "Juventus", "JUV"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Juventus",
    },
    {
        "canonical": "KF Víkingur",
        "mascot": "KF Víkingur",
        "city": "Reykjavik",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#003087",

        # Polymarket
        "polymarket_id": 2859,
        "polymarket_abbreviation": "vik",
        "polymarket_name": "KF Víkingur",
        "polymarket_safe_name": "KF Víkingur",
        "polymarket_names": ["KF Víkingur", "Víkingur Reykjavík", "VIK"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Víkingur Reykjavík",
    },
    {
        "canonical": "Lincoln Red Imps",
        "mascot": "Lincoln Red Imps",
        "city": "Gibraltar",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#CC0000",

        # Polymarket
        "polymarket_id": 2783,
        "polymarket_abbreviation": "lin",
        "polymarket_name": "Lincoln Red Imps FC",
        "polymarket_safe_name": "Lincoln Red Imps",
        "polymarket_names": ["Lincoln Red Imps FC", "Lincoln Red Imps", "LIN"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Lincoln Red Imps FC",
    },
    {
        "canonical": "Linfield",
        "mascot": "Linfield",
        "city": "Belfast",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#003CB5",

        # Polymarket
        "polymarket_id": 2862,
        "polymarket_abbreviation": "linf",
        "polymarket_name": "Linfield FC",
        "polymarket_safe_name": "Linfield",
        "polymarket_names": ["Linfield FC", "Linfield", "LINF"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Linfield",
    },
    {
        "canonical": "Liverpool",
        "mascot": "Liverpool",
        "city": "Liverpool",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#C8102E",

        # Polymarket
        "polymarket_id": 2723,
        "polymarket_abbreviation": "liv",
        "polymarket_name": "Liverpool FC",
        "polymarket_safe_name": "Liverpool",
        "polymarket_names": ["Liverpool FC", "Liverpool", "LIV"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Liverpool",
    },
    {
        "canonical": "Maccabi Tel Aviv",
        "mascot": "Maccabi Tel Aviv",
        "city": "Tel Aviv",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#8B7500",

        # Polymarket
        "polymarket_id": 2784,
        "polymarket_abbreviation": "mta",
        "polymarket_name": "MH Maccabi Tel Aviv",
        "polymarket_safe_name": "MH Maccabi Tel Aviv",
        "polymarket_names": ["MH Maccabi Tel Aviv", "Maccabi Tel Aviv", "MTA"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Maccabi Tel Aviv",
    },
    {
        "canonical": "Manchester City",
        "mascot": "Manchester City",
        "city": "Manchester",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#2B7BBB",

        # Polymarket
        "polymarket_id": 2724,
        "polymarket_abbreviation": "mnc",
        "polymarket_name": "Manchester City FC",
        "polymarket_safe_name": "Manchester City",
        "polymarket_names": ["Manchester City FC", "Manchester City", "MNC"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Manchester City",
    },
    {
        "canonical": "Napoli",
        "mascot": "Napoli",
        "city": "Naples",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#087AC5",

        # Polymarket
        "polymarket_id": 2814,
        "polymarket_abbreviation": "nap",
        "polymarket_name": "SSC Napoli",
        "polymarket_safe_name": "SSC Napoli",
        "polymarket_names": ["SSC Napoli", "Napoli", "NAP"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Napoli",
    },
    {
        "canonical": "Newcastle United",
        "mascot": "Newcastle United",
        "city": "Newcastle",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#241F20",

        # Polymarket
        "polymarket_id": 2726,
        "polymarket_abbreviation": "new",
        "polymarket_name": "Newcastle United FC",
        "polymarket_safe_name": "Newcastle United",
        "polymarket_names": ["Newcastle United FC", "Newcastle United", "NEW"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Newcastle United",
    },
    {
        "canonical": "NK Olimpija Ljubljana",
        "mascot": "NK Olimpija Ljubljana",
        "city": "Ljubljana",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#006A2E",

        # Polymarket
        "polymarket_id": 2890,
        "polymarket_abbreviation": "oli",
        "polymarket_name": "NK Olimpija Ljubljana",
        "polymarket_safe_name": "NK Olimpija Ljubljana",
        "polymarket_names": ["NK Olimpija Ljubljana", "Olimpija Ljubljana", "OLI"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "NK Olimpija Ljubljana",
    },
    {
        "canonical": "Olympiakos",
        "mascot": "Olympiakos",
        "city": "Piraeus",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#D0061F",

        # Polymarket
        "polymarket_id": 2789,
        "polymarket_abbreviation": "oly",
        "polymarket_name": "Olympiakós SFP",
        "polymarket_safe_name": "Olympiakós SFP",
        "polymarket_names": ["Olympiakós SFP", "Olympiakos Piraeus", "Olympiakos", "OLY"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Olympiakos Piraeus",
    },
    {
        "canonical": "Panathinaikos",
        "mascot": "Panathinaikos",
        "city": "Athens",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#00793F",

        # Polymarket
        "polymarket_id": 2790,
        "polymarket_abbreviation": "pao",
        "polymarket_name": "Panathinaikós AO",
        "polymarket_safe_name": "Panathinaikós AO",
        "polymarket_names": ["Panathinaikós AO", "Panathinaikos FC", "Panathinaikos", "PAO"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Panathinaikos FC",
    },
    {
        "canonical": "Paris Saint-Germain",
        "mascot": "Paris Saint-Germain",
        "city": "Paris",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#003370",

        # Polymarket
        "polymarket_id": 2791,
        "polymarket_abbreviation": "psg",
        "polymarket_name": "Paris Saint-Germain FC",
        "polymarket_safe_name": "Paris Saint-Germain",
        "polymarket_names": ["Paris Saint-Germain FC", "Paris Saint-Germain", "Paris Saint Germain", "PSG"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Paris Saint Germain",
    },
    {
        "canonical": "PSV Eindhoven",
        "mascot": "PSV Eindhoven",
        "city": "Eindhoven",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#E3000F",

        # Polymarket
        "polymarket_id": 2794,
        "polymarket_abbreviation": "psv",
        "polymarket_name": "PSV",
        "polymarket_safe_name": "PSV",
        "polymarket_names": ["PSV", "PSV Eindhoven"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "PSV Eindhoven",
    },
    {
        "canonical": "Qarabag",
        "mascot": "Qarabag",
        "city": "Baku",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#A26C10",

        # Polymarket
        "polymarket_id": 2795,
        "polymarket_abbreviation": "qar",
        "polymarket_name": "Qarabağ Ağdam FK",
        "polymarket_safe_name": "Qarabağ Ağdam FK",
        "polymarket_names": ["Qarabağ Ağdam FK", "Qarabağ FK", "Qarabag", "QAR"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Qarabağ FK",
    },
    {
        "canonical": "Qairat",
        "mascot": "Qairat",
        "city": "Almaty",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#8F7409",

        # Polymarket
        "polymarket_id": 2842,
        "polymarket_abbreviation": "kai",
        "polymarket_name": "Qairat FK",
        "polymarket_safe_name": "Qairat FK",
        "polymarket_names": ["Qairat FK", "FC Kairat", "Qairat", "KAI"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "FC Kairat",
    },
    {
        "canonical": "Rangers",
        "mascot": "Rangers",
        "city": "Glasgow",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#1B458F",

        # Polymarket
        "polymarket_id": 2919,
        "polymarket_abbreviation": "ran",
        "polymarket_name": "Rangers FC",
        "polymarket_safe_name": "Rangers",
        "polymarket_names": ["Rangers FC", "Rangers", "RAN"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Rangers FC",
    },
    {
        "canonical": "Real Madrid",
        "mascot": "Real Madrid",
        "city": "Madrid",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#997001",

        # Polymarket
        "polymarket_id": 2796,
        "polymarket_abbreviation": "rma",
        "polymarket_name": "Real Madrid CF",
        "polymarket_safe_name": "Real Madrid",
        "polymarket_names": ["Real Madrid CF", "Real Madrid", "RMA"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Real Madrid",
    },
    {
        "canonical": "Servette",
        "mascot": "Servette",
        "city": "Geneva",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#990000",

        # Polymarket
        "polymarket_id": 2942,
        "polymarket_abbreviation": "ser",
        "polymarket_name": "Servette FC",
        "polymarket_safe_name": "Servette",
        "polymarket_names": ["Servette FC", "Servette", "SER"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Servette FC",
    },
    {
        "canonical": "SK Brann",
        "mascot": "SK Brann",
        "city": "Bergen",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#D9001E",

        # Polymarket
        "polymarket_id": 2920,
        "polymarket_abbreviation": "bra",
        "polymarket_name": "SK Brann",
        "polymarket_safe_name": "SK Brann",
        "polymarket_names": ["SK Brann", "BRA"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "SK Brann",
    },
    {
        "canonical": "Slavia Praha",
        "mascot": "Slavia Praha",
        "city": "Prague",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#D7141A",

        # Polymarket
        "polymarket_id": 2907,
        "polymarket_abbreviation": "slp",
        "polymarket_name": "SK Slavia Praha",
        "polymarket_safe_name": "SK Slavia Praha",
        "polymarket_names": ["SK Slavia Praha", "Slavia Praha", "SLP"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Slavia Praha",
    },
    {
        "canonical": "Sporting CP",
        "mascot": "Sporting CP",
        "city": "Lisbon",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#008057",

        # Polymarket
        "polymarket_id": 2800,
        "polymarket_abbreviation": "spo",
        "polymarket_name": "Sporting CP",
        "polymarket_safe_name": "Sporting CP",
        "polymarket_names": ["Sporting CP", "Sporting Lisbon", "SPO"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Sporting Lisbon",
    },
    {
        "canonical": "The New Saints",
        "mascot": "The New Saints",
        "city": "Oswestry",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#008000",

        # Polymarket
        "polymarket_id": 2803,
        "polymarket_abbreviation": "tns",
        "polymarket_name": "The New Saints FC",
        "polymarket_safe_name": "The New Saints",
        "polymarket_names": ["The New Saints FC", "The New Saints", "TNS"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "The New Saints FC",
    },
    {
        "canonical": "Tottenham Hotspur",
        "mascot": "Tottenham Hotspur",
        "city": "London",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#132257",

        # Polymarket
        "polymarket_id": 2727,
        "polymarket_abbreviation": "tot",
        "polymarket_name": "Tottenham Hotspur FC",
        "polymarket_safe_name": "Tottenham Hotspur",
        "polymarket_names": ["Tottenham Hotspur FC", "Tottenham Hotspur", "Tottenham", "TOT"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Tottenham Hotspur",
    },
    {
        "canonical": "Villarreal",
        "mascot": "Villarreal",
        "city": "Villarreal",
        "league": "ucl",
        "sport": "soccer_uefa_champs_league",
        "color": "#8B7600",

        # Polymarket
        "polymarket_id": 2809,
        "polymarket_abbreviation": "vil",
        "polymarket_name": "Villarreal CF",
        "polymarket_safe_name": "Villarreal",
        "polymarket_names": ["Villarreal CF", "Villarreal", "VIL"],

        # Odds API
        "odds_api_key": "soccer_uefa_champs_league",
        "odds_api_name": "Villarreal",
    },

    # =========================================================
    # CBB
    # =========================================================

    {
        "canonical": "Abilene Christian Wildcats",
        "mascot": "Wildcats",
        "city": "Abilene",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#461D7C",

        # Polymarket
        "polymarket_id": 1953,
        "polymarket_abbreviation": "abchr",
        "polymarket_name": "Abilene Christian Wildcats",
        "polymarket_safe_name": "Abilene Christian Wildcats",
        "polymarket_names": ["Abilene Christian Wildcats", "ABCHR"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Abilene Christian Wildcats",
    },
    {
        "canonical": "Air Force Falcons",
        "mascot": "Falcons",
        "city": "Colorado Springs",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#00308F",

        # Polymarket
        "polymarket_id": 1879,
        "polymarket_abbreviation": "airf",
        "polymarket_name": "Air Force Falcons",
        "polymarket_safe_name": "Air Force Falcons",
        "polymarket_names": ["Air Force Falcons", "AIRF"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Air Force Falcons",
    },
    {
        "canonical": "Akron Zips",
        "mascot": "Zips",
        "city": "Akron",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#004080",

        # Polymarket
        "polymarket_id": 1836,
        "polymarket_abbreviation": "akron",
        "polymarket_name": "Akron Zips",
        "polymarket_safe_name": "Akron Zips",
        "polymarket_names": ["Akron Zips", "AKRON"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Akron Zips",
    },
    {
        "canonical": "Alabama A&M Bulldogs",
        "mascot": "Bulldogs",
        "city": "Huntsville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#8D2634",

        # Polymarket
        "polymarket_id": 1966,
        "polymarket_abbreviation": "alaam",
        "polymarket_name": "Alabama A&M Bulldogs",
        "polymarket_safe_name": "Alabama A&M Bulldogs",
        "polymarket_names": ["Alabama A&M Bulldogs", "ALAAM"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Alabama A&M Bulldogs",
    },
    {
        "canonical": "Alabama State Hornets",
        "mascot": "Hornets",
        "city": "Montgomery",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C99700",

        # Polymarket
        "polymarket_id": 1968,
        "polymarket_abbreviation": "alast",
        "polymarket_name": "Alabama State Hornets",
        "polymarket_safe_name": "Alabama State Hornets",
        "polymarket_names": ["Alabama State Hornets", "Alabama St Hornets", "ALAST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Alabama St Hornets",
    },
    {
        "canonical": "American Eagles",
        "mascot": "Eagles",
        "city": "Washington",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#005099",

        # Polymarket
        "polymarket_id": 1922,
        "polymarket_abbreviation": "amercn",
        "polymarket_name": "American Eagles",
        "polymarket_safe_name": "American University Eagles",
        "polymarket_names": ["American Eagles", "American University Eagles", "AMERCN"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "American Eagles",
    },
    {
        "canonical": "Appalachian State Mountaineers",
        "mascot": "Mountaineers",
        "city": "Boone",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#3D3D3D",

        # Polymarket
        "polymarket_id": 1988,
        "polymarket_abbreviation": "applst",
        "polymarket_name": "Appalachian State Mountaineers",
        "polymarket_safe_name": "App State Mountaineers",
        "polymarket_names": ["Appalachian State Mountaineers", "App State Mountaineers", "Appalachian St Mountaineers", "APPLST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Appalachian St Mountaineers",
    },
    {
        "canonical": "Arizona State Sun Devils",
        "mascot": "Sun Devils",
        "city": "Tempe",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#8C1D40",

        # Polymarket
        "polymarket_id": 1912,
        "polymarket_abbreviation": "arzst",
        "polymarket_name": "Arizona State Sun Devils",
        "polymarket_safe_name": "Arizona State Sun Devils",
        "polymarket_names": ["Arizona State Sun Devils", "Arizona St Sun Devils", "ARZST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Arizona St Sun Devils",
    },
    {
        "canonical": "Arizona Wildcats",
        "mascot": "Wildcats",
        "city": "Tucson",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#CC0033",

        # Polymarket
        "polymarket_id": 1904,
        "polymarket_abbreviation": "arz",
        "polymarket_name": "Arizona Wildcats",
        "polymarket_safe_name": "Arizona Wildcats",
        "polymarket_names": ["Arizona Wildcats", "ARZ"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Arizona Wildcats",
    },
    {
        "canonical": "Arkansas Razorbacks",
        "mascot": "Razorbacks",
        "city": "Fayetteville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#9D2235",

        # Polymarket
        "polymarket_id": 1933,
        "polymarket_abbreviation": "ark",
        "polymarket_name": "Arkansas Razorbacks",
        "polymarket_safe_name": "Arkansas Razorbacks",
        "polymarket_names": ["Arkansas Razorbacks", "ARK"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Arkansas Razorbacks",
    },
    {
        "canonical": "Arkansas State Red Wolves",
        "mascot": "Red Wolves",
        "city": "Jonesboro",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#CC092F",

        # Polymarket
        "polymarket_id": 1984,
        "polymarket_abbreviation": "arkst",
        "polymarket_name": "Arkansas State Red Wolves",
        "polymarket_safe_name": "Arkansas State Red Wolves",
        "polymarket_names": ["Arkansas State Red Wolves", "Arkansas St Red Wolves", "ARKST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Arkansas St Red Wolves",
    },
    {
        "canonical": "Auburn Tigers",
        "mascot": "Tigers",
        "city": "Auburn",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#E25F20",

        # Polymarket
        "polymarket_id": 1936,
        "polymarket_abbreviation": "aubrn",
        "polymarket_name": "Auburn Tigers",
        "polymarket_safe_name": "Auburn Tigers",
        "polymarket_names": ["Auburn Tigers", "AUBRN"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Auburn Tigers",
    },
    {
        "canonical": "BYU Cougars",
        "mascot": "Cougars",
        "city": "Provo",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#002E5D",

        # Polymarket
        "polymarket_id": 1993,
        "polymarket_abbreviation": "byu",
        "polymarket_name": "BYU Cougars",
        "polymarket_safe_name": "BYU Cougars",
        "polymarket_names": ["BYU Cougars", "BYU"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "BYU Cougars",
    },
    {
        "canonical": "CSU Bakersfield Roadrunners",
        "mascot": "Roadrunners",
        "city": "Bakersfield",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#004BD1",

        # Polymarket
        "polymarket_id": 2003,
        "polymarket_abbreviation": "csu",
        "polymarket_name": "Bakersfield Roadrunners",
        "polymarket_safe_name": "Cal State Bakersfield Roadrunners",
        "polymarket_names": ["Bakersfield Roadrunners", "Cal State Bakersfield Roadrunners", "CSU Bakersfield Roadrunners", "CSU"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "CSU Bakersfield Roadrunners",
    },
    {
        "canonical": "Ball State Cardinals",
        "mascot": "Cardinals",
        "city": "Muncie",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#CC0000",

        # Polymarket
        "polymarket_id": 1843,
        "polymarket_abbreviation": "ballst",
        "polymarket_name": "Ball State Cardinals",
        "polymarket_safe_name": "Ball State Cardinals",
        "polymarket_names": ["Ball State Cardinals", "BALLST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Ball State Cardinals",
    },
    {
        "canonical": "Belmont Bruins",
        "mascot": "Bruins",
        "city": "Nashville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C8102E",

        # Polymarket
        "polymarket_id": 1890,
        "polymarket_abbreviation": "belm",
        "polymarket_name": "Belmont Bruins",
        "polymarket_safe_name": "Belmont Bruins",
        "polymarket_names": ["Belmont Bruins", "BELM"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Belmont Bruins",
    },
    {
        "canonical": "Bethune-Cookman Wildcats",
        "mascot": "Wildcats",
        "city": "Daytona Beach",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#6F263D",

        # Polymarket
        "polymarket_id": 1851,
        "polymarket_abbreviation": "bcook",
        "polymarket_name": "Bethune-Cookman Wildcats",
        "polymarket_safe_name": "Bethune-Cookman Wildcats",
        "polymarket_names": ["Bethune-Cookman Wildcats", "BCOOK"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Bethune-Cookman Wildcats",
    },
    {
        "canonical": "Boise State Broncos",
        "mascot": "Broncos",
        "city": "Boise",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0033A0",

        # Polymarket
        "polymarket_id": 1873,
        "polymarket_abbreviation": "boise",
        "polymarket_name": "Boise State Broncos",
        "polymarket_safe_name": "Boise State Broncos",
        "polymarket_names": ["Boise State Broncos", "BOISE"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Boise State Broncos",
    },
    {
        "canonical": "Bucknell Bison",
        "mascot": "Bison",
        "city": "Lewisburg",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003865",

        # Polymarket
        "polymarket_id": 1914,
        "polymarket_abbreviation": "buck",
        "polymarket_name": "Bucknell Bison",
        "polymarket_safe_name": "Bucknell Bison",
        "polymarket_names": ["Bucknell Bison", "BUCK"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Bucknell Bison",
    },
    {
        "canonical": "Buffalo Bulls",
        "mascot": "Bulls",
        "city": "Buffalo",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#005BBB",

        # Polymarket
        "polymarket_id": 1838,
        "polymarket_abbreviation": "buf",
        "polymarket_name": "Buffalo Bulls",
        "polymarket_safe_name": "Buffalo Bulls",
        "polymarket_names": ["Buffalo Bulls", "BUF"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Buffalo Bulls",
    },
    {
        "canonical": "California Baptist Lancers",
        "mascot": "Lancers",
        "city": "Riverside",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#A07400",

        # Polymarket
        "polymarket_id": 2010,
        "polymarket_abbreviation": "cabap",
        "polymarket_name": "California Baptist Lancers",
        "polymarket_safe_name": "California Baptist Lancers",
        "polymarket_names": ["California Baptist Lancers", "Cal Baptist Lancers", "CABAP"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Cal Baptist Lancers",
    },
    {
        "canonical": "Canisius Golden Griffins",
        "mascot": "Golden Griffins",
        "city": "Buffalo",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#153A7F",

        # Polymarket
        "polymarket_id": 1831,
        "polymarket_abbreviation": "cans",
        "polymarket_name": "Canisius Golden Griffins",
        "polymarket_safe_name": "Canisius Golden Griffins",
        "polymarket_names": ["Canisius Golden Griffins", "CANS"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Canisius Golden Griffins",
    },
    {
        "canonical": "Central Connecticut Blue Devils",
        "mascot": "Blue Devils",
        "city": "New Britain",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#01529A",

        # Polymarket
        "polymarket_id": 1889,
        "polymarket_abbreviation": "cencon",
        "polymarket_name": "Central Connecticut State Blue Devils",
        "polymarket_safe_name": "Central Connecticut Blue Devils",
        "polymarket_names": ["Central Connecticut State Blue Devils", "Central Connecticut Blue Devils", "Central Connecticut St Blue Devils", "CENCON"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Central Connecticut St Blue Devils",
    },
    {
        "canonical": "Central Michigan Chippewas",
        "mascot": "Chippewas",
        "city": "Mount Pleasant",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#6A0032",

        # Polymarket
        "polymarket_id": 1844,
        "polymarket_abbreviation": "cmich",
        "polymarket_name": "Central Michigan Chippewas",
        "polymarket_safe_name": "Central Michigan Chippewas",
        "polymarket_names": ["Central Michigan Chippewas", "CMICH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Central Michigan Chippewas",
    },
    {
        "canonical": "Chattanooga Mocs",
        "mascot": "Mocs",
        "city": "Chattanooga",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#112E51",

        # Polymarket
        "polymarket_id": 1938,
        "polymarket_abbreviation": "chat",
        "polymarket_name": "Chattanooga Mocs",
        "polymarket_safe_name": "Chattanooga Mocs",
        "polymarket_names": ["Chattanooga Mocs", "CHAT"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Chattanooga Mocs",
    },
    {
        "canonical": "Chicago State Cougars",
        "mascot": "Cougars",
        "city": "Chicago",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#006666",

        # Polymarket
        "polymarket_id": 2007,
        "polymarket_abbreviation": "chist",
        "polymarket_name": "Chicago State Cougars",
        "polymarket_safe_name": "Chicago State Cougars",
        "polymarket_names": ["Chicago State Cougars", "Chicago St Cougars", "CHIST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Chicago St Cougars",
    },
    {
        "canonical": "Clemson Tigers",
        "mascot": "Tigers",
        "city": "Clemson",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#F56733",

        # Polymarket
        "polymarket_id": 1686,
        "polymarket_abbreviation": "clmsn",
        "polymarket_name": "Clemson Tigers",
        "polymarket_safe_name": "Clemson Tigers",
        "polymarket_names": ["Clemson Tigers", "CLMSN"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Clemson Tigers",
    },
    {
        "canonical": "Coastal Carolina Chanticleers",
        "mascot": "Chanticleers",
        "city": "Conway",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#007073",

        # Polymarket
        "polymarket_id": 1740,
        "polymarket_abbreviation": "coast",
        "polymarket_name": "Coastal Carolina Chanticleers",
        "polymarket_safe_name": "Coastal Carolina Chanticleers",
        "polymarket_names": ["Coastal Carolina Chanticleers", "COAST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Coastal Carolina Chanticleers",
    },
    {
        "canonical": "Colorado Buffaloes",
        "mascot": "Buffaloes",
        "city": "Boulder",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#CFB87C",

        # Polymarket
        "polymarket_id": 1907,
        "polymarket_abbreviation": "col",
        "polymarket_name": "Colorado Buffaloes",
        "polymarket_safe_name": "Colorado Buffaloes",
        "polymarket_names": ["Colorado Buffaloes", "COL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Colorado Buffaloes",
    },
    {
        "canonical": "Colorado State Rams",
        "mascot": "Rams",
        "city": "Fort Collins",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#1E4D2B",

        # Polymarket
        "polymarket_id": 1875,
        "polymarket_abbreviation": "colst",
        "polymarket_name": "Colorado State Rams",
        "polymarket_safe_name": "Colorado State Rams",
        "polymarket_names": ["Colorado State Rams", "Colorado St Rams", "COLST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Colorado St Rams",
    },
    {
        "canonical": "Coppin State Eagles",
        "mascot": "Eagles",
        "city": "Baltimore",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#00508F",

        # Polymarket
        "polymarket_id": 1858,
        "polymarket_abbreviation": "coppst",
        "polymarket_name": "Coppin State Eagles",
        "polymarket_safe_name": "Coppin State Eagles",
        "polymarket_names": ["Coppin State Eagles", "Coppin St Eagles", "COPPST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Coppin St Eagles",
    },
    {
        "canonical": "DePaul Blue Demons",
        "mascot": "Blue Demons",
        "city": "Chicago",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#005A8B",

        # Polymarket
        "polymarket_id": 1725,
        "polymarket_abbreviation": "depaul",
        "polymarket_name": "DePaul Blue Demons",
        "polymarket_safe_name": "DePaul Blue Demons",
        "polymarket_names": ["DePaul Blue Demons", "DEPAUL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "DePaul Blue Demons",
    },
    {
        "canonical": "Delaware State Hornets",
        "mascot": "Hornets",
        "city": "Dover",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#EE3124",

        # Polymarket
        "polymarket_id": 1859,
        "polymarket_abbreviation": "delst",
        "polymarket_name": "Delaware State Hornets",
        "polymarket_safe_name": "Delaware State Hornets",
        "polymarket_names": ["Delaware State Hornets", "Delaware St Hornets", "DELST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Delaware St Hornets",
    },
    {
        "canonical": "Denver Pioneers",
        "mascot": "Pioneers",
        "city": "Denver",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#BA0C2F",

        # Polymarket
        "polymarket_id": 1976,
        "polymarket_abbreviation": "den",
        "polymarket_name": "Denver Pioneers",
        "polymarket_safe_name": "Denver Pioneers",
        "polymarket_names": ["Denver Pioneers", "DEN"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Denver Pioneers",
    },
    {
        "canonical": "Detroit Mercy Titans",
        "mascot": "Titans",
        "city": "Detroit",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003E9E",

        # Polymarket
        "polymarket_id": 1812,
        "polymarket_abbreviation": "det",
        "polymarket_name": "Detroit Titans",
        "polymarket_safe_name": "Detroit Mercy Titans",
        "polymarket_names": ["Detroit Titans", "Detroit Mercy Titans", "DET"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Detroit Mercy Titans",
    },
    {
        "canonical": "Drexel Dragons",
        "mascot": "Dragons",
        "city": "Philadelphia",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0D4D91",

        # Polymarket
        "polymarket_id": 1791,
        "polymarket_abbreviation": "drexel",
        "polymarket_name": "Drexel Dragons",
        "polymarket_safe_name": "Drexel Dragons",
        "polymarket_names": ["Drexel Dragons", "DREXEL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Drexel Dragons",
    },
    {
        "canonical": "Duke Blue Devils",
        "mascot": "Blue Devils",
        "city": "Durham",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003087",

        # Polymarket
        "polymarket_id": 1685,
        "polymarket_abbreviation": "duke",
        "polymarket_name": "Duke Blue Devils",
        "polymarket_safe_name": "Duke Blue Devils",
        "polymarket_names": ["Duke Blue Devils", "DUKE"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Duke Blue Devils",
    },
    {
        "canonical": "East Tennessee State Buccaneers",
        "mascot": "Buccaneers",
        "city": "Johnson City",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#041E42",

        # Polymarket
        "polymarket_id": 1939,
        "polymarket_abbreviation": "etnst",
        "polymarket_name": "East Tennessee State Buccaneers",
        "polymarket_safe_name": "East Tennessee State Buccaneers",
        "polymarket_names": ["East Tennessee State Buccaneers", "East Tennessee St Buccaneers", "ETNST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "East Tennessee St Buccaneers",
    },
    {
        "canonical": "Eastern Illinois Panthers",
        "mascot": "Panthers",
        "city": "Charleston",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0033A0",

        # Polymarket
        "polymarket_id": 1896,
        "polymarket_abbreviation": "eill",
        "polymarket_name": "Eastern Illinois Panthers",
        "polymarket_safe_name": "Eastern Illinois Panthers",
        "polymarket_names": ["Eastern Illinois Panthers", "EILL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Eastern Illinois Panthers",
    },
    {
        "canonical": "Fairfield Stags",
        "mascot": "Stags",
        "city": "Fairfield",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#E0143E",

        # Polymarket
        "polymarket_id": 1829,
        "polymarket_abbreviation": "fair",
        "polymarket_name": "Fairfield Stags",
        "polymarket_safe_name": "Fairfield Stags",
        "polymarket_names": ["Fairfield Stags", "FAIR"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Fairfield Stags",
    },
    {
        "canonical": "Florida Atlantic Owls",
        "mascot": "Owls",
        "city": "Boca Raton",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003E7E",

        # Polymarket
        "polymarket_id": 1804,
        "polymarket_abbreviation": "flatl",
        "polymarket_name": "Florida Atlantic Owls",
        "polymarket_safe_name": "Florida Atlantic Owls",
        "polymarket_names": ["Florida Atlantic Owls", "FLATL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Florida Atlantic Owls",
    },
    {
        "canonical": "Georgia Tech Yellow Jackets",
        "mascot": "Yellow Jackets",
        "city": "Atlanta",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#B3A369",

        # Polymarket
        "polymarket_id": 1691,
        "polymarket_abbreviation": "gtech",
        "polymarket_name": "Georgia Tech Yellow Jackets",
        "polymarket_safe_name": "Georgia Tech Yellow Jackets",
        "polymarket_names": ["Georgia Tech Yellow Jackets", "GTECH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Georgia Tech Yellow Jackets",
    },
    {
        "canonical": "Harvard Crimson",
        "mascot": "Crimson",
        "city": "Cambridge",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#A31F36",

        # Polymarket
        "polymarket_id": 1823,
        "polymarket_abbreviation": "harvrd",
        "polymarket_name": "Harvard Crimson",
        "polymarket_safe_name": "Harvard Crimson",
        "polymarket_names": ["Harvard Crimson", "HARVRD"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Harvard Crimson",
    },
    {
        "canonical": "High Point Panthers",
        "mascot": "Panthers",
        "city": "High Point",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#4E00AD",

        # Polymarket
        "polymarket_id": 1744,
        "polymarket_abbreviation": "hpnt",
        "polymarket_name": "High Point Panthers",
        "polymarket_safe_name": "High Point Panthers",
        "polymarket_names": ["High Point Panthers", "HPNT"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "High Point Panthers",
    },
    {
        "canonical": "Houston Cougars",
        "mascot": "Cougars",
        "city": "Houston",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C8102E",

        # Polymarket
        "polymarket_id": 1666,
        "polymarket_abbreviation": "hou",
        "polymarket_name": "Houston Cougars",
        "polymarket_safe_name": "Houston Cougars",
        "polymarket_names": ["Houston Cougars", "HOU"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Houston Cougars",
    },
    {
        "canonical": "Howard Bison",
        "mascot": "Bison",
        "city": "Washington",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003A63",

        # Polymarket
        "polymarket_id": 1853,
        "polymarket_abbreviation": "howrd",
        "polymarket_name": "Howard Bison",
        "polymarket_safe_name": "Howard Bison",
        "polymarket_names": ["Howard Bison", "HOWRD"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Howard Bison",
    },
    {
        "canonical": "Illinois State Redbirds",
        "mascot": "Redbirds",
        "city": "Normal",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#CE1126",

        # Polymarket
        "polymarket_id": 1862,
        "polymarket_abbreviation": "illst",
        "polymarket_name": "Illinois State Redbirds",
        "polymarket_safe_name": "Illinois State Redbirds",
        "polymarket_names": ["Illinois State Redbirds", "Illinois St Redbirds", "ILLST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Illinois St Redbirds",
    },
    {
        "canonical": "Incarnate Word Cardinals",
        "mascot": "Cardinals",
        "city": "San Antonio",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#CB333B",

        # Polymarket
        "polymarket_id": 1951,
        "polymarket_abbreviation": "incar",
        "polymarket_name": "Incarnate Word Cardinals",
        "polymarket_safe_name": "Incarnate Word Cardinals",
        "polymarket_names": ["Incarnate Word Cardinals", "INCAR"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Incarnate Word Cardinals",
    },
    {
        "canonical": "Indiana Hoosiers",
        "mascot": "Hoosiers",
        "city": "Bloomington",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#990000",

        # Polymarket
        "polymarket_id": 1752,
        "polymarket_abbreviation": "ind",
        "polymarket_name": "Indiana Hoosiers",
        "polymarket_safe_name": "Indiana Hoosiers",
        "polymarket_names": ["Indiana Hoosiers", "IND"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Indiana Hoosiers",
    },
    {
        "canonical": "Iona Gaels",
        "mascot": "Gaels",
        "city": "New Rochelle",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#910026",

        # Polymarket
        "polymarket_id": 1826,
        "polymarket_abbreviation": "iona",
        "polymarket_name": "Iona Gaels",
        "polymarket_safe_name": "Iona Gaels",
        "polymarket_names": ["Iona Gaels", "IONA"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Iona Gaels",
    },
    {
        "canonical": "James Madison Dukes",
        "mascot": "Dukes",
        "city": "Harrisonburg",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#450084",

        # Polymarket
        "polymarket_id": 1785,
        "polymarket_abbreviation": "jmad",
        "polymarket_name": "James Madison Dukes",
        "polymarket_safe_name": "James Madison Dukes",
        "polymarket_names": ["James Madison Dukes", "JMAD"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "James Madison Dukes",
    },
    {
        "canonical": "Kennesaw State Owls",
        "mascot": "Owls",
        "city": "Kennesaw",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#EAA612",

        # Polymarket
        "polymarket_id": 1701,
        "polymarket_abbreviation": "kenest",
        "polymarket_name": "Kennesaw State Owls",
        "polymarket_safe_name": "Kennesaw State Owls",
        "polymarket_names": ["Kennesaw State Owls", "Kennesaw St Owls", "KENEST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Kennesaw St Owls",
    },
    {
        "canonical": "Kent State Golden Flashes",
        "mascot": "Golden Flashes",
        "city": "Kent",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003F8E",

        # Polymarket
        "polymarket_id": 1837,
        "polymarket_abbreviation": "kentst",
        "polymarket_name": "Kent State Golden Flashes",
        "polymarket_safe_name": "Kent State Golden Flashes",
        "polymarket_names": ["Kent State Golden Flashes", "KENTST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Kent State Golden Flashes",
    },
    {
        "canonical": "LIU Sharks",
        "mascot": "Sharks",
        "city": "Brooklyn",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#4FB5E5",

        # Polymarket
        "polymarket_id": 1886,
        "polymarket_abbreviation": "liub",
        "polymarket_name": "LIU Sharks",
        "polymarket_safe_name": "Long Island University Sharks",
        "polymarket_names": ["LIU Sharks", "Long Island University Sharks", "LIUB"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "LIU Sharks",
    },
    {
        "canonical": "Liberty Flames",
        "mascot": "Flames",
        "city": "Lynchburg",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C41230",

        # Polymarket
        "polymarket_id": 1743,
        "polymarket_abbreviation": "librty",
        "polymarket_name": "Liberty Flames",
        "polymarket_safe_name": "Liberty Flames",
        "polymarket_names": ["Liberty Flames", "LIBRTY"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Liberty Flames",
    },
    {
        "canonical": "Lindenwood Lions",
        "mascot": "Lions",
        "city": "St. Charles",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0070B9",

        # Polymarket
        "polymarket_id": 2013,
        "polymarket_abbreviation": "jac",
        "polymarket_name": "Lindenwood Lions",
        "polymarket_safe_name": "Lindenwood Lions",
        "polymarket_names": ["Lindenwood Lions", "JAC"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Lindenwood Lions",
    },
    {
        "canonical": "Little Rock Trojans",
        "mascot": "Trojans",
        "city": "Little Rock",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#792A3F",

        # Polymarket
        "polymarket_id": 1980,
        "polymarket_abbreviation": "arlr",
        "polymarket_name": "Little Rock Trojans",
        "polymarket_safe_name": "Little Rock Trojans",
        "polymarket_names": ["Little Rock Trojans", "Arkansas-Little Rock Trojans", "ARLR"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Arkansas-Little Rock Trojans",
    },
    {
        "canonical": "Louisiana-Monroe Warhawks",
        "mascot": "Warhawks",
        "city": "Monroe",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#862633",

        # Polymarket
        "polymarket_id": 1983,
        "polymarket_abbreviation": "lamon",
        "polymarket_name": "Louisiana-Monroe Warhawks",
        "polymarket_safe_name": "UL Monroe Warhawks",
        "polymarket_names": ["Louisiana-Monroe Warhawks", "UL Monroe Warhawks", "LAMON"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UL Monroe Warhawks",
    },
    {
        "canonical": "Loyola Chicago Ramblers",
        "mascot": "Ramblers",
        "city": "Chicago",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#8D0034",

        # Polymarket
        "polymarket_id": 1867,
        "polymarket_abbreviation": "loych",
        "polymarket_name": "Loyola Chicago Ramblers",
        "polymarket_safe_name": "Loyola Chicago Ramblers",
        "polymarket_names": ["Loyola Chicago Ramblers", "Loyola (Chi) Ramblers", "LOYCH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Loyola (Chi) Ramblers",
    },
    {
        "canonical": "Manhattan Jaspers",
        "mascot": "Jaspers",
        "city": "Riverdale",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#00703C",

        # Polymarket
        "polymarket_id": 1830,
        "polymarket_abbreviation": "manh",
        "polymarket_name": "Manhattan Jaspers",
        "polymarket_safe_name": "Manhattan Jaspers",
        "polymarket_names": ["Manhattan Jaspers", "MANH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Manhattan Jaspers",
    },
    {
        "canonical": "Marist Red Foxes",
        "mascot": "Red Foxes",
        "city": "Poughkeepsie",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C8102E",

        # Polymarket
        "polymarket_id": 1835,
        "polymarket_abbreviation": "marist",
        "polymarket_name": "Marist Red Foxes",
        "polymarket_safe_name": "Marist Red Foxes",
        "polymarket_names": ["Marist Red Foxes", "MARIST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Marist Red Foxes",
    },
    {
        "canonical": "Maryland Eastern Shore Hawks",
        "mascot": "Hawks",
        "city": "Princess Anne",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#872743",

        # Polymarket
        "polymarket_id": 1852,
        "polymarket_abbreviation": "mdes",
        "polymarket_name": "Maryland Eastern Shore Hawks",
        "polymarket_safe_name": "Maryland Eastern Shore Hawks",
        "polymarket_names": ["Maryland Eastern Shore Hawks", "Maryland-Eastern Shore Hawks", "MDES"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Maryland-Eastern Shore Hawks",
    },
    {
        "canonical": "Maryland Terrapins",
        "mascot": "Terrapins",
        "city": "College Park",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#E03A3E",

        # Polymarket
        "polymarket_id": 1751,
        "polymarket_abbreviation": "mary",
        "polymarket_name": "Maryland Terrapins",
        "polymarket_safe_name": "Maryland Terrapins",
        "polymarket_names": ["Maryland Terrapins", "MARY"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Maryland Terrapins",
    },
    {
        "canonical": "UMass Lowell River Hawks",
        "mascot": "River Hawks",
        "city": "Lowell",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0067B1",

        # Polymarket
        "polymarket_id": 1676,
        "polymarket_abbreviation": "maslow",
        "polymarket_name": "Massachusetts-Lowell River Hawks",
        "polymarket_safe_name": "UMass Lowell River Hawks",
        "polymarket_names": ["Massachusetts-Lowell River Hawks", "UMass Lowell River Hawks", "MASLOW"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UMass Lowell River Hawks",
    },
    {
        "canonical": "Mercer Bears",
        "mascot": "Bears",
        "city": "Macon",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#F76800",

        # Polymarket
        "polymarket_id": 1941,
        "polymarket_abbreviation": "merc",
        "polymarket_name": "Mercer Bears",
        "polymarket_safe_name": "Mercer Bears",
        "polymarket_names": ["Mercer Bears", "MERC"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Mercer Bears",
    },
    {
        "canonical": "Miami (OH) RedHawks",
        "mascot": "RedHawks",
        "city": "Oxford",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C41230",

        # Polymarket
        "polymarket_id": 1841,
        "polymarket_abbreviation": "miaoh",
        "polymarket_name": "Miami (OH) RedHawks",
        "polymarket_safe_name": "Miami (OH) RedHawks",
        "polymarket_names": ["Miami (OH) RedHawks", "MIAOH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Miami (OH) RedHawks",
    },
    {
        "canonical": "Miami Hurricanes",
        "mascot": "Hurricanes",
        "city": "Coral Gables",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#F47321",

        # Polymarket
        "polymarket_id": 1682,
        "polymarket_abbreviation": "mia",
        "polymarket_name": "Miami Hurricanes",
        "polymarket_safe_name": "Miami Hurricanes",
        "polymarket_names": ["Miami Hurricanes", "MIA"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Miami Hurricanes",
    },
    {
        "canonical": "Michigan Wolverines",
        "mascot": "Wolverines",
        "city": "Ann Arbor",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#00426B",

        # Polymarket
        "polymarket_id": 1754,
        "polymarket_abbreviation": "mich",
        "polymarket_name": "Michigan Wolverines",
        "polymarket_safe_name": "Michigan Wolverines",
        "polymarket_names": ["Michigan Wolverines", "MICH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Michigan Wolverines",
    },
    {
        "canonical": "Montana Grizzlies",
        "mascot": "Grizzlies",
        "city": "Missoula",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#660033",

        # Polymarket
        "polymarket_id": 1727,
        "polymarket_abbreviation": "mont",
        "polymarket_name": "Montana Grizzlies",
        "polymarket_safe_name": "Montana Grizzlies",
        "polymarket_names": ["Montana Grizzlies", "MONT"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Montana Grizzlies",
    },
    {
        "canonical": "Montana State Bobcats",
        "mascot": "Bobcats",
        "city": "Bozeman",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0D2C6C",

        # Polymarket
        "polymarket_id": 1733,
        "polymarket_abbreviation": "monst",
        "polymarket_name": "Montana State Bobcats",
        "polymarket_safe_name": "Montana State Bobcats",
        "polymarket_names": ["Montana State Bobcats", "Montana St Bobcats", "MONST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Montana St Bobcats",
    },
    {
        "canonical": "Murray State Racers",
        "mascot": "Racers",
        "city": "Murray",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#002144",

        # Polymarket
        "polymarket_id": 1897,
        "polymarket_abbreviation": "murst",
        "polymarket_name": "Murray State Racers",
        "polymarket_safe_name": "Murray State Racers",
        "polymarket_names": ["Murray State Racers", "Murray St Racers", "MURST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Murray St Racers",
    },
    {
        "canonical": "Nevada Wolf Pack",
        "mascot": "Wolf Pack",
        "city": "Reno",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003366",

        # Polymarket
        "polymarket_id": 1874,
        "polymarket_abbreviation": "nevada",
        "polymarket_name": "Nevada Wolf Pack",
        "polymarket_safe_name": "Nevada Wolf Pack",
        "polymarket_names": ["Nevada Wolf Pack", "NEVADA"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Nevada Wolf Pack",
    },
    {
        "canonical": "New Orleans Privateers",
        "mascot": "Privateers",
        "city": "New Orleans",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#005CA6",

        # Polymarket
        "polymarket_id": 1954,
        "polymarket_abbreviation": "no",
        "polymarket_name": "New Orleans Privateers",
        "polymarket_safe_name": "New Orleans Privateers",
        "polymarket_names": ["New Orleans Privateers", "NO"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "New Orleans Privateers",
    },
    {
        "canonical": "Norfolk State Spartans",
        "mascot": "Spartans",
        "city": "Norfolk",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#007A53",

        # Polymarket
        "polymarket_id": 1850,
        "polymarket_abbreviation": "norfst",
        "polymarket_name": "Norfolk State Spartans",
        "polymarket_safe_name": "Norfolk State Spartans",
        "polymarket_names": ["Norfolk State Spartans", "Norfolk St Spartans", "NORFST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Norfolk St Spartans",
    },
    {
        "canonical": "North Carolina Central Eagles",
        "mascot": "Eagles",
        "city": "Durham",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#8B2331",

        # Polymarket
        "polymarket_id": 1855,
        "polymarket_abbreviation": "ncc",
        "polymarket_name": "North Carolina Central Eagles",
        "polymarket_safe_name": "North Carolina Central Eagles",
        "polymarket_names": ["North Carolina Central Eagles", "NCC"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "North Carolina Central Eagles",
    },
    {
        "canonical": "NC State Wolfpack",
        "mascot": "Wolfpack",
        "city": "Raleigh",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#CC0000",

        # Polymarket
        "polymarket_id": 1692,
        "polymarket_abbreviation": "ncst",
        "polymarket_name": "North Carolina State Wolfpack",
        "polymarket_safe_name": "NC State Wolfpack",
        "polymarket_names": ["North Carolina State Wolfpack", "NC State Wolfpack", "NCST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "NC State Wolfpack",
    },
    {
        "canonical": "North Carolina Tar Heels",
        "mascot": "Tar Heels",
        "city": "Chapel Hill",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#56A0D3",

        # Polymarket
        "polymarket_id": 1680,
        "polymarket_abbreviation": "ncar",
        "polymarket_name": "North Carolina Tar Heels",
        "polymarket_safe_name": "North Carolina Tar Heels",
        "polymarket_names": ["North Carolina Tar Heels", "NCAR"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "North Carolina Tar Heels",
    },
    {
        "canonical": "North Dakota Fighting Hawks",
        "mascot": "Fighting Hawks",
        "city": "Grand Forks",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#009A44",

        # Polymarket
        "polymarket_id": 1730,
        "polymarket_abbreviation": "ndak",
        "polymarket_name": "North Dakota Fighting Hawks",
        "polymarket_safe_name": "North Dakota Fighting Hawks",
        "polymarket_names": ["North Dakota Fighting Hawks", "NDAK"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "North Dakota Fighting Hawks",
    },
    {
        "canonical": "Northeastern Huskies",
        "mascot": "Huskies",
        "city": "Boston",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C8102E",

        # Polymarket
        "polymarket_id": 1790,
        "polymarket_abbreviation": "neast",
        "polymarket_name": "Northeastern Huskies",
        "polymarket_safe_name": "Northeastern Huskies",
        "polymarket_names": ["Northeastern Huskies", "NEAST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Northeastern Huskies",
    },
    {
        "canonical": "Notre Dame Fighting Irish",
        "mascot": "Fighting Irish",
        "city": "South Bend",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0B4B8E",

        # Polymarket
        "polymarket_id": 1684,
        "polymarket_abbreviation": "nd",
        "polymarket_name": "Notre Dame Fighting Irish",
        "polymarket_safe_name": "Notre Dame Fighting Irish",
        "polymarket_names": ["Notre Dame Fighting Irish", "ND"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Notre Dame Fighting Irish",
    },
    {
        "canonical": "Omaha Mavericks",
        "mascot": "Mavericks",
        "city": "Omaha",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#D71920",

        # Polymarket
        "polymarket_id": 1973,
        "polymarket_abbreviation": "neom",
        "polymarket_name": "Omaha Mavericks",
        "polymarket_safe_name": "Omaha Mavericks",
        "polymarket_names": ["Omaha Mavericks", "NEOM"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Omaha Mavericks",
    },
    {
        "canonical": "Pacific Tigers",
        "mascot": "Tigers",
        "city": "Stockton",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#F47920",

        # Polymarket
        "polymarket_id": 1996,
        "polymarket_abbreviation": "pacfc",
        "polymarket_name": "Pacific Tigers",
        "polymarket_safe_name": "Pacific Tigers",
        "polymarket_names": ["Pacific Tigers", "PACFC"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Pacific Tigers",
    },
    {
        "canonical": "Saint Mary's Gaels",
        "mascot": "Gaels",
        "city": "Moraga",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#D90123",

        # Polymarket
        "polymarket_id": 1992,
        "polymarket_abbreviation": "stmry",
        "polymarket_name": "Saint Mary's Gaels",
        "polymarket_safe_name": "Saint Mary's Gaels",
        "polymarket_names": ["Saint Mary's Gaels", "STMRY"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Saint Mary's Gaels",
    },
    {
        "canonical": "Saint Peter's Peacocks",
        "mascot": "Peacocks",
        "city": "Jersey City",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003C71",

        # Polymarket
        "polymarket_id": 1828,
        "polymarket_abbreviation": "stpete",
        "polymarket_name": "Saint Peter's Peacocks",
        "polymarket_safe_name": "Saint Peter's Peacocks",
        "polymarket_names": ["Saint Peter's Peacocks", "STPETE"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Saint Peter's Peacocks",
    },
    {
        "canonical": "San Diego Toreros",
        "mascot": "Toreros",
        "city": "San Diego",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0061B8",

        # Polymarket
        "polymarket_id": 1999,
        "polymarket_abbreviation": "sd",
        "polymarket_name": "San Diego Toreros",
        "polymarket_safe_name": "San Diego Toreros",
        "polymarket_names": ["San Diego Toreros", "SD"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "San Diego Toreros",
    },
    {
        "canonical": "San Jose State Spartans",
        "mascot": "Spartans",
        "city": "San Jose",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0055A2",

        # Polymarket
        "polymarket_id": 1880,
        "polymarket_abbreviation": "sjst",
        "polymarket_name": "San Jose State Spartans",
        "polymarket_safe_name": "San José State Spartans",
        "polymarket_names": ["San Jose State Spartans", "San José State Spartans", "San José St Spartans", "SJST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "San José St Spartans",
    },
    {
        "canonical": "South Alabama Jaguars",
        "mascot": "Jaguars",
        "city": "Mobile",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#00205B",

        # Polymarket
        "polymarket_id": 1987,
        "polymarket_abbreviation": "sala",
        "polymarket_name": "South Alabama Jaguars",
        "polymarket_safe_name": "South Alabama Jaguars",
        "polymarket_names": ["South Alabama Jaguars", "SALA"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "South Alabama Jaguars",
    },
    {
        "canonical": "South Carolina Gamecocks",
        "mascot": "Gamecocks",
        "city": "Columbia",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#73000A",

        # Polymarket
        "polymarket_id": 1924,
        "polymarket_abbreviation": "sc",
        "polymarket_name": "South Carolina Gamecocks",
        "polymarket_safe_name": "South Carolina Gamecocks",
        "polymarket_names": ["South Carolina Gamecocks", "SC"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "South Carolina Gamecocks",
    },
    {
        "canonical": "South Dakota Coyotes",
        "mascot": "Coyotes",
        "city": "Vermillion",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C8102E",

        # Polymarket
        "polymarket_id": 1978,
        "polymarket_abbreviation": "sdak",
        "polymarket_name": "South Dakota Coyotes",
        "polymarket_safe_name": "South Dakota Coyotes",
        "polymarket_names": ["South Dakota Coyotes", "SDAK"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "South Dakota Coyotes",
    },
    {
        "canonical": "Southeast Missouri State Redhawks",
        "mascot": "Redhawks",
        "city": "Cape Girardeau",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C8102E",

        # Polymarket
        "polymarket_id": 1900,
        "polymarket_abbreviation": "semst",
        "polymarket_name": "Southeast Missouri State Redhawks",
        "polymarket_safe_name": "Southeast Missouri State Redhawks",
        "polymarket_names": ["Southeast Missouri State Redhawks", "SE Missouri St Redhawks", "SEMST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "SE Missouri St Redhawks",
    },
    {
        "canonical": "Southern Illinois Salukis",
        "mascot": "Salukis",
        "city": "Carbondale",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#7A0019",

        # Polymarket
        "polymarket_id": 1863,
        "polymarket_abbreviation": "sill",
        "polymarket_name": "Southern Illinois Salukis",
        "polymarket_safe_name": "Southern Illinois Salukis",
        "polymarket_names": ["Southern Illinois Salukis", "SILL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Southern Illinois Salukis",
    },
    {
        "canonical": "Stephen F. Austin Lumberjacks",
        "mascot": "Lumberjacks",
        "city": "Nacogdoches",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#5F259F",

        # Polymarket
        "polymarket_id": 1948,
        "polymarket_abbreviation": "sfaus",
        "polymarket_name": "Stephen F. Austin Lumberjacks",
        "polymarket_safe_name": "Stephen F. Austin Lumberjacks",
        "polymarket_names": ["Stephen F. Austin Lumberjacks", "SFAUS"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Stephen F. Austin Lumberjacks",
    },
    {
        "canonical": "Texas A&M-Corpus Christi Islanders",
        "mascot": "Islanders",
        "city": "Corpus Christi",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0067C5",

        # Polymarket
        "polymarket_id": 1949,
        "polymarket_abbreviation": "tamu",
        "polymarket_name": "Texas A&M-Corpus Christi Islanders",
        "polymarket_safe_name": "Texas A&M-Corpus Christi Islanders",
        "polymarket_names": ["Texas A&M-Corpus Christi Islanders", "Texas A&M-CC Islanders", "TAMU"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Texas A&M-CC Islanders",
    },
    {
        "canonical": "UTRGV Vaqueros",
        "mascot": "Vaqueros",
        "city": "Edinburg",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#F05023",

        # Polymarket
        "polymarket_id": 2006,
        "polymarket_abbreviation": "utrgv",
        "polymarket_name": "Texas-Rio Grande Valley Vaqueros",
        "polymarket_safe_name": "UT Rio Grande Valley Vaqueros",
        "polymarket_names": ["Texas-Rio Grande Valley Vaqueros", "UT Rio Grande Valley Vaqueros", "UTRGV"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UT Rio Grande Valley Vaqueros",
    },
    {
        "canonical": "The Citadel Bulldogs",
        "mascot": "Bulldogs",
        "city": "Charleston",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#3975B7",

        # Polymarket
        "polymarket_id": 1945,
        "polymarket_abbreviation": "cita",
        "polymarket_name": "The Citadel Bulldogs",
        "polymarket_safe_name": "The Citadel Bulldogs",
        "polymarket_names": ["The Citadel Bulldogs", "CITA"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "The Citadel Bulldogs",
    },
    {
        "canonical": "UNC Wilmington Seahawks",
        "mascot": "Seahawks",
        "city": "Wilmington",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#009CA6",

        # Polymarket
        "polymarket_id": 1783,
        "polymarket_abbreviation": "ncw",
        "polymarket_name": "UNCW Seahawks",
        "polymarket_safe_name": "UNC Wilmington Seahawks",
        "polymarket_names": ["UNCW Seahawks", "UNC Wilmington Seahawks", "NCW"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UNC Wilmington Seahawks",
    },
    {
        "canonical": "USC Upstate Spartans",
        "mascot": "Spartans",
        "city": "Spartanburg",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#00833E",

        # Polymarket
        "polymarket_id": 1702,
        "polymarket_abbreviation": "scup",
        "polymarket_name": "USC Upstate Spartans",
        "polymarket_safe_name": "South Carolina Upstate Spartans",
        "polymarket_names": ["USC Upstate Spartans", "South Carolina Upstate Spartans", "SCUP"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "South Carolina Upstate Spartans",
    },
    {
        "canonical": "Utah Tech Trailblazers",
        "mascot": "Trailblazers",
        "city": "St. George",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#BA1C21",

        # Polymarket
        "polymarket_id": 2014,
        "polymarket_abbreviation": "dxst",
        "polymarket_name": "Utah Tech Trailblazers",
        "polymarket_safe_name": "Utah Tech Trailblazers",
        "polymarket_names": ["Utah Tech Trailblazers", "DXST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Utah Tech Trailblazers",
    },
    {
        "canonical": "Vanderbilt Commodores",
        "mascot": "Commodores",
        "city": "Nashville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#866D4B",

        # Polymarket
        "polymarket_id": 1930,
        "polymarket_abbreviation": "vand",
        "polymarket_name": "Vanderbilt Commodores",
        "polymarket_safe_name": "Vanderbilt Commodores",
        "polymarket_names": ["Vanderbilt Commodores", "VAND"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Vanderbilt Commodores",
    },
    {
        "canonical": "Western Kentucky Hilltoppers",
        "mascot": "Hilltoppers",
        "city": "Bowling Green",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C8102E",

        # Polymarket
        "polymarket_id": 1803,
        "polymarket_abbreviation": "wkent",
        "polymarket_name": "Western Kentucky Hilltoppers",
        "polymarket_safe_name": "Western Kentucky Hilltoppers",
        "polymarket_names": ["Western Kentucky Hilltoppers", "WKENT"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Western Kentucky Hilltoppers",
    },
    {
        "canonical": "Albany Great Danes",
        "mascot": "Great Danes",
        "city": "Albany",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#46166B",

        # Polymarket
        "polymarket_id": 1673,
        "polymarket_abbreviation": "albny",
        "polymarket_name": "Albany Great Danes",
        "polymarket_safe_name": "UAlbany Great Danes",
        "polymarket_names": ["Albany Great Danes", "UAlbany Great Danes", "ALBNY"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Albany Great Danes",
    },
    {
        "canonical": "Arkansas-Pine Bluff Golden Lions",
        "mascot": "Golden Lions",
        "city": "Pine Bluff",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#FDB913",

        # Polymarket
        "polymarket_id": 1967,
        "polymarket_abbreviation": "arpb",
        "polymarket_name": "Arkansas-Pine Bluff Golden Lions",
        "polymarket_safe_name": "Arkansas-Pine Bluff Golden Lions",
        "polymarket_names": ["Arkansas-Pine Bluff Golden Lions", "ARPB"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Arkansas-Pine Bluff Golden Lions",
    },
    {
        "canonical": "Boston College Eagles",
        "mascot": "Eagles",
        "city": "Chestnut Hill",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#8B2332",

        # Polymarket
        "polymarket_id": 1694,
        "polymarket_abbreviation": "boscol",
        "polymarket_name": "Boston College Eagles",
        "polymarket_safe_name": "Boston College Eagles",
        "polymarket_names": ["Boston College Eagles", "BOSCOL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Boston College Eagles",
    },
    {
        "canonical": "Boston University Terriers",
        "mascot": "Terriers",
        "city": "Boston",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#CC0000",

        # Polymarket
        "polymarket_id": 1916,
        "polymarket_abbreviation": "bostu",
        "polymarket_name": "Boston Terriers",
        "polymarket_safe_name": "Boston University Terriers",
        "polymarket_names": ["Boston Terriers", "Boston University Terriers", "Boston Univ. Terriers", "BOSTU"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Boston Univ. Terriers",
    },
    {
        "canonical": "Bradley Braves",
        "mascot": "Braves",
        "city": "Peoria",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#A50000",

        # Polymarket
        "polymarket_id": 1868,
        "polymarket_abbreviation": "bradly",
        "polymarket_name": "Bradley Braves",
        "polymarket_safe_name": "Bradley Braves",
        "polymarket_names": ["Bradley Braves", "BRADLY"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Bradley Braves",
    },
    {
        "canonical": "Brown Bears",
        "mascot": "Bears",
        "city": "Providence",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#4E3629",

        # Polymarket
        "polymarket_id": 1822,
        "polymarket_abbreviation": "brown",
        "polymarket_name": "Brown Bears",
        "polymarket_safe_name": "Brown Bears",
        "polymarket_names": ["Brown Bears", "BROWN"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Brown Bears",
    },
    {
        "canonical": "Bryant Bulldogs",
        "mascot": "Bulldogs",
        "city": "Smithfield",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#B4975B",

        # Polymarket
        "polymarket_id": 1888,
        "polymarket_abbreviation": "bryant",
        "polymarket_name": "Bryant Bulldogs",
        "polymarket_safe_name": "Bryant Bulldogs",
        "polymarket_names": ["Bryant Bulldogs", "BRYANT"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Bryant Bulldogs",
    },
    {
        "canonical": "CSUN Matadors",
        "mascot": "Matadors",
        "city": "Northridge",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#D22030",

        # Polymarket
        "polymarket_id": 1780,
        "polymarket_abbreviation": "csunr",
        "polymarket_name": "CSUN Matadors",
        "polymarket_safe_name": "Cal State Northridge Matadors",
        "polymarket_names": ["CSUN Matadors", "Cal State Northridge Matadors", "CSU Northridge Matadors", "CSUNR"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "CSU Northridge Matadors",
    },
    {
        "canonical": "Campbell Fighting Camels",
        "mascot": "Fighting Camels",
        "city": "Buies Creek",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#F77F00",

        # Polymarket
        "polymarket_id": 1749,
        "polymarket_abbreviation": "camp",
        "polymarket_name": "Campbell Fighting Camels",
        "polymarket_safe_name": "Campbell Fighting Camels",
        "polymarket_names": ["Campbell Fighting Camels", "CAMP"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Campbell Fighting Camels",
    },
    {
        "canonical": "UConn Huskies",
        "mascot": "Huskies",
        "city": "Storrs",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#4E9FE5",

        # Polymarket
        "polymarket_id": 1663,
        "polymarket_abbreviation": "uconn",
        "polymarket_name": "Connecticut Huskies",
        "polymarket_safe_name": "UConn Huskies",
        "polymarket_names": ["Connecticut Huskies", "UConn Huskies", "UCONN"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UConn Huskies",
    },
    {
        "canonical": "Dartmouth Big Green",
        "mascot": "Big Green",
        "city": "Hanover",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#00693E",

        # Polymarket
        "polymarket_id": 1824,
        "polymarket_abbreviation": "dart",
        "polymarket_name": "Dartmouth Big Green",
        "polymarket_safe_name": "Dartmouth Big Green",
        "polymarket_names": ["Dartmouth Big Green", "DART"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Dartmouth Big Green",
    },
    {
        "canonical": "Elon Phoenix",
        "mascot": "Phoenix",
        "city": "Elon",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#73000A",

        # Polymarket
        "polymarket_id": 1789,
        "polymarket_abbreviation": "elon",
        "polymarket_name": "Elon Phoenix",
        "polymarket_safe_name": "Elon Phoenix",
        "polymarket_names": ["Elon Phoenix", "ELON"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Elon Phoenix",
    },
    {
        "canonical": "Evansville Purple Aces",
        "mascot": "Purple Aces",
        "city": "Evansville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#470A68",

        # Polymarket
        "polymarket_id": 1861,
        "polymarket_abbreviation": "evans",
        "polymarket_name": "Evansville Aces",
        "polymarket_safe_name": "Evansville Purple Aces",
        "polymarket_names": ["Evansville Aces", "Evansville Purple Aces", "EVANS"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Evansville Purple Aces",
    },
    {
        "canonical": "Florida A&M Rattlers",
        "mascot": "Rattlers",
        "city": "Tallahassee",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#006747",

        # Polymarket
        "polymarket_id": 1856,
        "polymarket_abbreviation": "flam",
        "polymarket_name": "Florida A&M Rattlers",
        "polymarket_safe_name": "Florida A&M Rattlers",
        "polymarket_names": ["Florida A&M Rattlers", "FLAM"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Florida A&M Rattlers",
    },
    {
        "canonical": "Florida Gators",
        "mascot": "Gators",
        "city": "Gainesville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#FA4616",

        # Polymarket
        "polymarket_id": 1928,
        "polymarket_abbreviation": "fl",
        "polymarket_name": "Florida Gators",
        "polymarket_safe_name": "Florida Gators",
        "polymarket_names": ["Florida Gators", "FL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Florida Gators",
    },
    {
        "canonical": "Gardner-Webb Bulldogs",
        "mascot": "Bulldogs",
        "city": "Boiling Springs",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C8102E",

        # Polymarket
        "polymarket_id": 1742,
        "polymarket_abbreviation": "gardwb",
        "polymarket_name": "Gardner-Webb Runnin' Bulldogs",
        "polymarket_safe_name": "Gardner-Webb Runnin' Bulldogs",
        "polymarket_names": ["Gardner-Webb Runnin' Bulldogs", "Gardner-Webb Bulldogs", "GARDWB"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Gardner-Webb Bulldogs",
    },
    {
        "canonical": "George Mason Patriots",
        "mascot": "Patriots",
        "city": "Fairfax",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#006633",

        # Polymarket
        "polymarket_id": 1715,
        "polymarket_abbreviation": "gmsn",
        "polymarket_name": "George Mason Patriots",
        "polymarket_safe_name": "George Mason Patriots",
        "polymarket_names": ["George Mason Patriots", "GMSN"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "George Mason Patriots",
    },
    {
        "canonical": "George Washington Revolutionaries",
        "mascot": "Revolutionaries",
        "city": "Washington",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#AA9868",

        # Polymarket
        "polymarket_id": 1707,
        "polymarket_abbreviation": "geows",
        "polymarket_name": "George Washington Revolutionaries",
        "polymarket_safe_name": "George Washington Revolutionaries",
        "polymarket_names": ["George Washington Revolutionaries", "GW Revolutionaries", "GEOWS"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "GW Revolutionaries",
    },
    {
        "canonical": "Georgia Bulldogs",
        "mascot": "Bulldogs",
        "city": "Athens",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#BA0C2F",

        # Polymarket
        "polymarket_id": 1929,
        "polymarket_abbreviation": "ga",
        "polymarket_name": "Georgia Bulldogs",
        "polymarket_safe_name": "Georgia Bulldogs",
        "polymarket_names": ["Georgia Bulldogs", "GA"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Georgia Bulldogs",
    },
    {
        "canonical": "Gonzaga Bulldogs",
        "mascot": "Bulldogs",
        "city": "Spokane",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#094290",

        # Polymarket
        "polymarket_id": 1991,
        "polymarket_abbreviation": "gnzg",
        "polymarket_name": "Gonzaga Bulldogs",
        "polymarket_safe_name": "Gonzaga Bulldogs",
        "polymarket_names": ["Gonzaga Bulldogs", "GNZG"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Gonzaga Bulldogs",
    },
    {
        "canonical": "Grambling State Tigers",
        "mascot": "Tigers",
        "city": "Grambling",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#FDB927",

        # Polymarket
        "polymarket_id": 1969,
        "polymarket_abbreviation": "grmbst",
        "polymarket_name": "Grambling State Tigers",
        "polymarket_safe_name": "Grambling Tigers",
        "polymarket_names": ["Grambling State Tigers", "Grambling Tigers", "Grambling St Tigers", "GRMBST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Grambling St Tigers",
    },
    {
        "canonical": "Hofstra Pride",
        "mascot": "Pride",
        "city": "Hempstead",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003591",

        # Polymarket
        "polymarket_id": 1787,
        "polymarket_abbreviation": "hofst",
        "polymarket_name": "Hofstra Pride",
        "polymarket_safe_name": "Hofstra Pride",
        "polymarket_names": ["Hofstra Pride", "HOFST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Hofstra Pride",
    },
    {
        "canonical": "IU Indianapolis Jaguars",
        "mascot": "Jaguars",
        "city": "Indianapolis",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#B11811",

        # Polymarket
        "polymarket_id": 1974,
        "polymarket_abbreviation": "iupui",
        "polymarket_name": "IU Indy Jaguars",
        "polymarket_safe_name": "IU Indianapolis Jaguars",
        "polymarket_names": ["IU Indy Jaguars", "IU Indianapolis Jaguars", "IUPUI Jaguars", "IUPUI"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "IUPUI Jaguars",
    },
    {
        "canonical": "Jacksonville State Gamecocks",
        "mascot": "Gamecocks",
        "city": "Jacksonville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#CC0000",

        # Polymarket
        "polymarket_id": 1895,
        "polymarket_abbreviation": "jaxst",
        "polymarket_name": "Jacksonville State Gamecocks",
        "polymarket_safe_name": "Jacksonville State Gamecocks",
        "polymarket_names": ["Jacksonville State Gamecocks", "Jacksonville St Gamecocks", "JAXST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Jacksonville St Gamecocks",
    },
    {
        "canonical": "Kentucky Wildcats",
        "mascot": "Wildcats",
        "city": "Lexington",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0033A0",

        # Polymarket
        "polymarket_id": 1925,
        "polymarket_abbreviation": "uk",
        "polymarket_name": "Kentucky Wildcats",
        "polymarket_safe_name": "Kentucky Wildcats",
        "polymarket_names": ["Kentucky Wildcats", "UK"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Kentucky Wildcats",
    },
    {
        "canonical": "LSU Tigers",
        "mascot": "Tigers",
        "city": "Baton Rouge",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#461D7C",

        # Polymarket
        "polymarket_id": 1926,
        "polymarket_abbreviation": "lsu",
        "polymarket_name": "LSU Tigers",
        "polymarket_safe_name": "LSU Tigers",
        "polymarket_names": ["LSU Tigers", "LSU"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "LSU Tigers",
    },
    {
        "canonical": "La Salle Explorers",
        "mascot": "Explorers",
        "city": "Philadelphia",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#004C8A",

        # Polymarket
        "polymarket_id": 1716,
        "polymarket_abbreviation": "lasal",
        "polymarket_name": "La Salle Explorers",
        "polymarket_safe_name": "La Salle Explorers",
        "polymarket_names": ["La Salle Explorers", "LASAL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "La Salle Explorers",
    },
    {
        "canonical": "Lafayette Leopards",
        "mascot": "Leopards",
        "city": "Easton",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#98002E",

        # Polymarket
        "polymarket_id": 1923,
        "polymarket_abbreviation": "lafay",
        "polymarket_name": "Lafayette Leopards",
        "polymarket_safe_name": "Lafayette Leopards",
        "polymarket_names": ["Lafayette Leopards", "LAFAY"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Lafayette Leopards",
    },
    {
        "canonical": "Lamar Cardinals",
        "mascot": "Cardinals",
        "city": "Beaumont",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#E41C38",

        # Polymarket
        "polymarket_id": 1960,
        "polymarket_abbreviation": "lamar",
        "polymarket_name": "Lamar Cardinals",
        "polymarket_safe_name": "Lamar Cardinals",
        "polymarket_names": ["Lamar Cardinals", "LAMAR"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Lamar Cardinals",
    },
    {
        "canonical": "Le Moyne Dolphins",
        "mascot": "Dolphins",
        "city": "Syracuse",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#006B41",

        # Polymarket
        "polymarket_id": 2012,
        "polymarket_abbreviation": "lemyn",
        "polymarket_name": "Le Moyne Dolphins",
        "polymarket_safe_name": "Le Moyne Dolphins",
        "polymarket_names": ["Le Moyne Dolphins", "LEMYN"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Le Moyne Dolphins",
    },
    {
        "canonical": "Long Beach State 49ers",
        "mascot": "49ers",
        "city": "Long Beach",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#E0A200",

        # Polymarket
        "polymarket_id": 1776,
        "polymarket_abbreviation": "lbst",
        "polymarket_name": "Long Beach State Beach",
        "polymarket_safe_name": "Long Beach State Beach",
        "polymarket_names": ["Long Beach State Beach", "Long Beach St 49ers", "LBST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Long Beach St 49ers",
    },
    {
        "canonical": "Longwood Lancers",
        "mascot": "Lancers",
        "city": "Farmville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#00428F",

        # Polymarket
        "polymarket_id": 1746,
        "polymarket_abbreviation": "longwd",
        "polymarket_name": "Longwood Lancers",
        "polymarket_safe_name": "Longwood Lancers",
        "polymarket_names": ["Longwood Lancers", "LONGWD"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Longwood Lancers",
    },
    {
        "canonical": "Louisville Cardinals",
        "mascot": "Cardinals",
        "city": "Louisville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#AD0000",

        # Polymarket
        "polymarket_id": 1683,
        "polymarket_abbreviation": "lou",
        "polymarket_name": "Louisville Cardinals",
        "polymarket_safe_name": "Louisville Cardinals",
        "polymarket_names": ["Louisville Cardinals", "LOU"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Louisville Cardinals",
    },
    {
        "canonical": "Loyola Maryland Greyhounds",
        "mascot": "Greyhounds",
        "city": "Baltimore",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#005A3C",

        # Polymarket
        "polymarket_id": 1919,
        "polymarket_abbreviation": "loymd",
        "polymarket_name": "Loyola Maryland Greyhounds",
        "polymarket_safe_name": "Loyola Maryland Greyhounds",
        "polymarket_names": ["Loyola Maryland Greyhounds", "Loyola (MD) Greyhounds", "LOYMD"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Loyola (MD) Greyhounds",
    },
    {
        "canonical": "Loyola Marymount Lions",
        "mascot": "Lions",
        "city": "Los Angeles",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#AB0C2F",

        # Polymarket
        "polymarket_id": 2000,
        "polymarket_abbreviation": "loymry",
        "polymarket_name": "Loyola Marymount Lions",
        "polymarket_safe_name": "Loyola Marymount Lions",
        "polymarket_names": ["Loyola Marymount Lions", "LOYMRY"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Loyola Marymount Lions",
    },
    {
        "canonical": "Marquette Golden Eagles",
        "mascot": "Golden Eagles",
        "city": "Milwaukee",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003B75",

        # Polymarket
        "polymarket_id": 1724,
        "polymarket_abbreviation": "marq",
        "polymarket_name": "Marquette Golden Eagles",
        "polymarket_safe_name": "Marquette Golden Eagles",
        "polymarket_names": ["Marquette Golden Eagles", "MARQ"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Marquette Golden Eagles",
    },
    {
        "canonical": "Marshall Thundering Herd",
        "mascot": "Thundering Herd",
        "city": "Huntington",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#00B140",

        # Polymarket
        "polymarket_id": 1795,
        "polymarket_abbreviation": "marsh",
        "polymarket_name": "Marshall Thundering Herd",
        "polymarket_safe_name": "Marshall Thundering Herd",
        "polymarket_names": ["Marshall Thundering Herd", "MARSH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Marshall Thundering Herd",
    },
    {
        "canonical": "Massachusetts Minutemen",
        "mascot": "Minutemen",
        "city": "Amherst",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#881C1C",

        # Polymarket
        "polymarket_id": 1714,
        "polymarket_abbreviation": "umass",
        "polymarket_name": "Massachusetts Minutemen",
        "polymarket_safe_name": "Massachusetts Minutemen",
        "polymarket_names": ["Massachusetts Minutemen", "UMASS"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Massachusetts Minutemen",
    },
    {
        "canonical": "Memphis Tigers",
        "mascot": "Tigers",
        "city": "Memphis",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003087",

        # Polymarket
        "polymarket_id": 1667,
        "polymarket_abbreviation": "mphs",
        "polymarket_name": "Memphis Tigers",
        "polymarket_safe_name": "Memphis Tigers",
        "polymarket_names": ["Memphis Tigers", "MPHS"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Memphis Tigers",
    },
    {
        "canonical": "Mercyhurst Lakers",
        "mascot": "Lakers",
        "city": "Erie",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#187C6B",

        # Polymarket
        "polymarket_id": 2020,
        "polymarket_abbreviation": "mrcy",
        "polymarket_name": "Mercyhurst Lakers",
        "polymarket_safe_name": "Mercyhurst Lakers",
        "polymarket_names": ["Mercyhurst Lakers", "MRCY"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Mercyhurst Lakers",
    },
    {
        "canonical": "Merrimack Warriors",
        "mascot": "Warriors",
        "city": "North Andover",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003767",

        # Polymarket
        "polymarket_id": 2015,
        "polymarket_abbreviation": "merri",
        "polymarket_name": "Merrimack College Warriors",
        "polymarket_safe_name": "Merrimack Warriors",
        "polymarket_names": ["Merrimack College Warriors", "Merrimack Warriors", "MERRI"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Merrimack Warriors",
    },
    {
        "canonical": "Michigan State Spartans",
        "mascot": "Spartans",
        "city": "East Lansing",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#18453B",

        # Polymarket
        "polymarket_id": 1756,
        "polymarket_abbreviation": "mst",
        "polymarket_name": "Michigan State Spartans",
        "polymarket_safe_name": "Michigan State Spartans",
        "polymarket_names": ["Michigan State Spartans", "Michigan St Spartans", "MST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Michigan St Spartans",
    },
    {
        "canonical": "Middle Tennessee Blue Raiders",
        "mascot": "Blue Raiders",
        "city": "Murfreesboro",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0066CC",

        # Polymarket
        "polymarket_id": 1794,
        "polymarket_abbreviation": "mtnst",
        "polymarket_name": "Middle Tennessee Blue Raiders",
        "polymarket_safe_name": "Middle Tennessee Blue Raiders",
        "polymarket_names": ["Middle Tennessee Blue Raiders", "MTNST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Middle Tennessee Blue Raiders",
    },
    {
        "canonical": "Mississippi State Bulldogs",
        "mascot": "Bulldogs",
        "city": "Starkville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#660000",

        # Polymarket
        "polymarket_id": 1935,
        "polymarket_abbreviation": "mspst",
        "polymarket_name": "Mississippi State Bulldogs",
        "polymarket_safe_name": "Mississippi State Bulldogs",
        "polymarket_names": ["Mississippi State Bulldogs", "Mississippi St Bulldogs", "MSPST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Mississippi St Bulldogs",
    },
    {
        "canonical": "Mississippi Valley State Delta Devils",
        "mascot": "Delta Devils",
        "city": "Itta Bena",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#007A33",

        # Polymarket
        "polymarket_id": 1965,
        "polymarket_abbreviation": "msvlst",
        "polymarket_name": "Mississippi Valley State Delta Devils",
        "polymarket_safe_name": "Mississippi Valley State Delta Devils",
        "polymarket_names": ["Mississippi Valley State Delta Devils", "Miss Valley St Delta Devils", "MSVLST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Miss Valley St Delta Devils",
    },
    {
        "canonical": "Missouri State Bears",
        "mascot": "Bears",
        "city": "Springfield",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#6C1D45",

        # Polymarket
        "polymarket_id": 1866,
        "polymarket_abbreviation": "msrst",
        "polymarket_name": "Missouri State Bears",
        "polymarket_safe_name": "Missouri State Bears",
        "polymarket_names": ["Missouri State Bears", "Missouri St Bears", "MSRST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Missouri St Bears",
    },
    {
        "canonical": "Missouri Tigers",
        "mascot": "Tigers",
        "city": "Columbia",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#F1B82D",

        # Polymarket
        "polymarket_id": 1937,
        "polymarket_abbreviation": "missr",
        "polymarket_name": "Missouri Tigers",
        "polymarket_safe_name": "Missouri Tigers",
        "polymarket_names": ["Missouri Tigers", "MISSR"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Missouri Tigers",
    },
    {
        "canonical": "Morehead State Eagles",
        "mascot": "Eagles",
        "city": "Morehead",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#005EB8",

        # Polymarket
        "polymarket_id": 1893,
        "polymarket_abbreviation": "mhst",
        "polymarket_name": "Morehead State Eagles",
        "polymarket_safe_name": "Morehead State Eagles",
        "polymarket_names": ["Morehead State Eagles", "Morehead St Eagles", "MHST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Morehead St Eagles",
    },
    {
        "canonical": "Morgan State Bears",
        "mascot": "Bears",
        "city": "Baltimore",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#E35205",

        # Polymarket
        "polymarket_id": 1857,
        "polymarket_abbreviation": "morgst",
        "polymarket_name": "Morgan State Bears",
        "polymarket_safe_name": "Morgan State Bears",
        "polymarket_names": ["Morgan State Bears", "Morgan St Bears", "MORGST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Morgan St Bears",
    },
    {
        "canonical": "NJIT Highlanders",
        "mascot": "Highlanders",
        "city": "Newark",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#CC0000",

        # Polymarket
        "polymarket_id": 1698,
        "polymarket_abbreviation": "njit",
        "polymarket_name": "NJIT Highlanders",
        "polymarket_safe_name": "NJIT Highlanders",
        "polymarket_names": ["NJIT Highlanders", "NJIT"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "NJIT Highlanders",
    },
    {
        "canonical": "Navy Midshipmen",
        "mascot": "Midshipmen",
        "city": "Annapolis",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003B7C",

        # Polymarket
        "polymarket_id": 1915,
        "polymarket_abbreviation": "navy",
        "polymarket_name": "Navy Midshipmen",
        "polymarket_safe_name": "Navy Midshipmen",
        "polymarket_names": ["Navy Midshipmen", "NAVY"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Navy Midshipmen",
    },
    {
        "canonical": "Nebraska Cornhuskers",
        "mascot": "Cornhuskers",
        "city": "Lincoln",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#E41C38",

        # Polymarket
        "polymarket_id": 1758,
        "polymarket_abbreviation": "nebr",
        "polymarket_name": "Nebraska Cornhuskers",
        "polymarket_safe_name": "Nebraska Cornhuskers",
        "polymarket_names": ["Nebraska Cornhuskers", "NEBR"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Nebraska Cornhuskers",
    },
    {
        "canonical": "New Hampshire Wildcats",
        "mascot": "Wildcats",
        "city": "Durham",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#041E42",

        # Polymarket
        "polymarket_id": 1674,
        "polymarket_abbreviation": "nhamp",
        "polymarket_name": "New Hampshire Wildcats",
        "polymarket_safe_name": "New Hampshire Wildcats",
        "polymarket_names": ["New Hampshire Wildcats", "NHAMP"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "New Hampshire Wildcats",
    },
    {
        "canonical": "New Haven Chargers",
        "mascot": "Chargers",
        "city": "West Haven",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0064BD",

        # Polymarket
        "polymarket_id": 2025,
        "polymarket_abbreviation": "nhvn",
        "polymarket_name": "New Haven Chargers",
        "polymarket_safe_name": "New Haven Chargers",
        "polymarket_names": ["New Haven Chargers", "NHVN"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "New Haven Chargers",
    },
    {
        "canonical": "Niagara Purple Eagles",
        "mascot": "Purple Eagles",
        "city": "Niagara",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#582C83",

        # Polymarket
        "polymarket_id": 1834,
        "polymarket_abbreviation": "niagra",
        "polymarket_name": "Niagara Purple Eagles",
        "polymarket_safe_name": "Niagara Purple Eagles",
        "polymarket_names": ["Niagara Purple Eagles", "NIAGRA"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Niagara Purple Eagles",
    },
    {
        "canonical": "Nicholls State Colonels",
        "mascot": "Colonels",
        "city": "Thibodaux",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C8102E",

        # Polymarket
        "polymarket_id": 1959,
        "polymarket_abbreviation": "nichls",
        "polymarket_name": "Nicholls Colonels",
        "polymarket_safe_name": "Nicholls Colonels",
        "polymarket_names": ["Nicholls Colonels", "Nicholls St Colonels", "NICHLS"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Nicholls St Colonels",
    },
    {
        "canonical": "North Alabama Lions",
        "mascot": "Lions",
        "city": "Florence",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#4E2A84",

        # Polymarket
        "polymarket_id": 2011,
        "polymarket_abbreviation": "nal",
        "polymarket_name": "North Alabama Lions",
        "polymarket_safe_name": "North Alabama Lions",
        "polymarket_names": ["North Alabama Lions", "NAL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "North Alabama Lions",
    },
    {
        "canonical": "North Carolina A&T Aggies",
        "mascot": "Aggies",
        "city": "Greensboro",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#004684",

        # Polymarket
        "polymarket_id": 1854,
        "polymarket_abbreviation": "ncat",
        "polymarket_name": "North Carolina A&T Aggies",
        "polymarket_safe_name": "North Carolina A&T Aggies",
        "polymarket_names": ["North Carolina A&T Aggies", "NCAT"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "North Carolina A&T Aggies",
    },
    {
        "canonical": "North Florida Ospreys",
        "mascot": "Ospreys",
        "city": "Jacksonville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#004099",

        # Polymarket
        "polymarket_id": 1695,
        "polymarket_abbreviation": "nfl",
        "polymarket_name": "North Florida Ospreys",
        "polymarket_safe_name": "North Florida Ospreys",
        "polymarket_names": ["North Florida Ospreys", "NFL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "North Florida Ospreys",
    },
    {
        "canonical": "North Texas Mean Green",
        "mascot": "Mean Green",
        "city": "Denton",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#006633",

        # Polymarket
        "polymarket_id": 1800,
        "polymarket_abbreviation": "ntx",
        "polymarket_name": "North Texas Mean Green",
        "polymarket_safe_name": "North Texas Mean Green",
        "polymarket_names": ["North Texas Mean Green", "NTX"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "North Texas Mean Green",
    },
    {
        "canonical": "Northern Arizona Lumberjacks",
        "mascot": "Lumberjacks",
        "city": "Flagstaff",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003466",

        # Polymarket
        "polymarket_id": 1738,
        "polymarket_abbreviation": "narz",
        "polymarket_name": "Northern Arizona Lumberjacks",
        "polymarket_safe_name": "Northern Arizona Lumberjacks",
        "polymarket_names": ["Northern Arizona Lumberjacks", "NARZ"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Northern Arizona Lumberjacks",
    },
    {
        "canonical": "Northern Colorado Bears",
        "mascot": "Bears",
        "city": "Greeley",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#013C65",

        # Polymarket
        "polymarket_id": 1734,
        "polymarket_abbreviation": "ncol",
        "polymarket_name": "Northern Colorado Bears",
        "polymarket_safe_name": "Northern Colorado Bears",
        "polymarket_names": ["Northern Colorado Bears", "N Colorado Bears", "NCOL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "N Colorado Bears",
    },
    {
        "canonical": "Northern Iowa Panthers",
        "mascot": "Panthers",
        "city": "Cedar Falls",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#500778",

        # Polymarket
        "polymarket_id": 1864,
        "polymarket_abbreviation": "niowa",
        "polymarket_name": "Northern Iowa Panthers",
        "polymarket_safe_name": "Northern Iowa Panthers",
        "polymarket_names": ["Northern Iowa Panthers", "NIOWA"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Northern Iowa Panthers",
    },
    {
        "canonical": "Northern Kentucky Norse",
        "mascot": "Norse",
        "city": "Highland Heights",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#DBA100",

        # Polymarket
        "polymarket_id": 1813,
        "polymarket_abbreviation": "nkent",
        "polymarket_name": "Northern Kentucky Norse",
        "polymarket_safe_name": "Northern Kentucky Norse",
        "polymarket_names": ["Northern Kentucky Norse", "NKENT"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Northern Kentucky Norse",
    },
    {
        "canonical": "Ohio State Buckeyes",
        "mascot": "Buckeyes",
        "city": "Columbus",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#BB0000",

        # Polymarket
        "polymarket_id": 1757,
        "polymarket_abbreviation": "ohiost",
        "polymarket_name": "Ohio State Buckeyes",
        "polymarket_safe_name": "Ohio State Buckeyes",
        "polymarket_names": ["Ohio State Buckeyes", "OHIOST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Ohio State Buckeyes",
    },
    {
        "canonical": "Ole Miss Rebels",
        "mascot": "Rebels",
        "city": "Oxford",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#14213D",

        # Polymarket
        "polymarket_id": 1931,
        "polymarket_abbreviation": "miss",
        "polymarket_name": "Ole Miss Rebels",
        "polymarket_safe_name": "Ole Miss Rebels",
        "polymarket_names": ["Ole Miss Rebels", "MISS"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Ole Miss Rebels",
    },
    {
        "canonical": "Presbyterian Blue Hose",
        "mascot": "Blue Hose",
        "city": "Clinton",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#002D72",

        # Polymarket
        "polymarket_id": 1748,
        "polymarket_abbreviation": "presb",
        "polymarket_name": "Presbyterian Blue Hose",
        "polymarket_safe_name": "Presbyterian Blue Hose",
        "polymarket_names": ["Presbyterian Blue Hose", "PRESB"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Presbyterian Blue Hose",
    },
    {
        "canonical": "Purdue Boilermakers",
        "mascot": "Boilermakers",
        "city": "West Lafayette",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#CEB888",

        # Polymarket
        "polymarket_id": 1753,
        "polymarket_abbreviation": "pur",
        "polymarket_name": "Purdue Boilermakers",
        "polymarket_safe_name": "Purdue Boilermakers",
        "polymarket_names": ["Purdue Boilermakers", "PUR"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Purdue Boilermakers",
    },
    {
        "canonical": "Purdue Fort Wayne Mastodons",
        "mascot": "Mastodons",
        "city": "Fort Wayne",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#B69558",

        # Polymarket
        "polymarket_id": 1972,
        "polymarket_abbreviation": "ipfw",
        "polymarket_name": "Purdue Fort Wayne Mastodons",
        "polymarket_safe_name": "Purdue Fort Wayne Mastodons",
        "polymarket_names": ["Purdue Fort Wayne Mastodons", "Fort Wayne Mastodons", "IPFW"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Fort Wayne Mastodons",
    },
    {
        "canonical": "Queens University Royals",
        "mascot": "Royals",
        "city": "Charlotte",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#194695",

        # Polymarket
        "polymarket_id": 2016,
        "polymarket_abbreviation": "queen",
        "polymarket_name": "Queens (NC) Royals",
        "polymarket_safe_name": "Queens University Royals",
        "polymarket_names": ["Queens (NC) Royals", "Queens University Royals", "QUEEN"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Queens University Royals",
    },
    {
        "canonical": "Radford Highlanders",
        "mascot": "Highlanders",
        "city": "Radford",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C2011B",

        # Polymarket
        "polymarket_id": 1745,
        "polymarket_abbreviation": "radf",
        "polymarket_name": "Radford Highlanders",
        "polymarket_safe_name": "Radford Highlanders",
        "polymarket_names": ["Radford Highlanders", "RADF"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Radford Highlanders",
    },
    {
        "canonical": "Samford Bulldogs",
        "mascot": "Bulldogs",
        "city": "Birmingham",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0C2340",

        # Polymarket
        "polymarket_id": 1946,
        "polymarket_abbreviation": "samf",
        "polymarket_name": "Samford Bulldogs",
        "polymarket_safe_name": "Samford Bulldogs",
        "polymarket_names": ["Samford Bulldogs", "SAMF"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Samford Bulldogs",
    },
    {
        "canonical": "San Francisco Dons",
        "mascot": "Dons",
        "city": "San Francisco",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#007050",

        # Polymarket
        "polymarket_id": 1995,
        "polymarket_abbreviation": "sf",
        "polymarket_name": "San Francisco Dons",
        "polymarket_safe_name": "San Francisco Dons",
        "polymarket_names": ["San Francisco Dons", "SF"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "San Francisco Dons",
    },
    {
        "canonical": "Seton Hall Pirates",
        "mascot": "Pirates",
        "city": "South Orange",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#004488",

        # Polymarket
        "polymarket_id": 1719,
        "polymarket_abbreviation": "seton",
        "polymarket_name": "Seton Hall Pirates",
        "polymarket_safe_name": "Seton Hall Pirates",
        "polymarket_names": ["Seton Hall Pirates", "SETON"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Seton Hall Pirates",
    },
    {
        "canonical": "South Dakota State Jackrabbits",
        "mascot": "Jackrabbits",
        "city": "Brookings",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0033A0",

        # Polymarket
        "polymarket_id": 1971,
        "polymarket_abbreviation": "sdkst",
        "polymarket_name": "South Dakota State Jackrabbits",
        "polymarket_safe_name": "South Dakota State Jackrabbits",
        "polymarket_names": ["South Dakota State Jackrabbits", "South Dakota St Jackrabbits", "SDKST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "South Dakota St Jackrabbits",
    },
    {
        "canonical": "Southern Indiana Screaming Eagles",
        "mascot": "Screaming Eagles",
        "city": "Evansville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#CF102D",

        # Polymarket
        "polymarket_id": 2022,
        "polymarket_abbreviation": "usi",
        "polymarket_name": "Southern Indiana Screaming Eagles",
        "polymarket_safe_name": "Southern Indiana Screaming Eagles",
        "polymarket_names": ["Southern Indiana Screaming Eagles", "USI"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Southern Indiana Screaming Eagles",
    },
    {
        "canonical": "Stonehill Skyhawks",
        "mascot": "Skyhawks",
        "city": "Easton",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#433AA6",

        # Polymarket
        "polymarket_id": 2023,
        "polymarket_abbreviation": "stnh",
        "polymarket_name": "Stonehill Skyhawks",
        "polymarket_safe_name": "Stonehill Skyhawks",
        "polymarket_names": ["Stonehill Skyhawks", "STNH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Stonehill Skyhawks",
    },
    {
        "canonical": "Syracuse Orange",
        "mascot": "Orange",
        "city": "Syracuse",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#F76900",

        # Polymarket
        "polymarket_id": 1689,
        "polymarket_abbreviation": "syra",
        "polymarket_name": "Syracuse Orange",
        "polymarket_safe_name": "Syracuse Orange",
        "polymarket_names": ["Syracuse Orange", "SYRA"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Syracuse Orange",
    },
    {
        "canonical": "Troy Trojans",
        "mascot": "Trojans",
        "city": "Troy",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#8B1538",

        # Polymarket
        "polymarket_id": 1990,
        "polymarket_abbreviation": "troy",
        "polymarket_name": "Troy Trojans",
        "polymarket_safe_name": "Troy Trojans",
        "polymarket_names": ["Troy Trojans", "TROY"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Troy Trojans",
    },
    {
        "canonical": "UC Davis Aggies",
        "mascot": "Aggies",
        "city": "Davis",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#022851",

        # Polymarket
        "polymarket_id": 1777,
        "polymarket_abbreviation": "ucdv",
        "polymarket_name": "UC Davis Aggies",
        "polymarket_safe_name": "UC Davis Aggies",
        "polymarket_names": ["UC Davis Aggies", "UCDV"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UC Davis Aggies",
    },
    {
        "canonical": "UC Santa Barbara Gauchos",
        "mascot": "Gauchos",
        "city": "Santa Barbara",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#004275",

        # Polymarket
        "polymarket_id": 1778,
        "polymarket_abbreviation": "uscb",
        "polymarket_name": "UC Santa Barbara Gauchos",
        "polymarket_safe_name": "UC Santa Barbara Gauchos",
        "polymarket_names": ["UC Santa Barbara Gauchos", "USCB"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UC Santa Barbara Gauchos",
    },
    {
        "canonical": "UCF Knights",
        "mascot": "Knights",
        "city": "Orlando",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#BA9B37",

        # Polymarket
        "polymarket_id": 1668,
        "polymarket_abbreviation": "ucf",
        "polymarket_name": "UCF Knights",
        "polymarket_safe_name": "UCF Knights",
        "polymarket_names": ["UCF Knights", "UCF"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UCF Knights",
    },
    {
        "canonical": "UMBC Retrievers",
        "mascot": "Retrievers",
        "city": "Baltimore",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#F3A802",

        # Polymarket
        "polymarket_id": 1678,
        "polymarket_abbreviation": "umbc",
        "polymarket_name": "UMBC Retrievers",
        "polymarket_safe_name": "UMBC Retrievers",
        "polymarket_names": ["UMBC Retrievers", "UMBC"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UMBC Retrievers",
    },
    {
        "canonical": "UNC Asheville Bulldogs",
        "mascot": "Bulldogs",
        "city": "Asheville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#004DD1",

        # Polymarket
        "polymarket_id": 1739,
        "polymarket_abbreviation": "ncashe",
        "polymarket_name": "UNC Asheville Bulldogs",
        "polymarket_safe_name": "UNC Asheville Bulldogs",
        "polymarket_names": ["UNC Asheville Bulldogs", "NCASHE"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UNC Asheville Bulldogs",
    },
    {
        "canonical": "UNC Greensboro Spartans",
        "mascot": "Spartans",
        "city": "Greensboro",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#D89709",

        # Polymarket
        "polymarket_id": 1943,
        "polymarket_abbreviation": "ncg",
        "polymarket_name": "UNCG Spartans",
        "polymarket_safe_name": "UNC Greensboro Spartans",
        "polymarket_names": ["UNCG Spartans", "UNC Greensboro Spartans", "NCG"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UNC Greensboro Spartans",
    },
    {
        "canonical": "USC Trojans",
        "mascot": "Trojans",
        "city": "Los Angeles",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#990000",

        # Polymarket
        "polymarket_id": 1903,
        "polymarket_abbreviation": "usc",
        "polymarket_name": "USC Trojans",
        "polymarket_safe_name": "USC Trojans",
        "polymarket_names": ["USC Trojans", "USC"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "USC Trojans",
    },
    {
        "canonical": "UT Arlington Mavericks",
        "mascot": "Mavericks",
        "city": "Arlington",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0064B1",

        # Polymarket
        "polymarket_id": 1982,
        "polymarket_abbreviation": "txa",
        "polymarket_name": "UT Arlington Mavericks",
        "polymarket_safe_name": "UT Arlington Mavericks",
        "polymarket_names": ["UT Arlington Mavericks", "UT-Arlington Mavericks", "TXA"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UT-Arlington Mavericks",
    },
    {
        "canonical": "UTSA Roadrunners",
        "mascot": "Roadrunners",
        "city": "San Antonio",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#E35205",

        # Polymarket
        "polymarket_id": 1806,
        "polymarket_abbreviation": "utsa",
        "polymarket_name": "UTSA Roadrunners",
        "polymarket_safe_name": "UTSA Roadrunners",
        "polymarket_names": ["UTSA Roadrunners", "UTSA"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UTSA Roadrunners",
    },
    {
        "canonical": "Utah State Aggies",
        "mascot": "Aggies",
        "city": "Logan",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#275582",

        # Polymarket
        "polymarket_id": 1878,
        "polymarket_abbreviation": "utahst",
        "polymarket_name": "Utah State Aggies",
        "polymarket_safe_name": "Utah State Aggies",
        "polymarket_names": ["Utah State Aggies", "UTAHST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Utah State Aggies",
    },
    {
        "canonical": "Utah Utes",
        "mascot": "Utes",
        "city": "Salt Lake City",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#CC0000",

        # Polymarket
        "polymarket_id": 1905,
        "polymarket_abbreviation": "utah",
        "polymarket_name": "Utah Utes",
        "polymarket_safe_name": "Utah Utes",
        "polymarket_names": ["Utah Utes", "UTAH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Utah Utes",
    },
    {
        "canonical": "VMI Keydets",
        "mascot": "Keydets",
        "city": "Lexington",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#AE122A",

        # Polymarket
        "polymarket_id": 1947,
        "polymarket_abbreviation": "vamil",
        "polymarket_name": "VMI Keydets",
        "polymarket_safe_name": "VMI Keydets",
        "polymarket_names": ["VMI Keydets", "VAMIL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "VMI Keydets",
    },
    {
        "canonical": "Vermont Catamounts",
        "mascot": "Catamounts",
        "city": "Burlington",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#005710",

        # Polymarket
        "polymarket_id": 1675,
        "polymarket_abbreviation": "verm",
        "polymarket_name": "Vermont Catamounts",
        "polymarket_safe_name": "Vermont Catamounts",
        "polymarket_names": ["Vermont Catamounts", "VERM"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Vermont Catamounts",
    },
    {
        "canonical": "Villanova Wildcats",
        "mascot": "Wildcats",
        "city": "Villanova",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#00205B",

        # Polymarket
        "polymarket_id": 1717,
        "polymarket_abbreviation": "vill",
        "polymarket_name": "Villanova Wildcats",
        "polymarket_safe_name": "Villanova Wildcats",
        "polymarket_names": ["Villanova Wildcats", "VILL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Villanova Wildcats",
    },
    {
        "canonical": "Virginia Cavaliers",
        "mascot": "Cavaliers",
        "city": "Charlottesville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#F84C1E",

        # Polymarket
        "polymarket_id": 1681,
        "polymarket_abbreviation": "vir",
        "polymarket_name": "Virginia Cavaliers",
        "polymarket_safe_name": "Virginia Cavaliers",
        "polymarket_names": ["Virginia Cavaliers", "VIR"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Virginia Cavaliers",
    },
    {
        "canonical": "Virginia Tech Hokies",
        "mascot": "Hokies",
        "city": "Blacksburg",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#861F41",

        # Polymarket
        "polymarket_id": 1690,
        "polymarket_abbreviation": "vtech",
        "polymarket_name": "Virginia Tech Hokies",
        "polymarket_safe_name": "Virginia Tech Hokies",
        "polymarket_names": ["Virginia Tech Hokies", "VTECH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Virginia Tech Hokies",
    },
    {
        "canonical": "Wagner Seahawks",
        "mascot": "Seahawks",
        "city": "Staten Island",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0F6F56",

        # Polymarket
        "polymarket_id": 1881,
        "polymarket_abbreviation": "wag",
        "polymarket_name": "Wagner Seahawks",
        "polymarket_safe_name": "Wagner Seahawks",
        "polymarket_names": ["Wagner Seahawks", "WAG"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Wagner Seahawks",
    },
    {
        "canonical": "Wake Forest Demon Deacons",
        "mascot": "Demon Deacons",
        "city": "Winston-Salem",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#CEB888",

        # Polymarket
        "polymarket_id": 1693,
        "polymarket_abbreviation": "wake",
        "polymarket_name": "Wake Forest Demon Deacons",
        "polymarket_safe_name": "Wake Forest Demon Deacons",
        "polymarket_names": ["Wake Forest Demon Deacons", "WAKE"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Wake Forest Demon Deacons",
    },
    {
        "canonical": "West Georgia Wolves",
        "mascot": "Wolves",
        "city": "Carrollton",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0656A5",

        # Polymarket
        "polymarket_id": 2024,
        "polymarket_abbreviation": "uwg",
        "polymarket_name": "West Georgia Wolves",
        "polymarket_safe_name": "West Georgia Wolves",
        "polymarket_names": ["West Georgia Wolves", "UWG"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "West Georgia Wolves",
    },
    {
        "canonical": "Winthrop Eagles",
        "mascot": "Eagles",
        "city": "Rock Hill",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#990000",

        # Polymarket
        "polymarket_id": 1741,
        "polymarket_abbreviation": "winth",
        "polymarket_name": "Winthrop Eagles",
        "polymarket_safe_name": "Winthrop Eagles",
        "polymarket_names": ["Winthrop Eagles", "WINTH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Winthrop Eagles",
    },
    {
        "canonical": "Wisconsin Badgers",
        "mascot": "Badgers",
        "city": "Madison",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C5050C",

        # Polymarket
        "polymarket_id": 1755,
        "polymarket_abbreviation": "wisc",
        "polymarket_name": "Wisconsin Badgers",
        "polymarket_safe_name": "Wisconsin Badgers",
        "polymarket_names": ["Wisconsin Badgers", "WISC"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Wisconsin Badgers",
    },
    {
        "canonical": "Alabama Crimson Tide",
        "mascot": "Crimson Tide",
        "city": "Tuscaloosa",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#9E1B32",

        # Polymarket
        "polymarket_id": 1932,
        "polymarket_abbreviation": "ala",
        "polymarket_name": "Alabama Crimson Tide",
        "polymarket_safe_name": "Alabama Crimson Tide",
        "polymarket_names": ["Alabama Crimson Tide", "ALA"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Alabama Crimson Tide",
    },
    {
        "canonical": "Alcorn State Braves",
        "mascot": "Braves",
        "city": "Lorman",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#46166B",

        # Polymarket
        "polymarket_id": 1964,
        "polymarket_abbreviation": "alcst",
        "polymarket_name": "Alcorn State Braves",
        "polymarket_safe_name": "Alcorn State Braves",
        "polymarket_names": ["Alcorn State Braves", "Alcorn St Braves", "ALCST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Alcorn St Braves",
    },
    {
        "canonical": "Army Black Knights",
        "mascot": "Black Knights",
        "city": "West Point",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#2C2A29",

        # Polymarket
        "polymarket_id": 1920,
        "polymarket_abbreviation": "army",
        "polymarket_name": "Army Black Knights",
        "polymarket_safe_name": "Army Black Knights",
        "polymarket_names": ["Army Black Knights", "Army Knights", "ARMY"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Army Knights",
    },
    {
        "canonical": "Austin Peay Governors",
        "mascot": "Governors",
        "city": "Clarksville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C41E3A",

        # Polymarket
        "polymarket_id": 1899,
        "polymarket_abbreviation": "ausp",
        "polymarket_name": "Austin Peay Governors",
        "polymarket_safe_name": "Austin Peay Governors",
        "polymarket_names": ["Austin Peay Governors", "AUSP"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Austin Peay Governors",
    },
    {
        "canonical": "Baylor Bears",
        "mascot": "Bears",
        "city": "Waco",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#154734",

        # Polymarket
        "polymarket_id": 1767,
        "polymarket_abbreviation": "bayl",
        "polymarket_name": "Baylor Bears",
        "polymarket_safe_name": "Baylor Bears",
        "polymarket_names": ["Baylor Bears", "BAYL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Baylor Bears",
    },
    {
        "canonical": "Binghamton Bearcats",
        "mascot": "Bearcats",
        "city": "Binghamton",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#005A43",

        # Polymarket
        "polymarket_id": 1679,
        "polymarket_abbreviation": "bing",
        "polymarket_name": "Binghamton Bearcats",
        "polymarket_safe_name": "Binghamton Bearcats",
        "polymarket_names": ["Binghamton Bearcats", "BING"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Binghamton Bearcats",
    },
    {
        "canonical": "Bowling Green Falcons",
        "mascot": "Falcons",
        "city": "Bowling Green",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#FE5000",

        # Polymarket
        "polymarket_id": 1840,
        "polymarket_abbreviation": "bowlgr",
        "polymarket_name": "Bowling Green Falcons",
        "polymarket_safe_name": "Bowling Green Falcons",
        "polymarket_names": ["Bowling Green Falcons", "BOWLGR"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Bowling Green Falcons",
    },
    {
        "canonical": "Butler Bulldogs",
        "mascot": "Bulldogs",
        "city": "Indianapolis",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#20457E",

        # Polymarket
        "polymarket_id": 1723,
        "polymarket_abbreviation": "butl",
        "polymarket_name": "Butler Bulldogs",
        "polymarket_safe_name": "Butler Bulldogs",
        "polymarket_names": ["Butler Bulldogs", "BUTL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Butler Bulldogs",
    },
    {
        "canonical": "Cal Poly Mustangs",
        "mascot": "Mustangs",
        "city": "San Luis Obispo",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#154734",

        # Polymarket
        "polymarket_id": 1781,
        "polymarket_abbreviation": "calpol",
        "polymarket_name": "Cal Poly Mustangs",
        "polymarket_safe_name": "Cal Poly Mustangs",
        "polymarket_names": ["Cal Poly Mustangs", "CALPOL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Cal Poly Mustangs",
    },
    {
        "canonical": "California Golden Bears",
        "mascot": "Golden Bears",
        "city": "Berkeley",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#D6A51F",

        # Polymarket
        "polymarket_id": 1908,
        "polymarket_abbreviation": "cah",
        "polymarket_name": "California Golden Bears",
        "polymarket_safe_name": "California Golden Bears",
        "polymarket_names": ["California Golden Bears", "CAH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "California Golden Bears",
    },
    {
        "canonical": "Charleston Cougars",
        "mascot": "Cougars",
        "city": "Charleston",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#8D2042",

        # Polymarket
        "polymarket_id": 1788,
        "polymarket_abbreviation": "char",
        "polymarket_name": "Charleston Cougars",
        "polymarket_safe_name": "Charleston Cougars",
        "polymarket_names": ["Charleston Cougars", "CHAR"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Charleston Cougars",
    },
    {
        "canonical": "Charleston Southern Buccaneers",
        "mascot": "Buccaneers",
        "city": "North Charleston",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0C2340",

        # Polymarket
        "polymarket_id": 1747,
        "polymarket_abbreviation": "chsou",
        "polymarket_name": "Charleston Southern Buccaneers",
        "polymarket_safe_name": "Charleston Southern Buccaneers",
        "polymarket_names": ["Charleston Southern Buccaneers", "CHSOU"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Charleston Southern Buccaneers",
    },
    {
        "canonical": "Charlotte 49ers",
        "mascot": "49ers",
        "city": "Charlotte",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#005035",

        # Polymarket
        "polymarket_id": 1801,
        "polymarket_abbreviation": "charlt",
        "polymarket_name": "Charlotte 49ers",
        "polymarket_safe_name": "Charlotte 49ers",
        "polymarket_names": ["Charlotte 49ers", "CHARLT"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Charlotte 49ers",
    },
    {
        "canonical": "Cincinnati Bearcats",
        "mascot": "Bearcats",
        "city": "Cincinnati",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#E00122",

        # Polymarket
        "polymarket_id": 1664,
        "polymarket_abbreviation": "cin",
        "polymarket_name": "Cincinnati Bearcats",
        "polymarket_safe_name": "Cincinnati Bearcats",
        "polymarket_names": ["Cincinnati Bearcats", "CIN"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Cincinnati Bearcats",
    },
    {
        "canonical": "Cleveland State Vikings",
        "mascot": "Vikings",
        "city": "Cleveland",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#006A4D",

        # Polymarket
        "polymarket_id": 1815,
        "polymarket_abbreviation": "clvst",
        "polymarket_name": "Cleveland State Vikings",
        "polymarket_safe_name": "Cleveland State Vikings",
        "polymarket_names": ["Cleveland State Vikings", "Cleveland St Vikings", "CLVST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Cleveland St Vikings",
    },
    {
        "canonical": "Colgate Raiders",
        "mascot": "Raiders",
        "city": "Hamilton",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#862633",

        # Polymarket
        "polymarket_id": 1918,
        "polymarket_abbreviation": "colg",
        "polymarket_name": "Colgate Raiders",
        "polymarket_safe_name": "Colgate Raiders",
        "polymarket_names": ["Colgate Raiders", "COLG"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Colgate Raiders",
    },
    {
        "canonical": "Columbia Lions",
        "mascot": "Lions",
        "city": "New York",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#60A9D2",

        # Polymarket
        "polymarket_id": 1818,
        "polymarket_abbreviation": "colmb",
        "polymarket_name": "Columbia Lions",
        "polymarket_safe_name": "Columbia Lions",
        "polymarket_names": ["Columbia Lions", "COLMB"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Columbia Lions",
    },
    {
        "canonical": "Cornell Big Red",
        "mascot": "Big Red",
        "city": "Ithaca",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#B31B1B",

        # Polymarket
        "polymarket_id": 1821,
        "polymarket_abbreviation": "cornel",
        "polymarket_name": "Cornell Big Red",
        "polymarket_safe_name": "Cornell Big Red",
        "polymarket_names": ["Cornell Big Red", "CORNEL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Cornell Big Red",
    },
    {
        "canonical": "Creighton Bluejays",
        "mascot": "Bluejays",
        "city": "Omaha",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0054A6",

        # Polymarket
        "polymarket_id": 1720,
        "polymarket_abbreviation": "creigh",
        "polymarket_name": "Creighton Bluejays",
        "polymarket_safe_name": "Creighton Bluejays",
        "polymarket_names": ["Creighton Bluejays", "CREIGH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Creighton Bluejays",
    },
    {
        "canonical": "Drake Bulldogs",
        "mascot": "Bulldogs",
        "city": "Des Moines",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#004477",

        # Polymarket
        "polymarket_id": 1869,
        "polymarket_abbreviation": "drake",
        "polymarket_name": "Drake Bulldogs",
        "polymarket_safe_name": "Drake Bulldogs",
        "polymarket_names": ["Drake Bulldogs", "DRAKE"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Drake Bulldogs",
    },
    {
        "canonical": "Duquesne Dukes",
        "mascot": "Dukes",
        "city": "Pittsburgh",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#041E42",

        # Polymarket
        "polymarket_id": 1710,
        "polymarket_abbreviation": "duq",
        "polymarket_name": "Duquesne Dukes",
        "polymarket_safe_name": "Duquesne Dukes",
        "polymarket_names": ["Duquesne Dukes", "DUQ"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Duquesne Dukes",
    },
    {
        "canonical": "East Carolina Pirates",
        "mascot": "Pirates",
        "city": "Greenville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#592A8A",

        # Polymarket
        "polymarket_id": 1669,
        "polymarket_abbreviation": "ecar",
        "polymarket_name": "East Carolina Pirates",
        "polymarket_safe_name": "East Carolina Pirates",
        "polymarket_names": ["East Carolina Pirates", "ECAR"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "East Carolina Pirates",
    },
    {
        "canonical": "Eastern Kentucky Colonels",
        "mascot": "Colonels",
        "city": "Richmond",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#861F41",

        # Polymarket
        "polymarket_id": 1894,
        "polymarket_abbreviation": "ekent",
        "polymarket_name": "Eastern Kentucky Colonels",
        "polymarket_safe_name": "Eastern Kentucky Colonels",
        "polymarket_names": ["Eastern Kentucky Colonels", "EKENT"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Eastern Kentucky Colonels",
    },
    {
        "canonical": "Fairleigh Dickinson Knights",
        "mascot": "Knights",
        "city": "Teaneck",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#72293C",

        # Polymarket
        "polymarket_id": 1882,
        "polymarket_abbreviation": "fairdk",
        "polymarket_name": "Fairleigh Dickinson Knights",
        "polymarket_safe_name": "Fairleigh Dickinson Knights",
        "polymarket_names": ["Fairleigh Dickinson Knights", "FAIRDK"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Fairleigh Dickinson Knights",
    },
    {
        "canonical": "Florida Gulf Coast Eagles",
        "mascot": "Eagles",
        "city": "Fort Myers",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#004F94",

        # Polymarket
        "polymarket_id": 1697,
        "polymarket_abbreviation": "flgc",
        "polymarket_name": "Florida Gulf Coast Eagles",
        "polymarket_safe_name": "Florida Gulf Coast Eagles",
        "polymarket_names": ["Florida Gulf Coast Eagles", "FLGC"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Florida Gulf Coast Eagles",
    },
    {
        "canonical": "Florida International Golden Panthers",
        "mascot": "Golden Panthers",
        "city": "Miami",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#002D62",

        # Polymarket
        "polymarket_id": 1799,
        "polymarket_abbreviation": "flint",
        "polymarket_name": "Florida International Golden Panthers",
        "polymarket_safe_name": "Florida International Panthers",
        "polymarket_names": ["Florida International Golden Panthers", "Florida International Panthers", "Florida Int'l Golden Panthers", "FLINT"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Florida Int'l Golden Panthers",
    },
    {
        "canonical": "Florida State Seminoles",
        "mascot": "Seminoles",
        "city": "Tallahassee",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#782F40",

        # Polymarket
        "polymarket_id": 1688,
        "polymarket_abbreviation": "flst",
        "polymarket_name": "Florida State Seminoles",
        "polymarket_safe_name": "Florida State Seminoles",
        "polymarket_names": ["Florida State Seminoles", "Florida St Seminoles", "FLST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Florida St Seminoles",
    },
    {
        "canonical": "Fresno State Bulldogs",
        "mascot": "Bulldogs",
        "city": "Fresno",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#CC0033",

        # Polymarket
        "polymarket_id": 1871,
        "polymarket_abbreviation": "frest",
        "polymarket_name": "Fresno State Bulldogs",
        "polymarket_safe_name": "Fresno State Bulldogs",
        "polymarket_names": ["Fresno State Bulldogs", "Fresno St Bulldogs", "FREST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Fresno St Bulldogs",
    },
    {
        "canonical": "Furman Paladins",
        "mascot": "Paladins",
        "city": "Greenville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#582C83",

        # Polymarket
        "polymarket_id": 1940,
        "polymarket_abbreviation": "furman",
        "polymarket_name": "Furman Paladins",
        "polymarket_safe_name": "Furman Paladins",
        "polymarket_names": ["Furman Paladins", "FURMAN"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Furman Paladins",
    },
    {
        "canonical": "Georgetown Hoyas",
        "mascot": "Hoyas",
        "city": "Washington",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#094290",

        # Polymarket
        "polymarket_id": 1721,
        "polymarket_abbreviation": "george",
        "polymarket_name": "Georgetown Hoyas",
        "polymarket_safe_name": "Georgetown Hoyas",
        "polymarket_names": ["Georgetown Hoyas", "GEORGE"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Georgetown Hoyas",
    },
    {
        "canonical": "Georgia Southern Eagles",
        "mascot": "Eagles",
        "city": "Statesboro",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003775",

        # Polymarket
        "polymarket_id": 1986,
        "polymarket_abbreviation": "gas",
        "polymarket_name": "Georgia Southern Eagles",
        "polymarket_safe_name": "Georgia Southern Eagles",
        "polymarket_names": ["Georgia Southern Eagles", "GAS"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Georgia Southern Eagles",
    },
    {
        "canonical": "Georgia State Panthers",
        "mascot": "Panthers",
        "city": "Atlanta",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0039A6",

        # Polymarket
        "polymarket_id": 1985,
        "polymarket_abbreviation": "gast",
        "polymarket_name": "Georgia State Panthers",
        "polymarket_safe_name": "Georgia State Panthers",
        "polymarket_names": ["Georgia State Panthers", "Georgia St Panthers", "GAST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Georgia St Panthers",
    },
    {
        "canonical": "Grand Canyon Antelopes",
        "mascot": "Antelopes",
        "city": "Phoenix",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#522398",

        # Polymarket
        "polymarket_id": 2002,
        "polymarket_abbreviation": "gcan",
        "polymarket_name": "Grand Canyon Antelopes",
        "polymarket_safe_name": "Grand Canyon Lopes",
        "polymarket_names": ["Grand Canyon Antelopes", "Grand Canyon Lopes", "GCAN"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Grand Canyon Antelopes",
    },
    {
        "canonical": "Green Bay Phoenix",
        "mascot": "Phoenix",
        "city": "Green Bay",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0F5640",

        # Polymarket
        "polymarket_id": 1811,
        "polymarket_abbreviation": "gb",
        "polymarket_name": "Green Bay Phoenix",
        "polymarket_safe_name": "Green Bay Phoenix",
        "polymarket_names": ["Green Bay Phoenix", "GB"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Green Bay Phoenix",
    },
    {
        "canonical": "Hampton Pirates",
        "mascot": "Pirates",
        "city": "Hampton",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#004AAD",

        # Polymarket
        "polymarket_id": 1848,
        "polymarket_abbreviation": "hamp",
        "polymarket_name": "Hampton Pirates",
        "polymarket_safe_name": "Hampton Pirates",
        "polymarket_names": ["Hampton Pirates", "HAMP"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Hampton Pirates",
    },
    {
        "canonical": "Houston Christian Huskies",
        "mascot": "Huskies",
        "city": "Houston",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#273A80",

        # Polymarket
        "polymarket_id": 1950,
        "polymarket_abbreviation": "houbap",
        "polymarket_name": "Houston Christian Huskies",
        "polymarket_safe_name": "Houston Christian Huskies",
        "polymarket_names": ["Houston Christian Huskies", "HOUBAP"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Houston Christian Huskies",
    },
    {
        "canonical": "Idaho State Bengals",
        "mascot": "Bengals",
        "city": "Pocatello",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#FF671F",

        # Polymarket
        "polymarket_id": 1731,
        "polymarket_abbreviation": "idhst",
        "polymarket_name": "Idaho State Bengals",
        "polymarket_safe_name": "Idaho State Bengals",
        "polymarket_names": ["Idaho State Bengals", "IDHST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Idaho State Bengals",
    },
    {
        "canonical": "Idaho Vandals",
        "mascot": "Vandals",
        "city": "Moscow",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#F1B300",

        # Polymarket
        "polymarket_id": 1732,
        "polymarket_abbreviation": "idaho",
        "polymarket_name": "Idaho Vandals",
        "polymarket_safe_name": "Idaho Vandals",
        "polymarket_names": ["Idaho Vandals", "IDAHO"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Idaho Vandals",
    },
    {
        "canonical": "Iowa State Cyclones",
        "mascot": "Cyclones",
        "city": "Ames",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C8102E",

        # Polymarket
        "polymarket_id": 1769,
        "polymarket_abbreviation": "iowast",
        "polymarket_name": "Iowa State Cyclones",
        "polymarket_safe_name": "Iowa State Cyclones",
        "polymarket_names": ["Iowa State Cyclones", "IOWAST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Iowa State Cyclones",
    },
    {
        "canonical": "Kansas Jayhawks",
        "mascot": "Jayhawks",
        "city": "Lawrence",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0051BA",

        # Polymarket
        "polymarket_id": 1765,
        "polymarket_abbreviation": "kan",
        "polymarket_name": "Kansas Jayhawks",
        "polymarket_safe_name": "Kansas Jayhawks",
        "polymarket_names": ["Kansas Jayhawks", "KAN"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Kansas Jayhawks",
    },
    {
        "canonical": "Kansas State Wildcats",
        "mascot": "Wildcats",
        "city": "Manhattan",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#512888",

        # Polymarket
        "polymarket_id": 1771,
        "polymarket_abbreviation": "kanst",
        "polymarket_name": "Kansas State Wildcats",
        "polymarket_safe_name": "Kansas State Wildcats",
        "polymarket_names": ["Kansas State Wildcats", "Kansas St Wildcats", "KANST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Kansas St Wildcats",
    },
    {
        "canonical": "Lehigh Mountain Hawks",
        "mascot": "Mountain Hawks",
        "city": "Bethlehem",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#502D0E",

        # Polymarket
        "polymarket_id": 1917,
        "polymarket_abbreviation": "lehi",
        "polymarket_name": "Lehigh Mountain Hawks",
        "polymarket_safe_name": "Lehigh Mountain Hawks",
        "polymarket_names": ["Lehigh Mountain Hawks", "LEHI"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Lehigh Mountain Hawks",
    },
    {
        "canonical": "Lipscomb Bisons",
        "mascot": "Bisons",
        "city": "Nashville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#402669",

        # Polymarket
        "polymarket_id": 1699,
        "polymarket_abbreviation": "lipsc",
        "polymarket_name": "Lipscomb Bisons",
        "polymarket_safe_name": "Lipscomb Bisons",
        "polymarket_names": ["Lipscomb Bisons", "LIPSC"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Lipscomb Bisons",
    },
    {
        "canonical": "Louisiana Ragin' Cajuns",
        "mascot": "Ragin' Cajuns",
        "city": "Lafayette",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#CE181E",

        # Polymarket
        "polymarket_id": 1981,
        "polymarket_abbreviation": "loulaf",
        "polymarket_name": "Louisiana-Lafayette Ragin' Cajuns",
        "polymarket_safe_name": "Louisiana Ragin' Cajuns",
        "polymarket_names": ["Louisiana-Lafayette Ragin' Cajuns", "Louisiana Ragin' Cajuns", "LOULAF"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Louisiana Ragin' Cajuns",
    },
    {
        "canonical": "Maine Black Bears",
        "mascot": "Black Bears",
        "city": "Orono",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003263",

        # Polymarket
        "polymarket_id": 1677,
        "polymarket_abbreviation": "maine",
        "polymarket_name": "Maine Black Bears",
        "polymarket_safe_name": "Maine Black Bears",
        "polymarket_names": ["Maine Black Bears", "MAINE"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Maine Black Bears",
    },
    {
        "canonical": "McNeese Cowboys",
        "mascot": "Cowboys",
        "city": "Lake Charles",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#00477F",

        # Polymarket
        "polymarket_id": 1956,
        "polymarket_abbreviation": "mcnst",
        "polymarket_name": "McNeese State Cowboys",
        "polymarket_safe_name": "McNeese Cowboys",
        "polymarket_names": ["McNeese State Cowboys", "McNeese Cowboys", "MCNST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "McNeese Cowboys",
    },
    {
        "canonical": "Minnesota Golden Gophers",
        "mascot": "Golden Gophers",
        "city": "Minneapolis",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#660000",

        # Polymarket
        "polymarket_id": 1763,
        "polymarket_abbreviation": "minnst",
        "polymarket_name": "Minnesota Golden Gophers",
        "polymarket_safe_name": "Minnesota Golden Gophers",
        "polymarket_names": ["Minnesota Golden Gophers", "MINNST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Minnesota Golden Gophers",
    },
    {
        "canonical": "Monmouth Hawks",
        "mascot": "Hawks",
        "city": "West Long Branch",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0A2240",

        # Polymarket
        "polymarket_id": 1825,
        "polymarket_abbreviation": "monm",
        "polymarket_name": "Monmouth Hawks",
        "polymarket_safe_name": "Monmouth Hawks",
        "polymarket_names": ["Monmouth Hawks", "MONM"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Monmouth Hawks",
    },
    {
        "canonical": "Mount St. Mary's Mountaineers",
        "mascot": "Mountaineers",
        "city": "Emmitsburg",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#84754E",

        # Polymarket
        "polymarket_id": 1884,
        "polymarket_abbreviation": "mstm",
        "polymarket_name": "Mount St. Mary's Mountaineers",
        "polymarket_safe_name": "Mount St. Mary's Mountaineers",
        "polymarket_names": ["Mount St. Mary's Mountaineers", "Mt. St. Mary's Mountaineers", "MSTM"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Mt. St. Mary's Mountaineers",
    },
    {
        "canonical": "New Mexico Lobos",
        "mascot": "Lobos",
        "city": "Albuquerque",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C10230",

        # Polymarket
        "polymarket_id": 1872,
        "polymarket_abbreviation": "nmx",
        "polymarket_name": "New Mexico Lobos",
        "polymarket_safe_name": "New Mexico Lobos",
        "polymarket_names": ["New Mexico Lobos", "NMX"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "New Mexico Lobos",
    },
    {
        "canonical": "North Dakota State Bison",
        "mascot": "Bison",
        "city": "Fargo",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0A5640",

        # Polymarket
        "polymarket_id": 1975,
        "polymarket_abbreviation": "ndkst",
        "polymarket_name": "North Dakota State Bison",
        "polymarket_safe_name": "North Dakota State Bison",
        "polymarket_names": ["North Dakota State Bison", "North Dakota St Bison", "NDKST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "North Dakota St Bison",
    },
    {
        "canonical": "Northwestern Wildcats",
        "mascot": "Wildcats",
        "city": "Evanston",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#4E2A84",

        # Polymarket
        "polymarket_id": 1759,
        "polymarket_abbreviation": "nw",
        "polymarket_name": "Northwestern Wildcats",
        "polymarket_safe_name": "Northwestern Wildcats",
        "polymarket_names": ["Northwestern Wildcats", "NW"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Northwestern Wildcats",
    },
    {
        "canonical": "Oakland Golden Grizzlies",
        "mascot": "Golden Grizzlies",
        "city": "Rochester",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#B09655",

        # Polymarket
        "polymarket_id": 1808,
        "polymarket_abbreviation": "oak",
        "polymarket_name": "Oakland Golden Grizzlies",
        "polymarket_safe_name": "Oakland Golden Grizzlies",
        "polymarket_names": ["Oakland Golden Grizzlies", "OAK"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Oakland Golden Grizzlies",
    },
    {
        "canonical": "Ohio Bobcats",
        "mascot": "Bobcats",
        "city": "Athens",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#00694E",

        # Polymarket
        "polymarket_id": 1839,
        "polymarket_abbreviation": "ohio",
        "polymarket_name": "Ohio Bobcats",
        "polymarket_safe_name": "Ohio Bobcats",
        "polymarket_names": ["Ohio Bobcats", "OHIO"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Ohio Bobcats",
    },
    {
        "canonical": "Oklahoma Sooners",
        "mascot": "Sooners",
        "city": "Norman",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#841617",

        # Polymarket
        "polymarket_id": 1764,
        "polymarket_abbreviation": "okl",
        "polymarket_name": "Oklahoma Sooners",
        "polymarket_safe_name": "Oklahoma Sooners",
        "polymarket_names": ["Oklahoma Sooners", "OKL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Oklahoma Sooners",
    },
    {
        "canonical": "Oklahoma State Cowboys",
        "mascot": "Cowboys",
        "city": "Stillwater",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#FF7300",

        # Polymarket
        "polymarket_id": 1772,
        "polymarket_abbreviation": "okst",
        "polymarket_name": "Oklahoma State Cowboys",
        "polymarket_safe_name": "Oklahoma State Cowboys",
        "polymarket_names": ["Oklahoma State Cowboys", "Oklahoma St Cowboys", "OKST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Oklahoma St Cowboys",
    },
    {
        "canonical": "Old Dominion Monarchs",
        "mascot": "Monarchs",
        "city": "Norfolk",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003087",

        # Polymarket
        "polymarket_id": 1797,
        "polymarket_abbreviation": "old",
        "polymarket_name": "Old Dominion Monarchs",
        "polymarket_safe_name": "Old Dominion Monarchs",
        "polymarket_names": ["Old Dominion Monarchs", "OLD"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Old Dominion Monarchs",
    },
    {
        "canonical": "Oral Roberts Golden Eagles",
        "mascot": "Golden Eagles",
        "city": "Tulsa",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003EA8",

        # Polymarket
        "polymarket_id": 1977,
        "polymarket_abbreviation": "oral",
        "polymarket_name": "Oral Roberts Golden Eagles",
        "polymarket_safe_name": "Oral Roberts Golden Eagles",
        "polymarket_names": ["Oral Roberts Golden Eagles", "ORAL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Oral Roberts Golden Eagles",
    },
    {
        "canonical": "Oregon Ducks",
        "mascot": "Ducks",
        "city": "Eugene",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#154733",

        # Polymarket
        "polymarket_id": 1902,
        "polymarket_abbreviation": "ore",
        "polymarket_name": "Oregon Ducks",
        "polymarket_safe_name": "Oregon Ducks",
        "polymarket_names": ["Oregon Ducks", "ORE"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Oregon Ducks",
    },
    {
        "canonical": "Oregon State Beavers",
        "mascot": "Beavers",
        "city": "Corvallis",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#DC4405",

        # Polymarket
        "polymarket_id": 1909,
        "polymarket_abbreviation": "oregst",
        "polymarket_name": "Oregon State Beavers",
        "polymarket_safe_name": "Oregon State Beavers",
        "polymarket_names": ["Oregon State Beavers", "Oregon St Beavers", "OREGST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Oregon St Beavers",
    },
    {
        "canonical": "Penn Quakers",
        "mascot": "Quakers",
        "city": "Philadelphia",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#990000",

        # Polymarket
        "polymarket_id": 1820,
        "polymarket_abbreviation": "penn",
        "polymarket_name": "Penn Quakers",
        "polymarket_safe_name": "Pennsylvania Quakers",
        "polymarket_names": ["Penn Quakers", "Pennsylvania Quakers", "PENN"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Pennsylvania Quakers",
    },
    {
        "canonical": "Penn State Nittany Lions",
        "mascot": "Nittany Lions",
        "city": "University Park",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003A73",

        # Polymarket
        "polymarket_id": 1760,
        "polymarket_abbreviation": "pennst",
        "polymarket_name": "Penn State Nittany Lions",
        "polymarket_safe_name": "Penn State Nittany Lions",
        "polymarket_names": ["Penn State Nittany Lions", "PENNST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Penn State Nittany Lions",
    },
    {
        "canonical": "Pepperdine Waves",
        "mascot": "Waves",
        "city": "Malibu",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#EE7624",

        # Polymarket
        "polymarket_id": 1994,
        "polymarket_abbreviation": "pepp",
        "polymarket_name": "Pepperdine Waves",
        "polymarket_safe_name": "Pepperdine Waves",
        "polymarket_names": ["Pepperdine Waves", "PEPP"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Pepperdine Waves",
    },
    {
        "canonical": "Pittsburgh Panthers",
        "mascot": "Panthers",
        "city": "Pittsburgh",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003594",

        # Polymarket
        "polymarket_id": 1687,
        "polymarket_abbreviation": "pitt",
        "polymarket_name": "Pittsburgh Panthers",
        "polymarket_safe_name": "Pittsburgh Panthers",
        "polymarket_names": ["Pittsburgh Panthers", "PITT"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Pittsburgh Panthers",
    },
    {
        "canonical": "Portland Pilots",
        "mascot": "Pilots",
        "city": "Portland",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#5900C7",

        # Polymarket
        "polymarket_id": 1997,
        "polymarket_abbreviation": "port",
        "polymarket_name": "Portland Pilots",
        "polymarket_safe_name": "Portland Pilots",
        "polymarket_names": ["Portland Pilots", "PORT"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Portland Pilots",
    },
    {
        "canonical": "Portland State Vikings",
        "mascot": "Vikings",
        "city": "Portland",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#154734",

        # Polymarket
        "polymarket_id": 1735,
        "polymarket_abbreviation": "portst",
        "polymarket_name": "Portland State Vikings",
        "polymarket_safe_name": "Portland State Vikings",
        "polymarket_names": ["Portland State Vikings", "Portland St Vikings", "PORTST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Portland St Vikings",
    },
    {
        "canonical": "Prairie View A&M Panthers",
        "mascot": "Panthers",
        "city": "Prairie View",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#582C83",

        # Polymarket
        "polymarket_id": 1970,
        "polymarket_abbreviation": "pvam",
        "polymarket_name": "Prairie View A&M Panthers",
        "polymarket_safe_name": "Prairie View A&M Panthers",
        "polymarket_names": ["Prairie View A&M Panthers", "Prairie View Panthers", "PVAM"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Prairie View Panthers",
    },
    {
        "canonical": "Princeton Tigers",
        "mascot": "Tigers",
        "city": "Princeton",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#FF671F",

        # Polymarket
        "polymarket_id": 1819,
        "polymarket_abbreviation": "prnce",
        "polymarket_name": "Princeton Tigers",
        "polymarket_safe_name": "Princeton Tigers",
        "polymarket_names": ["Princeton Tigers", "PRNCE"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Princeton Tigers",
    },
    {
        "canonical": "Providence Friars",
        "mascot": "Friars",
        "city": "Providence",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#808080",

        # Polymarket
        "polymarket_id": 1722,
        "polymarket_abbreviation": "prov",
        "polymarket_name": "Providence Friars",
        "polymarket_safe_name": "Providence Friars",
        "polymarket_names": ["Providence Friars", "PROV"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Providence Friars",
    },
    {
        "canonical": "Quinnipiac Bobcats",
        "mascot": "Bobcats",
        "city": "Hamden",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#154684",

        # Polymarket
        "polymarket_id": 1833,
        "polymarket_abbreviation": "quin",
        "polymarket_name": "Quinnipiac Bobcats",
        "polymarket_safe_name": "Quinnipiac Bobcats",
        "polymarket_names": ["Quinnipiac Bobcats", "QUIN"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Quinnipiac Bobcats",
    },
    {
        "canonical": "Rhode Island Rams",
        "mascot": "Rams",
        "city": "Kingston",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#75B2DD",

        # Polymarket
        "polymarket_id": 1709,
        "polymarket_abbreviation": "ri",
        "polymarket_name": "Rhode Island Rams",
        "polymarket_safe_name": "Rhode Island Rams",
        "polymarket_names": ["Rhode Island Rams", "RI"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Rhode Island Rams",
    },
    {
        "canonical": "Rice Owls",
        "mascot": "Owls",
        "city": "Houston",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#00205B",

        # Polymarket
        "polymarket_id": 1805,
        "polymarket_abbreviation": "rice",
        "polymarket_name": "Rice Owls",
        "polymarket_safe_name": "Rice Owls",
        "polymarket_names": ["Rice Owls", "RICE"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Rice Owls",
    },
    {
        "canonical": "Richmond Spiders",
        "mascot": "Spiders",
        "city": "Richmond",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#BA0C2F",

        # Polymarket
        "polymarket_id": 1711,
        "polymarket_abbreviation": "rich",
        "polymarket_name": "Richmond Spiders",
        "polymarket_safe_name": "Richmond Spiders",
        "polymarket_names": ["Richmond Spiders", "RICH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Richmond Spiders",
    },
    {
        "canonical": "Rider Broncs",
        "mascot": "Broncs",
        "city": "Lawrenceville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#981E32",

        # Polymarket
        "polymarket_id": 1832,
        "polymarket_abbreviation": "rider",
        "polymarket_name": "Rider Broncs",
        "polymarket_safe_name": "Rider Broncs",
        "polymarket_names": ["Rider Broncs", "RIDER"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Rider Broncs",
    },
    {
        "canonical": "SIU Edwardsville Cougars",
        "mascot": "Cougars",
        "city": "Edwardsville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#D81E05",

        # Polymarket
        "polymarket_id": 1901,
        "polymarket_abbreviation": "siue",
        "polymarket_name": "SIUE Cougars",
        "polymarket_safe_name": "SIU Edwardsville Cougars",
        "polymarket_names": ["SIUE Cougars", "SIU Edwardsville Cougars", "SIU-Edwardsville Cougars", "SIUE"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "SIU-Edwardsville Cougars",
    },
    {
        "canonical": "SMU Mustangs",
        "mascot": "Mustangs",
        "city": "Dallas",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C8102E",

        # Polymarket
        "polymarket_id": 1661,
        "polymarket_abbreviation": "smu",
        "polymarket_name": "SMU Mustangs",
        "polymarket_safe_name": "SMU Mustangs",
        "polymarket_names": ["SMU Mustangs", "SMU"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "SMU Mustangs",
    },
    {
        "canonical": "Sacramento State Hornets",
        "mascot": "Hornets",
        "city": "Sacramento",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#043927",

        # Polymarket
        "polymarket_id": 1736,
        "polymarket_abbreviation": "sacst",
        "polymarket_name": "Sacramento State Hornets",
        "polymarket_safe_name": "Sacramento State Hornets",
        "polymarket_names": ["Sacramento State Hornets", "Sacramento St Hornets", "SACST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Sacramento St Hornets",
    },
    {
        "canonical": "Sacred Heart Pioneers",
        "mascot": "Pioneers",
        "city": "Fairfield",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#CE1141",

        # Polymarket
        "polymarket_id": 1885,
        "polymarket_abbreviation": "sacred",
        "polymarket_name": "Sacred Heart Pioneers",
        "polymarket_safe_name": "Sacred Heart Pioneers",
        "polymarket_names": ["Sacred Heart Pioneers", "SACRED"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Sacred Heart Pioneers",
    },
    {
        "canonical": "Saint Louis Billikens",
        "mascot": "Billikens",
        "city": "St. Louis",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003DA5",

        # Polymarket
        "polymarket_id": 1713,
        "polymarket_abbreviation": "stlou",
        "polymarket_name": "Saint Louis Billikens",
        "polymarket_safe_name": "Saint Louis Billikens",
        "polymarket_names": ["Saint Louis Billikens", "STLOU"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Saint Louis Billikens",
    },
    {
        "canonical": "Sam Houston Bearkats",
        "mascot": "Bearkats",
        "city": "Huntsville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#F77F00",

        # Polymarket
        "polymarket_id": 1952,
        "polymarket_abbreviation": "smho",
        "polymarket_name": "Sam Houston Bearkats",
        "polymarket_safe_name": "Sam Houston Bearkats",
        "polymarket_names": ["Sam Houston Bearkats", "Sam Houston St Bearkats", "SMHO"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Sam Houston St Bearkats",
    },
    {
        "canonical": "San Diego State Aztecs",
        "mascot": "Aztecs",
        "city": "San Diego",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C41230",

        # Polymarket
        "polymarket_id": 1870,
        "polymarket_abbreviation": "sdst",
        "polymarket_name": "San Diego State Aztecs",
        "polymarket_safe_name": "San Diego State Aztecs",
        "polymarket_names": ["San Diego State Aztecs", "San Diego St Aztecs", "SDST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "San Diego St Aztecs",
    },
    {
        "canonical": "Santa Clara Broncos",
        "mascot": "Broncos",
        "city": "Santa Clara",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#862633",

        # Polymarket
        "polymarket_id": 1998,
        "polymarket_abbreviation": "sanclr",
        "polymarket_name": "Santa Clara Broncos",
        "polymarket_safe_name": "Santa Clara Broncos",
        "polymarket_names": ["Santa Clara Broncos", "SANCLR"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Santa Clara Broncos",
    },
    {
        "canonical": "Seattle Redhawks",
        "mascot": "Redhawks",
        "city": "Seattle",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#AA0000",

        # Polymarket
        "polymarket_id": 2004,
        "polymarket_abbreviation": "sea",
        "polymarket_name": "Seattle Redhawks",
        "polymarket_safe_name": "Seattle U Redhawks",
        "polymarket_names": ["Seattle Redhawks", "Seattle U Redhawks", "SEA"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Seattle Redhawks",
    },
    {
        "canonical": "South Carolina State Bulldogs",
        "mascot": "Bulldogs",
        "city": "Orangeburg",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#862633",

        # Polymarket
        "polymarket_id": 1849,
        "polymarket_abbreviation": "scarst",
        "polymarket_name": "South Carolina State Bulldogs",
        "polymarket_safe_name": "South Carolina State Bulldogs",
        "polymarket_names": ["South Carolina State Bulldogs", "South Carolina St Bulldogs", "SCARST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "South Carolina St Bulldogs",
    },
    {
        "canonical": "Southeastern Louisiana Lions",
        "mascot": "Lions",
        "city": "Hammond",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#046A38",

        # Polymarket
        "polymarket_id": 1957,
        "polymarket_abbreviation": "selou",
        "polymarket_name": "Southeastern Louisiana Lions",
        "polymarket_safe_name": "SE Louisiana Lions",
        "polymarket_names": ["Southeastern Louisiana Lions", "SE Louisiana Lions", "SELOU"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "SE Louisiana Lions",
    },
    {
        "canonical": "Southern Utah Thunderbirds",
        "mascot": "Thunderbirds",
        "city": "Cedar City",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#DB0000",

        # Polymarket
        "polymarket_id": 1737,
        "polymarket_abbreviation": "sutah",
        "polymarket_name": "Southern Utah Thunderbirds",
        "polymarket_safe_name": "Southern Utah Thunderbirds",
        "polymarket_names": ["Southern Utah Thunderbirds", "SUTAH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Southern Utah Thunderbirds",
    },
    {
        "canonical": "St. Francis (PA) Red Flash",
        "mascot": "Red Flash",
        "city": "Loretto",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C8102E",

        # Polymarket
        "polymarket_id": 1883,
        "polymarket_abbreviation": "stfpa",
        "polymarket_name": "St. Francis (PA) Red Flash",
        "polymarket_safe_name": "Saint Francis Red Flash",
        "polymarket_names": ["St. Francis (PA) Red Flash", "Saint Francis Red Flash", "STFPA"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "St. Francis (PA) Red Flash",
    },
    {
        "canonical": "St. John's Red Storm",
        "mascot": "Red Storm",
        "city": "Queens",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C3002F",

        # Polymarket
        "polymarket_id": 1726,
        "polymarket_abbreviation": "stjohn",
        "polymarket_name": "St. John's Red Storm",
        "polymarket_safe_name": "St. John's Red Storm",
        "polymarket_names": ["St. John's Red Storm", "STJOHN"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "St. John's Red Storm",
    },
    {
        "canonical": "Stony Brook Seawolves",
        "mascot": "Seawolves",
        "city": "Stony Brook",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#990000",

        # Polymarket
        "polymarket_id": 1672,
        "polymarket_abbreviation": "stbr",
        "polymarket_name": "Stony Brook Seawolves",
        "polymarket_safe_name": "Stony Brook Seawolves",
        "polymarket_names": ["Stony Brook Seawolves", "STBR"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Stony Brook Seawolves",
    },
    {
        "canonical": "TCU Horned Frogs",
        "mascot": "Horned Frogs",
        "city": "Fort Worth",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#4D1979",

        # Polymarket
        "polymarket_id": 1773,
        "polymarket_abbreviation": "tcu",
        "polymarket_name": "TCU Horned Frogs",
        "polymarket_safe_name": "TCU Horned Frogs",
        "polymarket_names": ["TCU Horned Frogs", "TCU"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "TCU Horned Frogs",
    },
    {
        "canonical": "Tarleton State Texans",
        "mascot": "Texans",
        "city": "Stephenville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#5A2B81",

        # Polymarket
        "polymarket_id": 2018,
        "polymarket_abbreviation": "tarl",
        "polymarket_name": "Tarleton State Texans",
        "polymarket_safe_name": "Tarleton State Texans",
        "polymarket_names": ["Tarleton State Texans", "TARL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Tarleton State Texans",
    },
    {
        "canonical": "Tennessee State Tigers",
        "mascot": "Tigers",
        "city": "Nashville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#00539F",

        # Polymarket
        "polymarket_id": 1892,
        "polymarket_abbreviation": "tenst",
        "polymarket_name": "Tennessee State Tigers",
        "polymarket_safe_name": "Tennessee State Tigers",
        "polymarket_names": ["Tennessee State Tigers", "Tennessee St Tigers", "TENST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Tennessee St Tigers",
    },
    {
        "canonical": "Tennessee Volunteers",
        "mascot": "Volunteers",
        "city": "Knoxville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#FF8200",

        # Polymarket
        "polymarket_id": 1934,
        "polymarket_abbreviation": "tenn",
        "polymarket_name": "Tennessee Volunteers",
        "polymarket_safe_name": "Tennessee Volunteers",
        "polymarket_names": ["Tennessee Volunteers", "TENN"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Tennessee Volunteers",
    },
    {
        "canonical": "Texas Tech Red Raiders",
        "mascot": "Red Raiders",
        "city": "Lubbock",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#CC0000",

        # Polymarket
        "polymarket_id": 1770,
        "polymarket_abbreviation": "txtech",
        "polymarket_name": "Texas Tech Red Raiders",
        "polymarket_safe_name": "Texas Tech Red Raiders",
        "polymarket_names": ["Texas Tech Red Raiders", "TXTECH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Texas Tech Red Raiders",
    },
    {
        "canonical": "Tulane Green Wave",
        "mascot": "Green Wave",
        "city": "New Orleans",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#006747",

        # Polymarket
        "polymarket_id": 1670,
        "polymarket_abbreviation": "tulane",
        "polymarket_name": "Tulane Green Wave",
        "polymarket_safe_name": "Tulane Green Wave",
        "polymarket_names": ["Tulane Green Wave", "TULANE"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Tulane Green Wave",
    },
    {
        "canonical": "UAB Blazers",
        "mascot": "Blazers",
        "city": "Birmingham",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#006341",

        # Polymarket
        "polymarket_id": 1793,
        "polymarket_abbreviation": "uab",
        "polymarket_name": "UAB Blazers",
        "polymarket_safe_name": "UAB Blazers",
        "polymarket_names": ["UAB Blazers", "UAB"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UAB Blazers",
    },
    {
        "canonical": "UC Irvine Anteaters",
        "mascot": "Anteaters",
        "city": "Irvine",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0064A4",

        # Polymarket
        "polymarket_id": 1775,
        "polymarket_abbreviation": "ucirv",
        "polymarket_name": "UC Irvine Anteaters",
        "polymarket_safe_name": "UC Irvine Anteaters",
        "polymarket_names": ["UC Irvine Anteaters", "UCIRV"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UC Irvine Anteaters",
    },
    {
        "canonical": "UCLA Bruins",
        "mascot": "Bruins",
        "city": "Los Angeles",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#2D68C4",

        # Polymarket
        "polymarket_id": 1910,
        "polymarket_abbreviation": "ucla",
        "polymarket_name": "UCLA Bruins",
        "polymarket_safe_name": "UCLA Bruins",
        "polymarket_names": ["UCLA Bruins", "UCLA"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UCLA Bruins",
    },
    {
        "canonical": "UIC Flames",
        "mascot": "Flames",
        "city": "Chicago",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#D50032",

        # Polymarket
        "polymarket_id": 1816,
        "polymarket_abbreviation": "illchi",
        "polymarket_name": "UIC Flames",
        "polymarket_safe_name": "UIC Flames",
        "polymarket_names": ["UIC Flames", "ILLCHI"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UIC Flames",
    },
    {
        "canonical": "VCU Rams",
        "mascot": "Rams",
        "city": "Richmond",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#DB9A00",

        # Polymarket
        "polymarket_id": 1704,
        "polymarket_abbreviation": "vcu",
        "polymarket_name": "VCU Rams",
        "polymarket_safe_name": "VCU Rams",
        "polymarket_names": ["VCU Rams", "VCU"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "VCU Rams",
    },
    {
        "canonical": "Bellarmine Knights",
        "mascot": "Knights",
        "city": "Louisville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#AD0000",

        # Polymarket
        "polymarket_id": 2019,
        "polymarket_abbreviation": "bella",
        "polymarket_name": "Bellarmine Knights",
        "polymarket_safe_name": "Bellarmine Knights",
        "polymarket_names": ["Bellarmine Knights", "BELLA"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Bellarmine Knights",
    },
    {
        "canonical": "Cal State Fullerton Titans",
        "mascot": "Titans",
        "city": "Fullerton",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#E17000",

        # Polymarket
        "polymarket_id": 1782,
        "polymarket_abbreviation": "csufl",
        "polymarket_name": "Cal State Fullerton Titans",
        "polymarket_safe_name": "Cal State Fullerton Titans",
        "polymarket_names": ["Cal State Fullerton Titans", "CSU Fullerton Titans", "CSUFL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "CSU Fullerton Titans",
    },
    {
        "canonical": "UC San Diego Tritons",
        "mascot": "Tritons",
        "city": "San Diego",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#00629B",

        # Polymarket
        "polymarket_id": 2017,
        "polymarket_abbreviation": "ucsd",
        "polymarket_name": "California-San Diego Tritons",
        "polymarket_safe_name": "UC San Diego Tritons",
        "polymarket_names": ["California-San Diego Tritons", "UC San Diego Tritons", "UCSD"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UC San Diego Tritons",
    },
    {
        "canonical": "Central Arkansas Bears",
        "mascot": "Bears",
        "city": "Conway",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#582C83",

        # Polymarket
        "polymarket_id": 1955,
        "polymarket_abbreviation": "cark",
        "polymarket_name": "Central Arkansas Bears",
        "polymarket_safe_name": "Central Arkansas Bears",
        "polymarket_names": ["Central Arkansas Bears", "CARK"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Central Arkansas Bears",
    },
    {
        "canonical": "Davidson Wildcats",
        "mascot": "Wildcats",
        "city": "Davidson",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#D42121",

        # Polymarket
        "polymarket_id": 1708,
        "polymarket_abbreviation": "david",
        "polymarket_name": "Davidson Wildcats",
        "polymarket_safe_name": "Davidson Wildcats",
        "polymarket_names": ["Davidson Wildcats", "DAVID"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Davidson Wildcats",
    },
    {
        "canonical": "Dayton Flyers",
        "mascot": "Flyers",
        "city": "Dayton",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#D70036",

        # Polymarket
        "polymarket_id": 1703,
        "polymarket_abbreviation": "day",
        "polymarket_name": "Dayton Flyers",
        "polymarket_safe_name": "Dayton Flyers",
        "polymarket_names": ["Dayton Flyers", "DAY"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Dayton Flyers",
    },
    {
        "canonical": "Delaware Blue Hens",
        "mascot": "Blue Hens",
        "city": "Newark",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#00539F",

        # Polymarket
        "polymarket_id": 1792,
        "polymarket_abbreviation": "del",
        "polymarket_name": "Delaware Fightin' Blue Hens",
        "polymarket_safe_name": "Delaware Blue Hens",
        "polymarket_names": ["Delaware Fightin' Blue Hens", "Delaware Blue Hens", "DEL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Delaware Blue Hens",
    },
    {
        "canonical": "East Texas A&M Lions",
        "mascot": "Lions",
        "city": "Commerce",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0033A0",

        # Polymarket
        "polymarket_id": 2009,
        "polymarket_abbreviation": "txamc",
        "polymarket_name": "East Texas A&M Lions",
        "polymarket_safe_name": "East Texas A&M Lions",
        "polymarket_names": ["East Texas A&M Lions", "TXAMC"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "East Texas A&M Lions",
    },
    {
        "canonical": "Eastern Michigan Eagles",
        "mascot": "Eagles",
        "city": "Ypsilanti",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#006633",

        # Polymarket
        "polymarket_id": 1846,
        "polymarket_abbreviation": "emich",
        "polymarket_name": "Eastern Michigan Eagles",
        "polymarket_safe_name": "Eastern Michigan Eagles",
        "polymarket_names": ["Eastern Michigan Eagles", "EMICH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Eastern Michigan Eagles",
    },
    {
        "canonical": "Eastern Washington Eagles",
        "mascot": "Eagles",
        "city": "Cheney",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#A10C2B",

        # Polymarket
        "polymarket_id": 1729,
        "polymarket_abbreviation": "ewash",
        "polymarket_name": "Eastern Washington Eagles",
        "polymarket_safe_name": "Eastern Washington Eagles",
        "polymarket_names": ["Eastern Washington Eagles", "EWASH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Eastern Washington Eagles",
    },
    {
        "canonical": "Fordham Rams",
        "mascot": "Rams",
        "city": "Bronx",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#862633",

        # Polymarket
        "polymarket_id": 1712,
        "polymarket_abbreviation": "fordm",
        "polymarket_name": "Fordham Rams",
        "polymarket_safe_name": "Fordham Rams",
        "polymarket_names": ["Fordham Rams", "FORDM"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Fordham Rams",
    },
    {
        "canonical": "Hawaii Rainbow Warriors",
        "mascot": "Rainbow Warriors",
        "city": "Honolulu",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#024731",

        # Polymarket
        "polymarket_id": 1774,
        "polymarket_abbreviation": "hawaii",
        "polymarket_name": "Hawaii Rainbow Warriors",
        "polymarket_safe_name": "Hawai'i Rainbow Warriors",
        "polymarket_names": ["Hawaii Rainbow Warriors", "Hawai'i Rainbow Warriors", "HAWAII"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Hawai'i Rainbow Warriors",
    },
    {
        "canonical": "Holy Cross Crusaders",
        "mascot": "Crusaders",
        "city": "Worcester",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#4E2A84",

        # Polymarket
        "polymarket_id": 1921,
        "polymarket_abbreviation": "holy",
        "polymarket_name": "Holy Cross Crusaders",
        "polymarket_safe_name": "Holy Cross Crusaders",
        "polymarket_names": ["Holy Cross Crusaders", "HOLY"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Holy Cross Crusaders",
    },
    {
        "canonical": "Illinois Fighting Illini",
        "mascot": "Fighting Illini",
        "city": "Champaign",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#E84A27",

        # Polymarket
        "polymarket_id": 1761,
        "polymarket_abbreviation": "ill",
        "polymarket_name": "Illinois Fighting Illini",
        "polymarket_safe_name": "Illinois Fighting Illini",
        "polymarket_names": ["Illinois Fighting Illini", "ILL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Illinois Fighting Illini",
    },
    {
        "canonical": "Indiana State Sycamores",
        "mascot": "Sycamores",
        "city": "Terre Haute",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0142BC",

        # Polymarket
        "polymarket_id": 1865,
        "polymarket_abbreviation": "indst",
        "polymarket_name": "Indiana State Sycamores",
        "polymarket_safe_name": "Indiana State Sycamores",
        "polymarket_names": ["Indiana State Sycamores", "Indiana St Sycamores", "INDST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Indiana St Sycamores",
    },
    {
        "canonical": "Iowa Hawkeyes",
        "mascot": "Hawkeyes",
        "city": "Iowa City",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#CFA904",

        # Polymarket
        "polymarket_id": 1750,
        "polymarket_abbreviation": "iowa",
        "polymarket_name": "Iowa Hawkeyes",
        "polymarket_safe_name": "Iowa Hawkeyes",
        "polymarket_names": ["Iowa Hawkeyes", "IOWA"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Iowa Hawkeyes",
    },
    {
        "canonical": "Jackson State Tigers",
        "mascot": "Tigers",
        "city": "Jackson",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0D2240",

        # Polymarket
        "polymarket_id": 1963,
        "polymarket_abbreviation": "jackst",
        "polymarket_name": "Jackson State Tigers",
        "polymarket_safe_name": "Jackson State Tigers",
        "polymarket_names": ["Jackson State Tigers", "Jackson St Tigers", "JACKST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Jackson St Tigers",
    },
    {
        "canonical": "Jacksonville Dolphins",
        "mascot": "Dolphins",
        "city": "Jacksonville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#005748",

        # Polymarket
        "polymarket_id": 1696,
        "polymarket_abbreviation": "jax",
        "polymarket_name": "Jacksonville Dolphins",
        "polymarket_safe_name": "Jacksonville Dolphins",
        "polymarket_names": ["Jacksonville Dolphins", "JAX"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Jacksonville Dolphins",
    },
    {
        "canonical": "Kansas City Roos",
        "mascot": "Roos",
        "city": "Kansas City",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#005EA8",

        # Polymarket
        "polymarket_id": 2008,
        "polymarket_abbreviation": "umkc",
        "polymarket_name": "Kansas City Roos",
        "polymarket_safe_name": "Kansas City Roos",
        "polymarket_names": ["Kansas City Roos", "UMKC Kangaroos", "UMKC"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UMKC Kangaroos",
    },
    {
        "canonical": "Louisiana Tech Bulldogs",
        "mascot": "Bulldogs",
        "city": "Ruston",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#002F8B",

        # Polymarket
        "polymarket_id": 1796,
        "polymarket_abbreviation": "loutch",
        "polymarket_name": "Louisiana Tech Bulldogs",
        "polymarket_safe_name": "Louisiana Tech Bulldogs",
        "polymarket_names": ["Louisiana Tech Bulldogs", "LOUTCH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Louisiana Tech Bulldogs",
    },
    {
        "canonical": "Milwaukee Panthers",
        "mascot": "Panthers",
        "city": "Milwaukee",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#DF9D02",

        # Polymarket
        "polymarket_id": 1810,
        "polymarket_abbreviation": "wbd",
        "polymarket_name": "Milwaukee Panthers",
        "polymarket_safe_name": "Milwaukee Panthers",
        "polymarket_names": ["Milwaukee Panthers", "WBD"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Milwaukee Panthers",
    },
    {
        "canonical": "New Mexico State Aggies",
        "mascot": "Aggies",
        "city": "Las Cruces",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#8F1538",

        # Polymarket
        "polymarket_id": 2001,
        "polymarket_abbreviation": "nmxst",
        "polymarket_name": "New Mexico State Aggies",
        "polymarket_safe_name": "New Mexico State Aggies",
        "polymarket_names": ["New Mexico State Aggies", "New Mexico St Aggies", "NMXST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "New Mexico St Aggies",
    },
    {
        "canonical": "Northern Illinois Huskies",
        "mascot": "Huskies",
        "city": "DeKalb",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#BA0C2E",

        # Polymarket
        "polymarket_id": 1845,
        "polymarket_abbreviation": "nill",
        "polymarket_name": "Northern Illinois Huskies",
        "polymarket_safe_name": "Northern Illinois Huskies",
        "polymarket_names": ["Northern Illinois Huskies", "NILL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Northern Illinois Huskies",
    },
    {
        "canonical": "Northwestern State Demons",
        "mascot": "Demons",
        "city": "Natchitoches",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#582C83",

        # Polymarket
        "polymarket_id": 1958,
        "polymarket_abbreviation": "nwst",
        "polymarket_name": "Northwestern State Demons",
        "polymarket_safe_name": "Northwestern State Demons",
        "polymarket_names": ["Northwestern State Demons", "Northwestern St Demons", "NWST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Northwestern St Demons",
    },
    {
        "canonical": "Robert Morris Colonials",
        "mascot": "Colonials",
        "city": "Moon Township",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#14234B",

        # Polymarket
        "polymarket_id": 1887,
        "polymarket_abbreviation": "robms",
        "polymarket_name": "Robert Morris Colonials",
        "polymarket_safe_name": "Robert Morris Colonials",
        "polymarket_names": ["Robert Morris Colonials", "ROBMS"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Robert Morris Colonials",
    },
    {
        "canonical": "Rutgers Scarlet Knights",
        "mascot": "Scarlet Knights",
        "city": "Piscataway",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#CC0033",

        # Polymarket
        "polymarket_id": 1762,
        "polymarket_abbreviation": "rutger",
        "polymarket_name": "Rutgers Scarlet Knights",
        "polymarket_safe_name": "Rutgers Scarlet Knights",
        "polymarket_names": ["Rutgers Scarlet Knights", "RUTGER"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Rutgers Scarlet Knights",
    },
    {
        "canonical": "Saint Joseph's Hawks",
        "mascot": "Hawks",
        "city": "Philadelphia",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#9E1B32",

        # Polymarket
        "polymarket_id": 1705,
        "polymarket_abbreviation": "stjoe",
        "polymarket_name": "Saint Joseph's Hawks",
        "polymarket_safe_name": "Saint Joseph's Hawks",
        "polymarket_names": ["Saint Joseph's Hawks", "STJOE"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Saint Joseph's Hawks",
    },
    {
        "canonical": "Siena Saints",
        "mascot": "Saints",
        "city": "Loudonville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#006B54",

        # Polymarket
        "polymarket_id": 1827,
        "polymarket_abbreviation": "siena",
        "polymarket_name": "Siena Saints",
        "polymarket_safe_name": "Siena Saints",
        "polymarket_names": ["Siena Saints", "SIENA"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Siena Saints",
    },
    {
        "canonical": "South Florida Bulls",
        "mascot": "Bulls",
        "city": "Tampa",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#006747",

        # Polymarket
        "polymarket_id": 1671,
        "polymarket_abbreviation": "sfl",
        "polymarket_name": "South Florida Bulls",
        "polymarket_safe_name": "South Florida Bulls",
        "polymarket_names": ["South Florida Bulls", "SFL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "South Florida Bulls",
    },
    {
        "canonical": "Southern Jaguars",
        "mascot": "Jaguars",
        "city": "Baton Rouge",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#00205B",

        # Polymarket
        "polymarket_id": 1962,
        "polymarket_abbreviation": "south",
        "polymarket_name": "Southern Jaguars",
        "polymarket_safe_name": "Southern Jaguars",
        "polymarket_names": ["Southern Jaguars", "SOUTH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Southern Jaguars",
    },
    {
        "canonical": "Southern Miss Golden Eagles",
        "mascot": "Golden Eagles",
        "city": "Hattiesburg",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#CBA041",

        # Polymarket
        "polymarket_id": 1802,
        "polymarket_abbreviation": "soumis",
        "polymarket_name": "Southern Miss Golden Eagles",
        "polymarket_safe_name": "Southern Miss Golden Eagles",
        "polymarket_names": ["Southern Miss Golden Eagles", "SOUMIS"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Southern Miss Golden Eagles",
    },
    {
        "canonical": "St. Bonaventure Bonnies",
        "mascot": "Bonnies",
        "city": "Allegany",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#4E3227",

        # Polymarket
        "polymarket_id": 1706,
        "polymarket_abbreviation": "stbon",
        "polymarket_name": "St. Bonaventure Bonnies",
        "polymarket_safe_name": "St. Bonaventure Bonnies",
        "polymarket_names": ["St. Bonaventure Bonnies", "STBON"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "St. Bonaventure Bonnies",
    },
    {
        "canonical": "St. Thomas (MN) Tommies",
        "mascot": "Tommies",
        "city": "St. Paul",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#512773",

        # Polymarket
        "polymarket_id": 2021,
        "polymarket_abbreviation": "stmn",
        "polymarket_name": "St. Thomas (MN) Tommies",
        "polymarket_safe_name": "St. Thomas-Minnesota Tommies",
        "polymarket_names": ["St. Thomas (MN) Tommies", "St. Thomas-Minnesota Tommies", "STMN"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "St. Thomas (MN) Tommies",
    },
    {
        "canonical": "Stanford Cardinal",
        "mascot": "Cardinal",
        "city": "Stanford",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#8C1515",

        # Polymarket
        "polymarket_id": 1911,
        "polymarket_abbreviation": "stan",
        "polymarket_name": "Stanford Cardinal",
        "polymarket_safe_name": "Stanford Cardinal",
        "polymarket_names": ["Stanford Cardinal", "STAN"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Stanford Cardinal",
    },
    {
        "canonical": "Stetson Hatters",
        "mascot": "Hatters",
        "city": "DeLand",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#3D8E33",

        # Polymarket
        "polymarket_id": 1700,
        "polymarket_abbreviation": "stetsn",
        "polymarket_name": "Stetson Hatters",
        "polymarket_safe_name": "Stetson Hatters",
        "polymarket_names": ["Stetson Hatters", "STETSN"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Stetson Hatters",
    },
    {
        "canonical": "Temple Owls",
        "mascot": "Owls",
        "city": "Philadelphia",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#A41E35",

        # Polymarket
        "polymarket_id": 1662,
        "polymarket_abbreviation": "templ",
        "polymarket_name": "Temple Owls",
        "polymarket_safe_name": "Temple Owls",
        "polymarket_names": ["Temple Owls", "TEMPL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Temple Owls",
    },
    {
        "canonical": "Tennessee Tech Golden Eagles",
        "mascot": "Golden Eagles",
        "city": "Cookeville",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#582C83",

        # Polymarket
        "polymarket_id": 1891,
        "polymarket_abbreviation": "tentch",
        "polymarket_name": "Tennessee Tech Golden Eagles",
        "polymarket_safe_name": "Tennessee Tech Golden Eagles",
        "polymarket_names": ["Tennessee Tech Golden Eagles", "TENTCH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Tennessee Tech Golden Eagles",
    },
    {
        "canonical": "Texas A&M Aggies",
        "mascot": "Aggies",
        "city": "College Station",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#500000",

        # Polymarket
        "polymarket_id": 1927,
        "polymarket_abbreviation": "txam",
        "polymarket_name": "Texas A&M Aggies",
        "polymarket_safe_name": "Texas A&M Aggies",
        "polymarket_names": ["Texas A&M Aggies", "TXAM"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Texas A&M Aggies",
    },
    {
        "canonical": "Texas Longhorns",
        "mascot": "Longhorns",
        "city": "Austin",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#BF5700",

        # Polymarket
        "polymarket_id": 1768,
        "polymarket_abbreviation": "tx",
        "polymarket_name": "Texas Longhorns",
        "polymarket_safe_name": "Texas Longhorns",
        "polymarket_names": ["Texas Longhorns", "TX"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Texas Longhorns",
    },
    {
        "canonical": "Texas Southern Tigers",
        "mascot": "Tigers",
        "city": "Houston",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#7C183E",

        # Polymarket
        "polymarket_id": 1961,
        "polymarket_abbreviation": "txs",
        "polymarket_name": "Texas Southern Tigers",
        "polymarket_safe_name": "Texas Southern Tigers",
        "polymarket_names": ["Texas Southern Tigers", "TXS"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Texas Southern Tigers",
    },
    {
        "canonical": "Texas State Bobcats",
        "mascot": "Bobcats",
        "city": "San Marcos",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#8B2635",

        # Polymarket
        "polymarket_id": 1989,
        "polymarket_abbreviation": "txst",
        "polymarket_name": "Texas State Bobcats",
        "polymarket_safe_name": "Texas State Bobcats",
        "polymarket_names": ["Texas State Bobcats", "TXST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Texas State Bobcats",
    },
    {
        "canonical": "Toledo Rockets",
        "mascot": "Rockets",
        "city": "Toledo",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003E7E",

        # Polymarket
        "polymarket_id": 1842,
        "polymarket_abbreviation": "toledo",
        "polymarket_name": "Toledo Rockets",
        "polymarket_safe_name": "Toledo Rockets",
        "polymarket_names": ["Toledo Rockets", "TOLEDO"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Toledo Rockets",
    },
    {
        "canonical": "Towson Tigers",
        "mascot": "Tigers",
        "city": "Towson",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#FFBB00",

        # Polymarket
        "polymarket_id": 1786,
        "polymarket_abbreviation": "tows",
        "polymarket_name": "Towson Tigers",
        "polymarket_safe_name": "Towson Tigers",
        "polymarket_names": ["Towson Tigers", "TOWS"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Towson Tigers",
    },
    {
        "canonical": "Tulsa Golden Hurricane",
        "mascot": "Golden Hurricane",
        "city": "Tulsa",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#0A3EAC",

        # Polymarket
        "polymarket_id": 1665,
        "polymarket_abbreviation": "tulsa",
        "polymarket_name": "Tulsa Golden Hurricane",
        "polymarket_safe_name": "Tulsa Golden Hurricane",
        "polymarket_names": ["Tulsa Golden Hurricane", "TULSA"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Tulsa Golden Hurricane",
    },
    {
        "canonical": "UC Riverside Highlanders",
        "mascot": "Highlanders",
        "city": "Riverside",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003DA5",

        # Polymarket
        "polymarket_id": 1779,
        "polymarket_abbreviation": "ucrvs",
        "polymarket_name": "UC Riverside Highlanders",
        "polymarket_safe_name": "UC Riverside Highlanders",
        "polymarket_names": ["UC Riverside Highlanders", "UCRVS"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UC Riverside Highlanders",
    },
    {
        "canonical": "UNLV Rebels",
        "mascot": "Rebels",
        "city": "Las Vegas",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C41E3A",

        # Polymarket
        "polymarket_id": 1876,
        "polymarket_abbreviation": "unlv",
        "polymarket_name": "UNLV Runnin' Rebels",
        "polymarket_safe_name": "UNLV Rebels",
        "polymarket_names": ["UNLV Runnin' Rebels", "UNLV Rebels", "UNLV"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UNLV Rebels",
    },
    {
        "canonical": "UT Martin Skyhawks",
        "mascot": "Skyhawks",
        "city": "Martin",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#003366",

        # Polymarket
        "polymarket_id": 1898,
        "polymarket_abbreviation": "tmrt",
        "polymarket_name": "UT Martin Skyhawks",
        "polymarket_safe_name": "UT Martin Skyhawks",
        "polymarket_names": ["UT Martin Skyhawks", "Tenn-Martin Skyhawks", "TMRT"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Tenn-Martin Skyhawks",
    },
    {
        "canonical": "UTEP Miners",
        "mascot": "Miners",
        "city": "El Paso",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#FF6A13",

        # Polymarket
        "polymarket_id": 1798,
        "polymarket_abbreviation": "utep",
        "polymarket_name": "UTEP Miners",
        "polymarket_safe_name": "UTEP Miners",
        "polymarket_names": ["UTEP Miners", "UTEP"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "UTEP Miners",
    },
    {
        "canonical": "Utah Valley Wolverines",
        "mascot": "Wolverines",
        "city": "Orem",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#275D38",

        # Polymarket
        "polymarket_id": 2005,
        "polymarket_abbreviation": "utahv",
        "polymarket_name": "Utah Valley Wolverines",
        "polymarket_safe_name": "Utah Valley Wolverines",
        "polymarket_names": ["Utah Valley Wolverines", "UTAHV"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Utah Valley Wolverines",
    },
    {
        "canonical": "Valparaiso Beacons",
        "mascot": "Beacons",
        "city": "Valparaiso",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#5C3000",

        # Polymarket
        "polymarket_id": 1807,
        "polymarket_abbreviation": "valp",
        "polymarket_name": "Valparaiso Beacons",
        "polymarket_safe_name": "Valparaiso Beacons",
        "polymarket_names": ["Valparaiso Beacons", "VALP"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Valparaiso Beacons",
    },
    {
        "canonical": "Washington Huskies",
        "mascot": "Huskies",
        "city": "Seattle",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#4B2E83",

        # Polymarket
        "polymarket_id": 1906,
        "polymarket_abbreviation": "wash",
        "polymarket_name": "Washington Huskies",
        "polymarket_safe_name": "Washington Huskies",
        "polymarket_names": ["Washington Huskies", "WASH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Washington Huskies",
    },
    {
        "canonical": "Washington State Cougars",
        "mascot": "Cougars",
        "city": "Pullman",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#981E32",

        # Polymarket
        "polymarket_id": 1913,
        "polymarket_abbreviation": "washst",
        "polymarket_name": "Washington State Cougars",
        "polymarket_safe_name": "Washington State Cougars",
        "polymarket_names": ["Washington State Cougars", "Washington St Cougars", "WASHST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Washington St Cougars",
    },
    {
        "canonical": "Weber State Wildcats",
        "mascot": "Wildcats",
        "city": "Ogden",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#4F2D7F",

        # Polymarket
        "polymarket_id": 1728,
        "polymarket_abbreviation": "webst",
        "polymarket_name": "Weber State Wildcats",
        "polymarket_safe_name": "Weber State Wildcats",
        "polymarket_names": ["Weber State Wildcats", "WEBST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Weber State Wildcats",
    },
    {
        "canonical": "West Virginia Mountaineers",
        "mascot": "Mountaineers",
        "city": "Morgantown",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#002855",

        # Polymarket
        "polymarket_id": 1766,
        "polymarket_abbreviation": "wvir",
        "polymarket_name": "West Virginia Mountaineers",
        "polymarket_safe_name": "West Virginia Mountaineers",
        "polymarket_names": ["West Virginia Mountaineers", "WVIR"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "West Virginia Mountaineers",
    },
    {
        "canonical": "Western Carolina Catamounts",
        "mascot": "Catamounts",
        "city": "Cullowhee",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#592C88",

        # Polymarket
        "polymarket_id": 1944,
        "polymarket_abbreviation": "wcar",
        "polymarket_name": "Western Carolina Catamounts",
        "polymarket_safe_name": "Western Carolina Catamounts",
        "polymarket_names": ["Western Carolina Catamounts", "WCAR"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Western Carolina Catamounts",
    },
    {
        "canonical": "Western Illinois Leathernecks",
        "mascot": "Leathernecks",
        "city": "Macomb",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#663399",

        # Polymarket
        "polymarket_id": 1979,
        "polymarket_abbreviation": "will",
        "polymarket_name": "Western Illinois Leathernecks",
        "polymarket_safe_name": "Western Illinois Leathernecks",
        "polymarket_names": ["Western Illinois Leathernecks", "WILL"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Western Illinois Leathernecks",
    },
    {
        "canonical": "Western Michigan Broncos",
        "mascot": "Broncos",
        "city": "Kalamazoo",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#532E1F",

        # Polymarket
        "polymarket_id": 1847,
        "polymarket_abbreviation": "wmich",
        "polymarket_name": "Western Michigan Broncos",
        "polymarket_safe_name": "Western Michigan Broncos",
        "polymarket_names": ["Western Michigan Broncos", "WMICH"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Western Michigan Broncos",
    },
    {
        "canonical": "Wichita State Shockers",
        "mascot": "Shockers",
        "city": "Wichita",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#504B3F",

        # Polymarket
        "polymarket_id": 1860,
        "polymarket_abbreviation": "wichst",
        "polymarket_name": "Wichita State Shockers",
        "polymarket_safe_name": "Wichita State Shockers",
        "polymarket_names": ["Wichita State Shockers", "Wichita St Shockers", "WICHST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Wichita St Shockers",
    },
    {
        "canonical": "William & Mary Tribe",
        "mascot": "Tribe",
        "city": "Williamsburg",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#115740",

        # Polymarket
        "polymarket_id": 1784,
        "polymarket_abbreviation": "wm",
        "polymarket_name": "William & Mary Tribe",
        "polymarket_safe_name": "William & Mary Tribe",
        "polymarket_names": ["William & Mary Tribe", "WM"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "William & Mary Tribe",
    },
    {
        "canonical": "Wofford Terriers",
        "mascot": "Terriers",
        "city": "Spartanburg",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#886E4C",

        # Polymarket
        "polymarket_id": 1942,
        "polymarket_abbreviation": "woff",
        "polymarket_name": "Wofford Terriers",
        "polymarket_safe_name": "Wofford Terriers",
        "polymarket_names": ["Wofford Terriers", "WOFF"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Wofford Terriers",
    },
    {
        "canonical": "Wright State Raiders",
        "mascot": "Raiders",
        "city": "Dayton",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#026937",

        # Polymarket
        "polymarket_id": 1809,
        "polymarket_abbreviation": "wrght",
        "polymarket_name": "Wright State Raiders",
        "polymarket_safe_name": "Wright State Raiders",
        "polymarket_names": ["Wright State Raiders", "Wright St Raiders", "WRGHT"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Wright St Raiders",
    },
    {
        "canonical": "Wyoming Cowboys",
        "mascot": "Cowboys",
        "city": "Laramie",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#492F24",

        # Polymarket
        "polymarket_id": 1877,
        "polymarket_abbreviation": "wyom",
        "polymarket_name": "Wyoming Cowboys",
        "polymarket_safe_name": "Wyoming Cowboys",
        "polymarket_names": ["Wyoming Cowboys", "WYOM"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Wyoming Cowboys",
    },
    {
        "canonical": "Xavier Musketeers",
        "mascot": "Musketeers",
        "city": "Cincinnati",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#184681",

        # Polymarket
        "polymarket_id": 1718,
        "polymarket_abbreviation": "xav",
        "polymarket_name": "Xavier Musketeers",
        "polymarket_safe_name": "Xavier Musketeers",
        "polymarket_names": ["Xavier Musketeers", "XAV"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Xavier Musketeers",
    },
    {
        "canonical": "Yale Bulldogs",
        "mascot": "Bulldogs",
        "city": "New Haven",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#00356B",

        # Polymarket
        "polymarket_id": 1817,
        "polymarket_abbreviation": "yale",
        "polymarket_name": "Yale Bulldogs",
        "polymarket_safe_name": "Yale Bulldogs",
        "polymarket_names": ["Yale Bulldogs", "YALE"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Yale Bulldogs",
    },
    {
        "canonical": "Youngstown State Penguins",
        "mascot": "Penguins",
        "city": "Youngstown",
        "league": "cbb",
        "sport": "basketball_ncaab",
        "color": "#C8102E",

        # Polymarket
        "polymarket_id": 1814,
        "polymarket_abbreviation": "yngst",
        "polymarket_name": "Youngstown State Penguins",
        "polymarket_safe_name": "Youngstown State Penguins",
        "polymarket_names": ["Youngstown State Penguins", "Youngstown St Penguins", "YNGST"],

        # Odds API
        "odds_api_key": "basketball_ncaab",
        "odds_api_name": "Youngstown St Penguins",
    },

    # =========================================================
    # CFB
    # =========================================================

    {
        "canonical": "Alcorn State Braves",
        "mascot": "Braves",
        "city": "Lorman",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#46166B",

        # Polymarket
        "polymarket_id": 1288,
        "polymarket_abbreviation": "alcst",
        "polymarket_name": "Braves",
        "polymarket_safe_name": "Alcorn State",
        "polymarket_names": ["Braves", "Alcorn State", "Alcorn State Braves", "ALCST"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "Alcorn State Braves",
    },

    {
        "canonical": "Arkansas-Monticello Boll Weevils",
        "mascot": "Boll Weevils",
        "city": "Monticello",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#006747",

        # Polymarket
        "polymarket_id": 1321,
        "polymarket_abbreviation": "armon",
        "polymarket_name": "Boll Weevils",
        "polymarket_safe_name": "Arkansas-Monticello",
        "polymarket_names": ["Boll Weevils", "Arkansas-Monticello", "Arkansas-Monticello Boll Weevils", "ARMON"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "Arkansas-Monticello Boll Weevils",
    },

    {
        "canonical": "Baylor Bears",
        "mascot": "Bears",
        "city": "Waco",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#154734",

        # Polymarket
        "polymarket_id": 1139,
        "polymarket_abbreviation": "bayl",
        "polymarket_name": "Bears",
        "polymarket_safe_name": "Baylor",
        "polymarket_names": ["Bears", "Baylor", "Baylor Bears", "BAYL"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "Baylor Bears",
    },

    {
        "canonical": "Bucknell Bison",
        "mascot": "Bison",
        "city": "Lewisburg",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#003865",

        # Polymarket
        "polymarket_id": 1244,
        "polymarket_abbreviation": "buck",
        "polymarket_name": "Bison",
        "polymarket_safe_name": "Bucknell",
        "polymarket_names": ["Bison", "Bucknell", "Bucknell Bison", "BUCK"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "Bucknell Bison",
    },

    {
        "canonical": "Central Arkansas Bears",
        "mascot": "Bears",
        "city": "Conway",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#582C83",

        # Polymarket
        "polymarket_id": 1279,
        "polymarket_abbreviation": "cark",
        "polymarket_name": "Bears",
        "polymarket_safe_name": "Central Arkansas",
        "polymarket_names": ["Bears", "Central Arkansas", "Central Arkansas Bears", "CARK"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "Central Arkansas Bears",
    },

    {
        "canonical": "Central Connecticut State Blue Devils",
        "mascot": "Blue Devils",
        "city": "New Britain",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#01529A",

        # Polymarket
        "polymarket_id": 1222,
        "polymarket_abbreviation": "cencon",
        "polymarket_name": "Blue Devils",
        "polymarket_safe_name": "Central Connecticut State",
        "polymarket_names": ["Blue Devils", "Central Connecticut State", "Central Connecticut State Blue Devils", "CENCON"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "Central Connecticut State Blue Devils",
    },

    {
        "canonical": "Charleston Southern Buccaneers",
        "mascot": "Buccaneers",
        "city": "North Charleston",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#0C2340",

        # Polymarket
        "polymarket_id": 1119,
        "polymarket_abbreviation": "chsou",
        "polymarket_name": "Buccaneers",
        "polymarket_safe_name": "Charleston Southern",
        "polymarket_names": ["Buccaneers", "Charleston Southern", "Charleston Southern Buccaneers", "CHSOU"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "Charleston Southern Buccaneers",
    },

    {
        "canonical": "East Tennessee State Buccaneers",
        "mascot": "Buccaneers",
        "city": "Johnson City",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#041E42",

        # Polymarket
        "polymarket_id": 1266,
        "polymarket_abbreviation": "etnst",
        "polymarket_name": "Buccaneers",
        "polymarket_safe_name": "East Tennessee State",
        "polymarket_names": ["Buccaneers", "East Tennessee State", "East Tennessee State Buccaneers", "ETNST"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "East Tennessee State Buccaneers",
    },

    {
        "canonical": "Howard Bison",
        "mascot": "Bison",
        "city": "Washington",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#003A63",

        # Polymarket
        "polymarket_id": 1193,
        "polymarket_abbreviation": "howrd",
        "polymarket_name": "Bison",
        "polymarket_safe_name": "Howard",
        "polymarket_names": ["Bison", "Howard", "Howard Bison", "HOWRD"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "Howard Bison",
    },

    {
        "canonical": "Idaho State Bengals",
        "mascot": "Bengals",
        "city": "Pocatello",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#FF671F",

        # Polymarket
        "polymarket_id": 1108,
        "polymarket_abbreviation": "idhst",
        "polymarket_name": "Bengals",
        "polymarket_safe_name": "Idaho State",
        "polymarket_names": ["Bengals", "Idaho State", "Idaho State Bengals", "IDHST"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "Idaho State Bengals",
    },

    {
        "canonical": "Livingstone Blue Bears",
        "mascot": "Blue Bears",
        "city": "Salisbury",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#8CB0BF",

        # Polymarket
        "polymarket_id": 1328,
        "polymarket_abbreviation": "lbb",
        "polymarket_name": "Blue Bears",
        "polymarket_safe_name": "Livingstone",
        "polymarket_names": ["Blue Bears", "Livingstone", "Livingstone Blue Bears", "LBB"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "Livingstone Blue Bears",
    },

    {
        "canonical": "Maine Black Bears",
        "mascot": "Black Bears",
        "city": "Orono",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#003263",

        # Polymarket
        "polymarket_id": 1081,
        "polymarket_abbreviation": "maine",
        "polymarket_name": "Black Bears",
        "polymarket_safe_name": "Maine",
        "polymarket_names": ["Black Bears", "Maine", "Maine Black Bears", "MAINE"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "Maine Black Bears",
    },

    {
        "canonical": "Mercer Bears",
        "mascot": "Bears",
        "city": "Macon",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#F76800",

        # Polymarket
        "polymarket_id": 1268,
        "polymarket_abbreviation": "merc",
        "polymarket_name": "Bears",
        "polymarket_safe_name": "Mercer",
        "polymarket_names": ["Bears", "Mercer", "Mercer Bears", "MERC"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "Mercer Bears",
    },

    {
        "canonical": "Montana State Bobcats",
        "mascot": "Bobcats",
        "city": "Bozeman",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#0D2C6C",

        # Polymarket
        "polymarket_id": 1110,
        "polymarket_abbreviation": "monst",
        "polymarket_name": "Bobcats",
        "polymarket_safe_name": "Montana State",
        "polymarket_names": ["Bobcats", "Montana State", "Montana State Bobcats", "MONST"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "Montana State Bobcats",
    },

    {
        "canonical": "North Dakota State Bison",
        "mascot": "Bison",
        "city": "Fargo",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#0A5640",

        # Polymarket
        "polymarket_id": 1296,
        "polymarket_abbreviation": "ndkst",
        "polymarket_name": "Bison",
        "polymarket_safe_name": "North Dakota State",
        "polymarket_names": ["Bison", "North Dakota State", "North Dakota State Bison", "NDKST"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "North Dakota State Bison",
    },

    {
        "canonical": "Northern Colorado Bears",
        "mascot": "Bears",
        "city": "Greeley",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#013C65",

        # Polymarket
        "polymarket_id": 1111,
        "polymarket_abbreviation": "ncol",
        "polymarket_name": "Bears",
        "polymarket_safe_name": "Northern Colorado",
        "polymarket_names": ["Bears", "Northern Colorado", "Northern Colorado Bears", "NCOL"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "Northern Colorado Bears",
    },

    {
        "canonical": "Ohio State Buckeyes",
        "mascot": "Buckeyes",
        "city": "Columbus",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#BB0000",

        # Polymarket
        "polymarket_id": 1129,
        "polymarket_abbreviation": "ohiost",
        "polymarket_name": "Buckeyes",
        "polymarket_safe_name": "Ohio State",
        "polymarket_names": ["Buckeyes", "Ohio State", "Ohio State Buckeyes", "OHIOST"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "Ohio State Buckeyes",
    },

    {
        "canonical": "Oklahoma Baptist Bison",
        "mascot": "Bison",
        "city": "Shawnee",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#255F2B",

        # Polymarket
        "polymarket_id": 1329,
        "polymarket_abbreviation": "obb",
        "polymarket_name": "Bison",
        "polymarket_safe_name": "Oklahoma Baptist",
        "polymarket_names": ["Bison", "Oklahoma Baptist", "Oklahoma Baptist Bison", "OBB"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "Oklahoma Baptist Bison",
    },

    {
        "canonical": "Presbyterian Blue Hose",
        "mascot": "Blue Hose",
        "city": "Clinton",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#002D72",

        # Polymarket
        "polymarket_id": 1120,
        "polymarket_abbreviation": "presb",
        "polymarket_name": "Blue Hose",
        "polymarket_safe_name": "Presbyterian",
        "polymarket_names": ["Blue Hose", "Presbyterian", "Presbyterian Blue Hose", "PRESB"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "Presbyterian Blue Hose",
    },

    {
        "canonical": "Purdue Boilermakers",
        "mascot": "Boilermakers",
        "city": "West Lafayette",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#CEB888",

        # Polymarket
        "polymarket_id": 1125,
        "polymarket_abbreviation": "pur",
        "polymarket_name": "Boilermakers",
        "polymarket_safe_name": "Purdue",
        "polymarket_names": ["Boilermakers", "Purdue", "Purdue Boilermakers", "PUR"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "Purdue Boilermakers",
    },

    {
        "canonical": "San Diego State Aztecs",
        "mascot": "Aztecs",
        "city": "San Diego",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#C41230",

        # Polymarket
        "polymarket_id": 1205,
        "polymarket_abbreviation": "sdst",
        "polymarket_name": "Aztecs",
        "polymarket_safe_name": "San Diego State",
        "polymarket_names": ["Aztecs", "San Diego State", "San Diego State Aztecs", "SDST"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "San Diego State Aztecs",
    },

    {
        "canonical": "South Carolina State Bulldogs",
        "mascot": "Bulldogs",
        "city": "Orangeburg",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#862633",

        # Polymarket
        "polymarket_id": 1189,
        "polymarket_abbreviation": "scarst",
        "polymarket_name": "Bulldogs",
        "polymarket_safe_name": "South Carolina State",
        "polymarket_names": ["Bulldogs", "South Carolina State", "South Carolina State Bulldogs", "SCARST"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "South Carolina State Bulldogs",
    },

    {
        "canonical": "The Citadel Bulldogs",
        "mascot": "Bulldogs",
        "city": "Charleston",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#3975B7",

        # Polymarket
        "polymarket_id": 1271,
        "polymarket_abbreviation": "cita",
        "polymarket_name": "Bulldogs",
        "polymarket_safe_name": "The Citadel",
        "polymarket_names": ["Bulldogs", "The Citadel", "The Citadel Bulldogs", "CITA"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "The Citadel Bulldogs",
    },

    {
        "canonical": "UC Davis Aggies",
        "mascot": "Aggies",
        "city": "Davis",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#022851",

        # Polymarket
        "polymarket_id": 1147,
        "polymarket_abbreviation": "ucdv",
        "polymarket_name": "Aggies",
        "polymarket_safe_name": "UC Davis",
        "polymarket_names": ["Aggies", "UC Davis", "UC Davis Aggies", "UCDV"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "UC Davis Aggies",
    },

    {
        "canonical": "Valparaiso Beacons",
        "mascot": "Beacons",
        "city": "Valparaiso",
        "league": "cfb",
        "sport": "americanfootball_ncaaf",
        "color": "#5C3000",

        # Polymarket
        "polymarket_id": 1171,
        "polymarket_abbreviation": "valp",
        "polymarket_name": "Beacons",
        "polymarket_safe_name": "Valparaiso",
        "polymarket_names": ["Beacons", "Valparaiso", "Valparaiso Beacons", "VALP"],

        # Odds API
        "odds_api_key": "americanfootball_ncaaf",
        "odds_api_name": "Valparaiso Beacons",
    },
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
