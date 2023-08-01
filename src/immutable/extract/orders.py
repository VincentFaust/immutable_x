from typing import Dict, List
from utility import Crypto


class Order(Crypto):
    def __init__(self, parameters: Dict) -> None:
        self.endpoint = "orders"
        self.orders = []
        super().__init__(parameters)

    def json_elements(self, data: Dict) -> List[Dict]:
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
