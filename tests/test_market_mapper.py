import pytest
from unittest.mock import MagicMock, AsyncMock
from core.market_mapper import MarketMapper

def make_mapper():
    registry = MagicMock()
    loader = MagicMock()
    loader.odds_data = {}
    loader.odds_last_updated = {}
    return MarketMapper(registry, loader)

def test_american_to_prob_negative():
    m = make_mapper()
    # -150 odds = 150/250 = 0.60
    assert abs(m._american_to_prob(-150) - 0.60) < 0.01

def test_american_to_prob_positive():
    m = make_mapper()
    # +200 odds = 100/300 = 0.333
    assert abs(m._american_to_prob(200) - 0.333) < 0.01

def test_remove_vig():
    m = make_mapper()
    yes, no = m._remove_vig(0.55, 0.50)
    assert abs(yes + no - 1.0) < 0.001

def test_fuzzy_match_high():
    m = make_mapper()
    score, _ = m._fuzzy_match_teams(
        "Los Angeles Dodgers", "San Francisco Giants",
        "Los Angeles Dodgers", "San Francisco Giants"
    )
    assert score >= 95

def test_fuzzy_match_medium():
    m = make_mapper()
    score, _ = m._fuzzy_match_teams(
        "LA Dodgers", "SF Giants",
        "Los Angeles Dodgers", "San Francisco Giants"
    )
    assert 50 <= score <= 94

def test_fuzzy_match_low():
    m = make_mapper()
    score, _ = m._fuzzy_match_teams(
        "Chicago Bulls", "Miami Heat",
        "Boston Celtics", "Golden State Warriors"
    )
    assert score < 50

def test_confirmed_threshold():
    m = make_mapper()
    score, _ = m._fuzzy_match_teams(
        "Los Angeles Dodgers", "New York Yankees",
        "Los Angeles Dodgers", "New York Yankees"
    )
    assert score >= 95  # CONFIRMED

def test_time_within_window():
    m = make_mapper()
    assert m._times_within_window(
        "2026-04-01T19:00:00Z",
        "2026-04-01T19:10:00Z",
        hours=2
    )

def test_time_outside_window():
    m = make_mapper()
    assert not m._times_within_window(
        "2026-04-01T13:00:00Z",
        "2026-04-01T19:10:00Z",
        hours=2
    )
