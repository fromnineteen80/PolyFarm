from core.odds_api_client import (
    normalize_team,
    american_to_implied,
    calculate_fair_probs,
    consensus_from_bookmakers,
    OddsAPIClient,
)


def test_american_implied_favorite():
    p = american_to_implied(-305)
    assert abs(p - 0.7531) < 0.001


def test_american_implied_underdog():
    p = american_to_implied(240)
    assert abs(p - 0.2941) < 0.001


def test_american_implied_even():
    p = american_to_implied(-110)
    assert abs(p - 0.5238) < 0.001


def test_vig_removal_sums_to_one():
    outcomes = [
        {"name": "Tampa Bay Buccaneers", "price": -305},
        {"name": "Dallas Cowboys", "price": 240},
    ]
    h, a, d = calculate_fair_probs(outcomes, "Tampa Bay Buccaneers", "Dallas Cowboys")
    assert d is None
    assert abs(h + a - 1.0) < 0.001
    assert h > a


def test_vig_removal_soccer():
    outcomes = [
        {"name": "Manchester City", "price": -150},
        {"name": "Arsenal", "price": 400},
        {"name": "Draw", "price": 300},
    ]
    h, a, d = calculate_fair_probs(outcomes, "Manchester City", "Arsenal")
    assert d is not None
    assert abs(h + a + d - 1.0) < 0.001


def test_consensus_two_books():
    bookmakers = [
        {"key": "draftkings", "markets": [{"key": "h2h", "outcomes": [
            {"name": "Team A", "price": -200}, {"name": "Team B", "price": 160}]}]},
        {"key": "fanduel", "markets": [{"key": "h2h", "outcomes": [
            {"name": "Team A", "price": -210}, {"name": "Team B", "price": 170}]}]},
    ]
    h, a, d, books, _ = consensus_from_bookmakers(bookmakers, "Team A", "Team B")
    assert h is not None
    assert abs(h + a - 1.0) < 0.001
    assert "draftkings" in books
    assert "fanduel" in books


def test_consensus_insufficient_books():
    bookmakers = [
        {"key": "draftkings", "markets": [{"key": "h2h", "outcomes": [
            {"name": "Team A", "price": -200}, {"name": "Team B", "price": 160}]}]},
    ]
    h, a, d, books, _ = consensus_from_bookmakers(bookmakers, "Team A", "Team B")
    assert h is None


def test_normalize_team():
    assert normalize_team("Los Angeles Lakers") == "los angeles lakers"
    assert normalize_team("Manchester City FC") == "manchester city"
    assert normalize_team("The Lakers") == "lakers"
    assert normalize_team("") == ""


def test_team_registry_canonical_lookup():
    client = OddsAPIClient.__new__(OddsAPIClient)
    client._poly_teams = {
        123: {"name": "Los Angeles Lakers", "league": "nba"},
        456: {"name": "Boston Celtics", "league": "nba"},
    }
    client._poly_name_to_id = {
        "los angeles lakers": 123,
        "boston celtics": 456,
    }
    # Exact lookup
    assert client.get_canonical_name("Los Angeles Lakers") == "Los Angeles Lakers"
    assert client.get_canonical_name("Boston Celtics") == "Boston Celtics"
    # Normalized lookup
    assert client.get_canonical_name("los angeles lakers") == "Los Angeles Lakers"
    # Unknown team returns input
    assert client.get_canonical_name("Unknown Team") == "Unknown Team"


def test_team_registry_by_id():
    client = OddsAPIClient.__new__(OddsAPIClient)
    client._poly_teams = {
        123: {"name": "Los Angeles Lakers", "league": "nba"},
    }
    team = client.get_team_by_id(123)
    assert team["name"] == "Los Angeles Lakers"
    assert client.get_team_by_id(999) is None
