import pytest
from config import (
    BAND_A_MIN_PRICE, BAND_A_MIN_EDGE,
    BAND_B_MIN_PRICE, BAND_B_MAX_PRICE,
    BAND_B_MIN_EDGE,
    BAND_C_MIN_PRICE, BAND_C_MAX_PRICE,
    BAND_C_MIN_EDGE,
    FAVORITES_FLOOR,
    MAX_SINGLE_SPORT_PCT,
)

def classify_band(price: float,
                  edge: float) -> str | None:
    if price < FAVORITES_FLOOR:
        return None
    if price >= BAND_A_MIN_PRICE and \
       edge >= BAND_A_MIN_EDGE:
        return "A"
    if BAND_B_MIN_PRICE <= price < BAND_B_MAX_PRICE \
       and edge >= BAND_B_MIN_EDGE:
        return "B"
    if BAND_C_MIN_PRICE <= price < BAND_C_MAX_PRICE \
       and edge >= BAND_C_MIN_EDGE:
        return "C"
    return None

def test_band_a_qualifies():
    assert classify_band(0.72, 0.09) == "A"

def test_band_a_min_boundary():
    assert classify_band(0.70, 0.08) == "A"

def test_band_b_qualifies():
    assert classify_band(0.65, 0.06) == "B"

def test_band_c_qualifies():
    assert classify_band(0.57, 0.04) == "C"

def test_below_floor_rejected():
    assert classify_band(0.54, 0.10) is None

def test_floor_boundary():
    assert classify_band(0.55, 0.04) == "C"

def test_insufficient_edge_band_a():
    assert classify_band(0.72, 0.07) is None

def test_insufficient_edge_band_b():
    assert classify_band(0.65, 0.04) is None

def test_concentration_limit():
    assert MAX_SINGLE_SPORT_PCT == 0.40
