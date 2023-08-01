from typing import Dict, List
from .utility import Crypto


class Mint(Crypto):
    def __init__(self, parameters: Dict) -> None:
        self.endpoint = "mints"
        self.mints = []
        super().__init__(parameters)

    def json_elements(self, data: Dict) -> List[Dict]:
        for element in data["result"]:
            timestamp = element["timestamp"].split("T")[0]
            status = element["status"]
            user = element["user"]
            token_id = element["token"]["data"]["token_id"]
            id = element["token"]["data"]["id"]

            minter = {
                "timestamp": timestamp,
                "status": status,
                "user": user,
                "token_id": token_id,
            }
            self.mints.append(minter)
        return self.mints
