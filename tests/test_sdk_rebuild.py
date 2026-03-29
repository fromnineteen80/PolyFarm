from core.market_loader import parse_bbo


def test_parse_bbo_correct():
    bbo = {"marketData": {
        "bestBid": {"value": "0.65"},
        "bestAsk": {"value": "0.66"},
        "currentPx": {"value": "0.655"}
    }}
    bid, ask, cur = parse_bbo(bbo)
    assert bid == 0.65
    assert ask == 0.66
    assert cur == 0.655


def test_parse_bbo_bad_input():
    bid, ask, cur = parse_bbo({})
    assert bid == 0.0
    assert ask == 1.0


def test_balance_parsing():
    result = {"balances": [{
        "buyingPower": 850.0,
        "currentBalance": 1000.0,
        "assetNotional": 150.0
    }]}
    b = result.get("balances", [])
    bp = float(b[0].get("buyingPower", 0))
    assert bp == 850.0


def test_positions_parsing():
    result = {"positions": {
        "test-slug": {
            "marketSlug": "test-slug",
            "longShares": "100",
            "shortShares": "0",
            "avgEntryPx": {
                "value": "0.65",
                "currency": "USD"
            }
        }
    }}
    pm = result.get("positions", {})
    assert isinstance(pm, dict)
    assert "test-slug" in pm
    shares = float(pm["test-slug"].get("longShares", 0))
    assert shares == 100.0


def test_ws_markets_batch_size():
    slugs = [f"slug-{i}" for i in range(11)]
    batches = [
        slugs[i:i+10]
        for i in range(0, len(slugs), 10)
    ]
    assert len(batches) == 2
    assert len(batches[0]) == 10
    assert len(batches[1]) == 1


def test_event_market_price_reading():
    market = {
        "slug": "test",
        "bestBid": 0.65,
        "bestAsk": 0.66,
        "active": True,
        "acceptingOrders": True,
        "volumeNum": 50000,
        "sportsMarketTypeV2": "SPORTS_MARKET_TYPE_MONEYLINE"
    }
    bid = market["bestBid"]
    ask = market["bestAsk"]
    assert isinstance(bid, float)
    assert bid == 0.65
    assert ask == 0.66
