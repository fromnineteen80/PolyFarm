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
