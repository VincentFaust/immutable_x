from utility import Crypto


class Orders(Crypto):
    def __init__(self, parameters):
        self.endpoint = "orders"
        self.orders = []
        super().__init__(parameters)

    def json_elements(self, data):
        for element in data["result"]:
            updated_timestamp = element["timestamp"].split("T")[0]
            order_id = element["order_id"]
            status = element["status"]
            user = element["user"]
            sell_asset = element["sell"]["data"]["properties"]["name"]
            buy_type = element["buy"]["type"]
            buy_quantity = float(element["buy"]["data"]["quantity"]) / 10 ** float(
                element["buy"]["data"]["decimals"]
            )

            orderer = {
                "timestamp": updated_timestamp,
                "order_id": order_id,
                "status": status,
                "user": user,
                "sell_asset": sell_asset,
                "buy_type": buy_type,
                "buy_quantity": buy_quantity,
            }

            self.orders.append(orderer)
        return self.orders


gods_orders = Orders(
    parameters=(
        {
            "sell_token_address": "0xacb3c6a43d15b907e8433077b6d38ae40936fe2c",
            "min_timestamp": "2023-07-18T00:00:00.00Z",
            "max_timestamp": "2023-07-18T00:59:59.99Z",
        }
    ),
)

print(gods_orders.orders)
