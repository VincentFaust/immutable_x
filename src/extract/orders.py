import requests


class Orders:
    def __init__(self, base_url, endpoint, params):
        self.base_url = base_url
        self.cursor = ""
        self.endpoint = endpoint
        self.orders = []
        self.params = params

    def get_main_session(self):
        session = requests.get(
            f"{self.base_url}{self.endpoint}?cursor={self.cursor}", params=self.params
        )
        session.raise_for_status()
        return session.json()

    def cursor_helper(self):
        pass

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


query_params = {
    "sell_token_address": "0xacb3c6a43d15b907e8433077b6d38ae40936fe2c",
    "min_timestamp": "2023-07-18T00:00:00.00Z",
}

gods_orders = Orders("https://api.x.immutable.com/v3/", "orders", params=query_params)

data = gods_orders.get_main_session()

results = gods_orders.json_elements(data)
print(results)
