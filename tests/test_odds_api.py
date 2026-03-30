from core.odds_api_client import (
    normalize_team,
    name_similarity,
    american_to_implied,
    calculate_fair_probs,
    consensus_from_bookmakers,
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


def test_name_similarity_exact():
    assert name_similarity("Boston Celtics", "Boston Celtics") == 1.0


def test_name_similarity_zero():
    assert name_similarity("Boston Celtics", "Miami Heat") == 0.0
