def test_price_velocity_falling():
    from core.ws_markets import MarketsWebSocket
    from datetime import datetime, timezone, timedelta
    ws = MarketsWebSocket.__new__(MarketsWebSocket)
    ws._price_history = {}
    ws._trade_flow = {}
    ws._HISTORY_WINDOW_SECONDS = 1800
    now = datetime.now(timezone.utc)
    ws._price_history["test-slug"] = [
        {"price": 0.65, "bid": 0.64, "ask": 0.66, "timestamp": (now - timedelta(minutes=10)).isoformat()},
        {"price": 0.55, "bid": 0.54, "ask": 0.56, "timestamp": now.isoformat()},
    ]
    velocity, direction = ws.calculate_velocity("test-slug")
    assert direction == "falling"
    assert velocity < -0.2


def test_price_velocity_stable():
    from core.ws_markets import MarketsWebSocket
    from datetime import datetime, timezone, timedelta
    ws = MarketsWebSocket.__new__(MarketsWebSocket)
    ws._price_history = {}
    ws._HISTORY_WINDOW_SECONDS = 1800
    now = datetime.now(timezone.utc)
    ws._price_history["test-slug"] = [
        {"price": 0.65, "bid": 0.64, "ask": 0.66, "timestamp": (now - timedelta(minutes=10)).isoformat()},
        {"price": 0.651, "bid": 0.641, "ask": 0.661, "timestamp": now.isoformat()},
    ]
    velocity, direction = ws.calculate_velocity("test-slug")
    assert direction == "stable"


def test_net_buy_pressure():
    from core.ws_markets import MarketsWebSocket
    ws = MarketsWebSocket.__new__(MarketsWebSocket)
    ws._trade_flow = {"test-slug": {"buy_volume": 600.0, "sell_volume": 400.0}}
    pressure = ws.get_net_buy_pressure("test-slug")
    assert pressure == 1.5


def test_insufficient_history():
    from core.ws_markets import MarketsWebSocket
    ws = MarketsWebSocket.__new__(MarketsWebSocket)
    ws._price_history = {}
    ws._HISTORY_WINDOW_SECONDS = 1800
    velocity, direction = ws.calculate_velocity("no-data-slug")
    assert direction == "stable"
    assert velocity == 0.0
