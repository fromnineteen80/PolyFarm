"""
OracleFarming Master Team Registry.

Every team we could encounter across Polymarket and
The Odds API, with every name variation, color, and
both API identifiers.

The pipeline uses this as the single source of truth.
No fuzzy matching. No guessing. If a team isn't in
this registry, it doesn't get matched.

Structure per team:
  canonical: Our display name
  mascot: Team mascot/nickname only
  city: City/state/school only
  abbreviation: Short code (Polymarket abbr field)
  color: Team primary color (Polymarket colorPrimary)
  polymarket_id: Polymarket team ID
  polymarket_names: All name forms Polymarket might use
  odds_api_name: Exact name The Odds API uses
  league: Our league slug (nba, mlb, etc)
  sport: Our sport key (basketball_nba, etc)
  odds_api_key: Odds API sport key
"""

TEAM_REGISTRY = [
    # ═══════════════════════════════════════════
    # NBA
    # ═══════════════════════════════════════════
    {"canonical": "Atlanta Hawks", "mascot": "Hawks", "city": "Atlanta", "abbreviation": "atl", "color": "#C8102E", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Hawks", "Atlanta Hawks", "Atlanta"], "odds_api_name": "Atlanta Hawks"},
    {"canonical": "Boston Celtics", "mascot": "Celtics", "city": "Boston", "abbreviation": "bos", "color": "#007A33", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Celtics", "Boston Celtics", "Boston"], "odds_api_name": "Boston Celtics"},
    {"canonical": "Brooklyn Nets", "mascot": "Nets", "city": "Brooklyn", "abbreviation": "bkn", "color": "#000000", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Nets", "Brooklyn Nets", "Brooklyn"], "odds_api_name": "Brooklyn Nets"},
    {"canonical": "Charlotte Hornets", "mascot": "Hornets", "city": "Charlotte", "abbreviation": "cha", "color": "#1D1160", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Hornets", "Charlotte Hornets", "Charlotte"], "odds_api_name": "Charlotte Hornets"},
    {"canonical": "Chicago Bulls", "mascot": "Bulls", "city": "Chicago", "abbreviation": "chi", "color": "#CE1141", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Bulls", "Chicago Bulls", "Chicago"], "odds_api_name": "Chicago Bulls"},
    {"canonical": "Cleveland Cavaliers", "mascot": "Cavaliers", "city": "Cleveland", "abbreviation": "cle", "color": "#860038", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Cavaliers", "Cleveland Cavaliers", "Cleveland"], "odds_api_name": "Cleveland Cavaliers"},
    {"canonical": "Dallas Mavericks", "mascot": "Mavericks", "city": "Dallas", "abbreviation": "dal", "color": "#00538C", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Mavericks", "Dallas Mavericks", "Dallas"], "odds_api_name": "Dallas Mavericks"},
    {"canonical": "Denver Nuggets", "mascot": "Nuggets", "city": "Denver", "abbreviation": "den", "color": "#0E2240", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Nuggets", "Denver Nuggets", "Denver"], "odds_api_name": "Denver Nuggets"},
    {"canonical": "Detroit Pistons", "mascot": "Pistons", "city": "Detroit", "abbreviation": "det", "color": "#C8102E", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Pistons", "Detroit Pistons", "Detroit"], "odds_api_name": "Detroit Pistons"},
    {"canonical": "Golden State Warriors", "mascot": "Warriors", "city": "Golden State", "abbreviation": "gs", "color": "#1D428A", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Warriors", "Golden State Warriors", "Golden State"], "odds_api_name": "Golden State Warriors"},
    {"canonical": "Houston Rockets", "mascot": "Rockets", "city": "Houston", "abbreviation": "hou", "color": "#CE1141", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Rockets", "Houston Rockets", "Houston"], "odds_api_name": "Houston Rockets"},
    {"canonical": "Indiana Pacers", "mascot": "Pacers", "city": "Indiana", "abbreviation": "ind", "color": "#002D62", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Pacers", "Indiana Pacers", "Indiana"], "odds_api_name": "Indiana Pacers"},
    {"canonical": "Los Angeles Clippers", "mascot": "Clippers", "city": "Los Angeles", "abbreviation": "lac", "color": "#C8102E", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Clippers", "Los Angeles C Clippers", "Los Angeles Clippers"], "odds_api_name": "Los Angeles Clippers"},
    {"canonical": "Los Angeles Lakers", "mascot": "Lakers", "city": "Los Angeles", "abbreviation": "lal", "color": "#552583", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Lakers", "Los Angeles L Lakers", "Los Angeles Lakers"], "odds_api_name": "Los Angeles Lakers"},
    {"canonical": "Memphis Grizzlies", "mascot": "Grizzlies", "city": "Memphis", "abbreviation": "mem", "color": "#5D76A9", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Grizzlies", "Memphis Grizzlies", "Memphis"], "odds_api_name": "Memphis Grizzlies"},
    {"canonical": "Miami Heat", "mascot": "Heat", "city": "Miami", "abbreviation": "mia", "color": "#98002E", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Heat", "Miami Heat", "Miami"], "odds_api_name": "Miami Heat"},
    {"canonical": "Milwaukee Bucks", "mascot": "Bucks", "city": "Milwaukee", "abbreviation": "mil", "color": "#00471B", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Bucks", "Milwaukee Bucks", "Milwaukee"], "odds_api_name": "Milwaukee Bucks"},
    {"canonical": "Minnesota Timberwolves", "mascot": "Timberwolves", "city": "Minnesota", "abbreviation": "min", "color": "#0C2340", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Timberwolves", "Minnesota Timberwolves", "Minnesota"], "odds_api_name": "Minnesota Timberwolves"},
    {"canonical": "New Orleans Pelicans", "mascot": "Pelicans", "city": "New Orleans", "abbreviation": "no", "color": "#0C2340", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Pelicans", "New Orleans Pelicans", "New Orleans"], "odds_api_name": "New Orleans Pelicans"},
    {"canonical": "New York Knicks", "mascot": "Knicks", "city": "New York", "abbreviation": "ny", "color": "#006BB6", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Knicks", "New York Knicks", "New York"], "odds_api_name": "New York Knicks"},
    {"canonical": "Oklahoma City Thunder", "mascot": "Thunder", "city": "Oklahoma City", "abbreviation": "okc", "color": "#007AC1", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Thunder", "Oklahoma City Thunder", "Oklahoma City"], "odds_api_name": "Oklahoma City Thunder"},
    {"canonical": "Orlando Magic", "mascot": "Magic", "city": "Orlando", "abbreviation": "orl", "color": "#0077C0", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Magic", "Orlando Magic", "Orlando"], "odds_api_name": "Orlando Magic"},
    {"canonical": "Philadelphia 76ers", "mascot": "76ers", "city": "Philadelphia", "abbreviation": "phi", "color": "#006BB6", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["76ers", "Philadelphia 76ers", "Philadelphia"], "odds_api_name": "Philadelphia 76ers"},
    {"canonical": "Phoenix Suns", "mascot": "Suns", "city": "Phoenix", "abbreviation": "pho", "color": "#1D1160", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Suns", "Phoenix Suns", "Phoenix"], "odds_api_name": "Phoenix Suns"},
    {"canonical": "Portland Trail Blazers", "mascot": "Trail Blazers", "city": "Portland", "abbreviation": "por", "color": "#E03A3E", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Trail Blazers", "Portland Trail Blazers", "Portland"], "odds_api_name": "Portland Trail Blazers"},
    {"canonical": "Sacramento Kings", "mascot": "Kings", "city": "Sacramento", "abbreviation": "sac", "color": "#5A2D81", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Kings", "Sacramento Kings", "Sacramento"], "odds_api_name": "Sacramento Kings"},
    {"canonical": "San Antonio Spurs", "mascot": "Spurs", "city": "San Antonio", "abbreviation": "sa", "color": "#C4CED4", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Spurs", "San Antonio Spurs", "San Antonio"], "odds_api_name": "San Antonio Spurs"},
    {"canonical": "Toronto Raptors", "mascot": "Raptors", "city": "Toronto", "abbreviation": "tor", "color": "#CE1141", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Raptors", "Toronto Raptors", "Toronto"], "odds_api_name": "Toronto Raptors"},
    {"canonical": "Utah Jazz", "mascot": "Jazz", "city": "Utah", "abbreviation": "uta", "color": "#002B5C", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Jazz", "Utah Jazz", "Utah"], "odds_api_name": "Utah Jazz"},
    {"canonical": "Washington Wizards", "mascot": "Wizards", "city": "Washington", "abbreviation": "was", "color": "#002B5C", "league": "nba", "sport": "basketball_nba", "odds_api_key": "basketball_nba", "polymarket_names": ["Wizards", "Washington Wizards", "Washington"], "odds_api_name": "Washington Wizards"},

    # ═══════════════════════════════════════════
    # NHL
    # ═══════════════════════════════════════════
    {"canonical": "Anaheim Ducks", "mascot": "Ducks", "city": "Anaheim", "abbreviation": "ana", "color": "#F47A38", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Ducks", "ANA Ducks"], "odds_api_name": "Anaheim Ducks"},
    {"canonical": "Boston Bruins", "mascot": "Bruins", "city": "Boston", "abbreviation": "bos", "color": "#FFB81C", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Bruins", "BOS Bruins"], "odds_api_name": "Boston Bruins"},
    {"canonical": "Buffalo Sabres", "mascot": "Sabres", "city": "Buffalo", "abbreviation": "buf", "color": "#002654", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Sabres", "BUF Sabres"], "odds_api_name": "Buffalo Sabres"},
    {"canonical": "Calgary Flames", "mascot": "Flames", "city": "Calgary", "abbreviation": "cgy", "color": "#D2001C", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Flames", "CGY Flames"], "odds_api_name": "Calgary Flames"},
    {"canonical": "Carolina Hurricanes", "mascot": "Hurricanes", "city": "Carolina", "abbreviation": "car", "color": "#CC0000", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Hurricanes", "CAR Hurricanes"], "odds_api_name": "Carolina Hurricanes"},
    {"canonical": "Chicago Blackhawks", "mascot": "Blackhawks", "city": "Chicago", "abbreviation": "chi", "color": "#CF0A2C", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Blackhawks", "CHI Blackhawks"], "odds_api_name": "Chicago Blackhawks"},
    {"canonical": "Colorado Avalanche", "mascot": "Avalanche", "city": "Colorado", "abbreviation": "col", "color": "#6F263D", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Avalanche", "COL Avalanche"], "odds_api_name": "Colorado Avalanche"},
    {"canonical": "Columbus Blue Jackets", "mascot": "Blue Jackets", "city": "Columbus", "abbreviation": "cbj", "color": "#002654", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Blue Jackets", "CBJ Blue Jackets"], "odds_api_name": "Columbus Blue Jackets"},
    {"canonical": "Dallas Stars", "mascot": "Stars", "city": "Dallas", "abbreviation": "dal", "color": "#006847", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Stars", "DAL Stars"], "odds_api_name": "Dallas Stars"},
    {"canonical": "Detroit Red Wings", "mascot": "Red Wings", "city": "Detroit", "abbreviation": "det", "color": "#CE1126", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Red Wings", "DET Red Wings"], "odds_api_name": "Detroit Red Wings"},
    {"canonical": "Edmonton Oilers", "mascot": "Oilers", "city": "Edmonton", "abbreviation": "edm", "color": "#041E42", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Oilers", "EDM Oilers"], "odds_api_name": "Edmonton Oilers"},
    {"canonical": "Florida Panthers", "mascot": "Panthers", "city": "Florida", "abbreviation": "fla", "color": "#041E42", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Panthers", "FLA Panthers"], "odds_api_name": "Florida Panthers"},
    {"canonical": "Los Angeles Kings", "mascot": "Kings", "city": "Los Angeles", "abbreviation": "la", "color": "#111111", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Kings", "LA Kings"], "odds_api_name": "Los Angeles Kings"},
    {"canonical": "Minnesota Wild", "mascot": "Wild", "city": "Minnesota", "abbreviation": "min", "color": "#154734", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Wild", "MIN Wild"], "odds_api_name": "Minnesota Wild"},
    {"canonical": "Montreal Canadiens", "mascot": "Canadiens", "city": "Montreal", "abbreviation": "mon", "color": "#AF1E2D", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Canadiens", "MON Canadiens"], "odds_api_name": "Montréal Canadiens"},
    {"canonical": "Nashville Predators", "mascot": "Predators", "city": "Nashville", "abbreviation": "nas", "color": "#FFB81C", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Predators", "NAS Predators"], "odds_api_name": "Nashville Predators"},
    {"canonical": "New Jersey Devils", "mascot": "Devils", "city": "New Jersey", "abbreviation": "nj", "color": "#CE1126", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Devils", "NJ Devils"], "odds_api_name": "New Jersey Devils"},
    {"canonical": "New York Islanders", "mascot": "Islanders", "city": "New York", "abbreviation": "nyi", "color": "#00539B", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Islanders", "NYI Islanders"], "odds_api_name": "New York Islanders"},
    {"canonical": "New York Rangers", "mascot": "Rangers", "city": "New York", "abbreviation": "nyr", "color": "#0038A8", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Rangers", "NYR Rangers"], "odds_api_name": "New York Rangers"},
    {"canonical": "Ottawa Senators", "mascot": "Senators", "city": "Ottawa", "abbreviation": "ott", "color": "#C52032", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Senators", "OTT Senators"], "odds_api_name": "Ottawa Senators"},
    {"canonical": "Philadelphia Flyers", "mascot": "Flyers", "city": "Philadelphia", "abbreviation": "phi", "color": "#F74902", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Flyers", "PHI Flyers"], "odds_api_name": "Philadelphia Flyers"},
    {"canonical": "Pittsburgh Penguins", "mascot": "Penguins", "city": "Pittsburgh", "abbreviation": "pit", "color": "#FCB514", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Penguins", "PIT Penguins"], "odds_api_name": "Pittsburgh Penguins"},
    {"canonical": "San Jose Sharks", "mascot": "Sharks", "city": "San Jose", "abbreviation": "sj", "color": "#006D75", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Sharks", "SJ Sharks"], "odds_api_name": "San Jose Sharks"},
    {"canonical": "Seattle Kraken", "mascot": "Kraken", "city": "Seattle", "abbreviation": "sea", "color": "#001628", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Kraken", "SEA Kraken"], "odds_api_name": "Seattle Kraken"},
    {"canonical": "St. Louis Blues", "mascot": "Blues", "city": "St. Louis", "abbreviation": "stl", "color": "#002F87", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Blues", "STL Blues"], "odds_api_name": "St Louis Blues"},
    {"canonical": "Tampa Bay Lightning", "mascot": "Lightning", "city": "Tampa Bay", "abbreviation": "tb", "color": "#002868", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Lightning", "TB Lightning"], "odds_api_name": "Tampa Bay Lightning"},
    {"canonical": "Toronto Maple Leafs", "mascot": "Maple Leafs", "city": "Toronto", "abbreviation": "tor", "color": "#00205B", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Maple Leafs", "TOR Maple Leafs"], "odds_api_name": "Toronto Maple Leafs"},
    {"canonical": "Utah Mammoth", "mascot": "Mammoth", "city": "Utah", "abbreviation": "uta", "color": "#000000", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Mammoth", "UTA Mammoth"], "odds_api_name": "Utah Hockey Club"},
    {"canonical": "Vancouver Canucks", "mascot": "Canucks", "city": "Vancouver", "abbreviation": "van", "color": "#001F5B", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Canucks", "VAN Canucks"], "odds_api_name": "Vancouver Canucks"},
    {"canonical": "Vegas Golden Knights", "mascot": "Golden Knights", "city": "Vegas", "abbreviation": "veg", "color": "#B4975A", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Golden Knights", "VEG Golden Knights"], "odds_api_name": "Vegas Golden Knights"},
    {"canonical": "Washington Capitals", "mascot": "Capitals", "city": "Washington", "abbreviation": "was", "color": "#C8102E", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Capitals", "WAS Capitals"], "odds_api_name": "Washington Capitals"},
    {"canonical": "Winnipeg Jets", "mascot": "Jets", "city": "Winnipeg", "abbreviation": "wpg", "color": "#041E42", "league": "nhl", "sport": "icehockey_nhl", "odds_api_key": "icehockey_nhl", "polymarket_names": ["Jets", "WPG Jets"], "odds_api_name": "Winnipeg Jets"},

    # ═══════════════════════════════════════════
    # MLB
    # ═══════════════════════════════════════════
    {"canonical": "Arizona Diamondbacks", "mascot": "Diamondbacks", "city": "Arizona", "abbreviation": "az", "color": "#A71930", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Arizona Diamondbacks"], "odds_api_name": "Arizona Diamondbacks"},
    {"canonical": "Oakland Athletics", "mascot": "Athletics", "city": "Oakland", "abbreviation": "ath", "color": "#003831", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Athletics"], "odds_api_name": "Oakland Athletics"},
    {"canonical": "Atlanta Braves", "mascot": "Braves", "city": "Atlanta", "abbreviation": "atl", "color": "#CE1141", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Atlanta Braves"], "odds_api_name": "Atlanta Braves"},
    {"canonical": "Baltimore Orioles", "mascot": "Orioles", "city": "Baltimore", "abbreviation": "bal", "color": "#DF4601", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Baltimore Orioles"], "odds_api_name": "Baltimore Orioles"},
    {"canonical": "Boston Red Sox", "mascot": "Red Sox", "city": "Boston", "abbreviation": "bos", "color": "#BD3039", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Boston Red Sox"], "odds_api_name": "Boston Red Sox"},
    {"canonical": "Chicago Cubs", "mascot": "Cubs", "city": "Chicago", "abbreviation": "chc", "color": "#0E3386", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Chicago Cubs"], "odds_api_name": "Chicago Cubs"},
    {"canonical": "Chicago White Sox", "mascot": "White Sox", "city": "Chicago", "abbreviation": "cws", "color": "#27251F", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Chicago White Sox"], "odds_api_name": "Chicago White Sox"},
    {"canonical": "Cincinnati Reds", "mascot": "Reds", "city": "Cincinnati", "abbreviation": "cin", "color": "#C6011F", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Cincinnati Reds"], "odds_api_name": "Cincinnati Reds"},
    {"canonical": "Cleveland Guardians", "mascot": "Guardians", "city": "Cleveland", "abbreviation": "cle", "color": "#00385D", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Cleveland Guardians"], "odds_api_name": "Cleveland Guardians"},
    {"canonical": "Colorado Rockies", "mascot": "Rockies", "city": "Colorado", "abbreviation": "col", "color": "#333366", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Colorado Rockies"], "odds_api_name": "Colorado Rockies"},
    {"canonical": "Detroit Tigers", "mascot": "Tigers", "city": "Detroit", "abbreviation": "det", "color": "#0C2340", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Detroit Tigers"], "odds_api_name": "Detroit Tigers"},
    {"canonical": "Houston Astros", "mascot": "Astros", "city": "Houston", "abbreviation": "hou", "color": "#002D62", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Houston Astros"], "odds_api_name": "Houston Astros"},
    {"canonical": "Kansas City Royals", "mascot": "Royals", "city": "Kansas City", "abbreviation": "kc", "color": "#004687", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Kansas City Royals"], "odds_api_name": "Kansas City Royals"},
    {"canonical": "Los Angeles Angels", "mascot": "Angels", "city": "Los Angeles", "abbreviation": "laa", "color": "#BA0021", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Los Angeles Angels"], "odds_api_name": "Los Angeles Angels"},
    {"canonical": "Los Angeles Dodgers", "mascot": "Dodgers", "city": "Los Angeles", "abbreviation": "lad", "color": "#005A9C", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Los Angeles Dodgers"], "odds_api_name": "Los Angeles Dodgers"},
    {"canonical": "Miami Marlins", "mascot": "Marlins", "city": "Miami", "abbreviation": "mia", "color": "#00A3E0", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Miami Marlins"], "odds_api_name": "Miami Marlins"},
    {"canonical": "Milwaukee Brewers", "mascot": "Brewers", "city": "Milwaukee", "abbreviation": "mil", "color": "#12284B", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Milwaukee Brewers"], "odds_api_name": "Milwaukee Brewers"},
    {"canonical": "Minnesota Twins", "mascot": "Twins", "city": "Minnesota", "abbreviation": "min", "color": "#002B5C", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Minnesota Twins"], "odds_api_name": "Minnesota Twins"},
    {"canonical": "New York Mets", "mascot": "Mets", "city": "New York", "abbreviation": "nym", "color": "#002D72", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["New York Mets"], "odds_api_name": "New York Mets"},
    {"canonical": "New York Yankees", "mascot": "Yankees", "city": "New York", "abbreviation": "nyy", "color": "#003087", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["New York Yankees"], "odds_api_name": "New York Yankees"},
    {"canonical": "Philadelphia Phillies", "mascot": "Phillies", "city": "Philadelphia", "abbreviation": "phi", "color": "#E81828", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Philadelphia Phillies"], "odds_api_name": "Philadelphia Phillies"},
    {"canonical": "Pittsburgh Pirates", "mascot": "Pirates", "city": "Pittsburgh", "abbreviation": "pit", "color": "#27251F", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Pittsburgh Pirates"], "odds_api_name": "Pittsburgh Pirates"},
    {"canonical": "San Diego Padres", "mascot": "Padres", "city": "San Diego", "abbreviation": "sd", "color": "#2F241D", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["San Diego Padres"], "odds_api_name": "San Diego Padres"},
    {"canonical": "San Francisco Giants", "mascot": "Giants", "city": "San Francisco", "abbreviation": "sf", "color": "#FD5A1E", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["San Francisco Giants"], "odds_api_name": "San Francisco Giants"},
    {"canonical": "Seattle Mariners", "mascot": "Mariners", "city": "Seattle", "abbreviation": "sea", "color": "#0C2C56", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Seattle Mariners"], "odds_api_name": "Seattle Mariners"},
    {"canonical": "St. Louis Cardinals", "mascot": "Cardinals", "city": "St. Louis", "abbreviation": "stl", "color": "#C41E3A", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["St. Louis Cardinals"], "odds_api_name": "St. Louis Cardinals"},
    {"canonical": "Tampa Bay Rays", "mascot": "Rays", "city": "Tampa Bay", "abbreviation": "tb", "color": "#092C5C", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Tampa Bay Rays"], "odds_api_name": "Tampa Bay Rays"},
    {"canonical": "Texas Rangers", "mascot": "Rangers", "city": "Texas", "abbreviation": "tex", "color": "#003278", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Texas Rangers"], "odds_api_name": "Texas Rangers"},
    {"canonical": "Toronto Blue Jays", "mascot": "Blue Jays", "city": "Toronto", "abbreviation": "tor", "color": "#134A8E", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Toronto Blue Jays"], "odds_api_name": "Toronto Blue Jays"},
    {"canonical": "Washington Nationals", "mascot": "Nationals", "city": "Washington", "abbreviation": "wsh", "color": "#AB0003", "league": "mlb", "sport": "baseball_mlb", "odds_api_key": "baseball_mlb", "polymarket_names": ["Washington Nationals"], "odds_api_name": "Washington Nationals"},
]

# Build lookup indexes
_BY_POLY_NAME = {}  # normalized polymarket name -> registry entry
_BY_ODDS_NAME = {}  # normalized odds api name -> registry entry
_BY_ABBR = {}       # abbreviation -> registry entry

def _build_indexes():
    from core.pipeline import normalize_team
    for team in TEAM_REGISTRY:
        for pname in team["polymarket_names"]:
            _BY_POLY_NAME[normalize_team(pname)] = team
        _BY_ODDS_NAME[normalize_team(team["odds_api_name"])] = team
        _BY_ABBR[team["abbreviation"]] = team

def lookup_by_polymarket_name(name):
    if not _BY_POLY_NAME:
        _build_indexes()
    from core.pipeline import normalize_team
    return _BY_POLY_NAME.get(normalize_team(name))

def lookup_by_odds_api_name(name):
    if not _BY_ODDS_NAME:
        _build_indexes()
    from core.pipeline import normalize_team
    return _BY_ODDS_NAME.get(normalize_team(name))

def lookup_by_abbreviation(abbr):
    if not _BY_ABBR:
        _build_indexes()
    return _BY_ABBR.get(abbr.lower() if abbr else "")
