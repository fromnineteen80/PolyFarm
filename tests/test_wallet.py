import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from config import (
    FLOOR_PCT, HARVEST_THRESHOLD,
    PROTECTION_THRESHOLD, LOCK_THRESHOLD,
    DAILY_LOSS_REDUCE_TIER, DAILY_LOSS_PAUSE_TIER,
    DAILY_LOSS_HALT_TIER
)

def make_wallet(start_value=1000.0,
                paper_mode=True):
    from core.wallet import WalletManager, WalletState
    client = AsyncMock()
    client.account.balances = AsyncMock(
        return_value={"buying_power": str(start_value)}
    )
    client.portfolio.positions = AsyncMock(
        return_value=[]
    )
    wm = WalletManager(client, paper_mode)
    wm.state.session_start_value = start_value
    wm.state.floor_value = start_value * FLOOR_PCT
    wm.state.live_portfolio_value = start_value
    return wm

def test_floor_calculation():
    wm = make_wallet(1000.0)
    assert wm.state.floor_value == 800.0

def test_working_capital():
    wm = make_wallet(1000.0)
    working = (wm.state.live_portfolio_value
               - wm.state.floor_value)
    assert working == 200.0

def test_band_a_sizing_normal():
    wm = make_wallet(1000.0)
    size = wm.get_position_size_usd("band_a")
    from config import BAND_A_POSITION_PCT
    assert abs(size - 1000.0 * BAND_A_POSITION_PCT) < 0.01

def test_band_b_sizing_normal():
    wm = make_wallet(1000.0)
    size = wm.get_position_size_usd("band_b")
    from config import BAND_B_POSITION_PCT
    assert abs(size - 1000.0 * BAND_B_POSITION_PCT) < 0.01

def test_band_c_sizing_normal():
    wm = make_wallet(1000.0)
    size = wm.get_position_size_usd("band_c")
    from config import BAND_C_POSITION_PCT
    assert abs(size - 1000.0 * BAND_C_POSITION_PCT) < 0.01

def test_band_sizing_in_reduce_mode():
    wm = make_wallet(1000.0)
    wm.state.loss_mode = "REDUCE"
    size = wm.get_position_size_usd("band_a")
    from config import BAND_A_POSITION_PCT
    expected = 1000.0 * BAND_A_POSITION_PCT * 0.50
    assert abs(size - expected) < 0.01

def test_exception_not_active_in_normal():
    wm = make_wallet(1000.0)
    assert not wm.can_enter("exception")

def test_exception_active_in_harvest():
    wm = make_wallet(1000.0)
    wm.state.profit_mode = "HARVEST"
    assert wm.can_enter("exception")

def test_exception_active_when_locked():
    wm = make_wallet(1000.0)
    wm.state.profit_mode = "LOCKED"
    wm.state.session_locked = True
    wm.state.entries_halted = False
    assert wm.can_enter("exception")

def test_fade_active_in_normal():
    wm = make_wallet(1000.0)
    assert wm.can_enter("fade")

def test_fade_active_when_locked():
    wm = make_wallet(1000.0)
    wm.state.profit_mode = "LOCKED"
    wm.state.session_locked = True
    wm.state.entries_halted = False
    assert wm.can_enter("fade")

def test_fade_not_active_in_reduce():
    wm = make_wallet(1000.0)
    wm.state.loss_mode = "REDUCE"
    assert not wm.can_enter("fade")

def test_nothing_active_in_halt():
    wm = make_wallet(1000.0)
    wm.state.loss_mode = "HALT"
    for s in ["band_a","band_b","band_c",
               "exception","fade","research"]:
        assert not wm.can_enter(s)

def test_nothing_active_in_floor_breach():
    wm = make_wallet(1000.0)
    wm.state.loss_mode = "FLOOR_BREACH"
    for s in ["band_a","band_b","band_c",
               "exception","fade","research"]:
        assert not wm.can_enter(s)

def test_harvest_threshold():
    assert HARVEST_THRESHOLD == 0.08

def test_protection_threshold():
    assert PROTECTION_THRESHOLD == 0.12

def test_lock_threshold():
    assert LOCK_THRESHOLD == 0.17

def test_daily_loss_tiers():
    assert DAILY_LOSS_REDUCE_TIER == -0.10
    assert DAILY_LOSS_PAUSE_TIER == -0.15
    assert DAILY_LOSS_HALT_TIER == -0.20
