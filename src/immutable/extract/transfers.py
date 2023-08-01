from typing import Dict, List
from .utility import Crypto


class Transfer(Crypto):
    def __init__(self, parameters: Dict) -> None:
        self.endpoint = "transfers"
        self.transfers = []
        super().__init__(parameters)

    def json_elements(self, data: Dict) -> List[Dict]:
        for element in data["result"]:
            timestamp = element["timestamp"].split("T")[0]
            user = element["user"]
            token_type = element["token"]["type"]
            token_id = element["token"]["data"]["token_id"]
            id = element["token"]["data"]["id"]

            transferer = {
                "timestamp": timestamp,
                "user": user,
                "token_type": token_type,
                "token_id": token_id,
                "id": id,
            }

            self.transfers.append(transferer)
        return self.transfers
