import responses
from immutable.extract.orders import Order
from immutable.extract.mints import Mint


@responses.activate
def test_orders_endpoint_integration():
    responses.add(
        responses.GET,
        "https://api.x.immutable.com/v3/orders",
        json={
            "result": [
                {
                    "order_id": 1,
                    "status": "success",
                    "user": "xyz",
                    "sell": {
                        "type": "ERC721",
                        "data": {
                            "token_id": "123",
                            "properties": {
                                "name": "Dream Shaman",
                            },
                        },
                    },
                    "buy": {
                        "type": "ETH",
                        "data": {
                            "decimals": 18,
                            "quantity": "1000000000000000000",
                        },
                    },
                    "timestamp": "2023-08-01T20:30:52.063568Z",
                }
            ],
            "remaining": 0,
            "cursor": None,
        },
        status=200,
    )

    parameters = {
        "sell_token_address": "0xacb3c6a43d15b907e8433077b6d38ae40936fe2c",
        "min_timestamp": "2023-08-01T00:00:00.00Z",
        "max_timestamp": "2023-08-01T00:30:59.99Z",
    }

    order = Order(parameters=parameters)
    assert isinstance(order.orders[0], dict)
    assert "timestamp" in order.orders[0]
    assert "order_id" in order.orders[0]
    assert "status" in order.orders[0]
    assert "user" in order.orders[0]
    assert "sell_asset" in order.orders[0]
    assert "buy_type" in order.orders[0]
    assert "buy_quantity" in order.orders[0]
    assert order.orders[0]["status"] == "success"


@responses.activate
def test_mints_endpoint_integration():
    responses.add(
        responses.GET,
        "https://api.x.immutable.com/v1/mints",
        json={
            "result": [
                {
                    "transaction_id": 12190538,
                    "status": "success",
                    "user": "xyz",
                    "token": {
                        "type": "ERC721",
                        "data": {
                            "token_id": "73583",
                            "id": "123",
                            "token_address": "abcd",
                            "quantity": "1",
                            "quantity_with_fees": "",
                        },
                    },
                    "timestamp": "2023-08-02T21:20:46.352943Z",
                }
            ],
            "remaining": 0,
            "cursor": None,
        },
        status=200,
    )

    parameters = {
        "token_address": "0xacb3c6a43d15b907e8433077b6d38ae40936fe2c",
        "min_timestamp": "2023-07-18T00:00:00.00Z",
        "max_timestamp": "2023-07-18T00:30:59.99Z",
    }

    mint = Mint(parameters=parameters)
    assert isinstance(mint.mints[0], dict)
    assert "timestamp" in mint.mints[0]
    assert "status" in mint.mints[0]
    assert "user" in mint.mints[0]
    assert "token_id" in mint.mints[0]
    assert mint.mints[0]["status"] == "success"
