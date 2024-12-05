from typing import Dict, List
from .utility import Crypto


class Deposit(Crypto):
    def __init__(self, parameters: Dict) -> None:
        self.endpoint = "deposits"
        self.deposits = []
        super().__init__(parameters)

    def json_elements(self, data: Dict):
        for element in data["result"]:
            timestamp = element["timestamp"].split("T")[0]
            transaction_id = element["transaction_id"]
            user_id = element["user"]
            status = element["status"]
            token_type = element["token"]["type"]
            quantity = float(element["token"]["data"]["quantity"]) / 10 ** float(
                element["token"]["data"]["decimals"]
            )

            depositer = {
                "timestamp": timestamp,
                "transaction_id": transaction_id,
                "user_id": user_id,
                "status": status,
                "token_type": token_type,
                "quantity": quantity,
            }

            self.deposits.append(depositer)

        return self.deposits
