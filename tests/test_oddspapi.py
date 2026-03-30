from core.oddspapi_client import (
    normalize_team,
    name_similarity,
    decimal_to_fair_prob,
)


def test_normalize_team_fc():
    assert normalize_team("Manchester City FC") == "manchester city"


def test_normalize_team_the():
    assert normalize_team("The Lakers") == "lakers"


def test_normalize_team_plain():
    assert normalize_team("Kansas City Chiefs") == "kansas city chiefs"


def test_normalize_team_empty():
    assert normalize_team("") == ""


def test_name_similarity_exact():
    assert name_similarity("Boston Celtics", "Boston Celtics") == 1.0


def test_name_similarity_close():
    # "lakers" is the shared token, jaccard = 1/4
    score = name_similarity("LA Lakers", "Los Angeles Lakers")
    assert score > 0.0
    # Full names match well
    score2 = name_similarity("Los Angeles Lakers", "Los Angeles Lakers")
    assert score2 == 1.0


def test_name_similarity_different():
    score = name_similarity("Boston Celtics", "Miami Heat")
    assert score == 0.0


def test_decimal_to_fair_prob_basic():
    home, away, draw = decimal_to_fair_prob(1.87, 2.05)
    assert draw is None
    assert abs(home - 0.523) < 0.01
    assert abs(away - 0.477) < 0.01
    assert abs(home + away - 1.0) < 0.001


def test_decimal_to_fair_prob_even():
    home, away, draw = decimal_to_fair_prob(2.0, 2.0)
    assert home == away == 0.5
    assert draw is None


def test_decimal_to_fair_prob_soccer():
    home, away, draw = decimal_to_fair_prob(2.5, 3.5, 3.2)
    assert draw is not None
    assert abs(home + away + draw - 1.0) < 0.001
    assert draw > 0


def test_decimal_to_fair_prob_heavy_fav():
    home, away, draw = decimal_to_fair_prob(1.333, 3.5)
    assert home > 0.70
    assert away < 0.30


def test_decimal_to_fair_prob_invalid():
    home, away, draw = decimal_to_fair_prob(0.5, 2.0)
    assert home == 0.5
    assert away == 0.5
