import pytest
from config import (
    FAVORITES_FLOOR,
    BAND_A_MIN_PRICE, BAND_A_MIN_EDGE,
    BAND_B_MIN_PRICE, BAND_B_MIN_EDGE,
    BAND_C_MIN_PRICE, BAND_C_MIN_EDGE,
    LIVE_GAME_EDGE_REDUCTION,
    TAKER_FEE_RATE, MAKER_REBATE_RATE,
    REPRICE_EXIT_PCT,
)

def test_favorites_floor():
    assert FAVORITES_FLOOR == 0.55

def test_band_a_threshold():
    assert BAND_A_MIN_PRICE == 0.70
    assert BAND_A_MIN_EDGE == 0.08

def test_band_b_threshold():
    assert BAND_B_MIN_PRICE == 0.60
    assert BAND_B_MIN_EDGE == 0.05

def test_band_c_threshold():
    assert BAND_C_MIN_PRICE == 0.55
    assert BAND_C_MIN_EDGE == 0.03

def test_live_game_edge_reduction():
    assert LIVE_GAME_EDGE_REDUCTION == 0.01
    # Band A live minimum
    assert BAND_A_MIN_EDGE - LIVE_GAME_EDGE_REDUCTION\
           == 0.07

def test_net_edge_calculation():
    # Given: entry at 0.65, edge 0.08, 100 shares
    poly_price = 0.65
    raw_edge = 0.08
    shares = 100
    entry_notional = shares * poly_price
    taker_fee = entry_notional * TAKER_FEE_RATE
    exit_target = poly_price + (raw_edge * REPRICE_EXIT_PCT)
    exit_notional = shares * (1 - exit_target)
    maker_rebate = exit_notional * MAKER_REBATE_RATE
    net = (raw_edge * shares) - taker_fee + maker_rebate
    assert net > 0
    assert taker_fee > 0
    assert maker_rebate > 0

def test_reprice_exit_target():
    entry = 0.65
    edge = 0.08
    target = entry + (edge * REPRICE_EXIT_PCT)
    assert abs(target - 0.702) < 0.001

def test_below_favorites_floor_rejected():
    assert 0.54 < FAVORITES_FLOOR
    assert 0.55 >= FAVORITES_FLOOR

def test_taker_fee_rate():
    assert TAKER_FEE_RATE == 0.003

def test_maker_rebate_rate():
    assert MAKER_REBATE_RATE == 0.002
