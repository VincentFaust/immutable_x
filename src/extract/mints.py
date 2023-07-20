from utility import Crypto


class Mint(Crypto):
    def __init__(self, parameters):
        self.endpoint = "mints"
        self.mints = []
        super().__init__(parameters)

    def json_elements(self, data):
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


gods_mints = Mint(
    parameters=(
        {
            "token_address": "0xacb3c6a43d15b907e8433077b6d38ae40936fe2c",
            "min_timestamp": "2023-07-18T00:00:00.00Z",
            "max_timestamp": "2023-07-18T01:59:59.99Z",
            "status": "success",
        }
    ),
)

print(gods_mints.mints)
