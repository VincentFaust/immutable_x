from utility import Crypto


class Deposit(Crypto):
    def __init__(self, params):
        self.endpoint = "deposits"
        self.deposits = []
        super().__init__(params)

    def json_elements(self, data):
        for element in data["result"]:
            timestamp = element["timestamp"].split("T")[0]
            status = element["status"]
            user = element["user"]
            token_type = element["token"]["type"]
            token_address = element["token"]["data"]["token_address"]
            quantity = float(element["token"]["data"]["quantity"]) / float(
                10 ** element["token"]["data"]["decimals"]
            )

            depositer = {
                "timestamp": timestamp,
                "status": status,
                "user": user,
                "token_type": token_type,
                "token_address": token_address,
                "quantity": quantity,
            }

            self.deposits.append(depositer)
        return self.deposits


gods_deposits = Deposit(params={"min_timestamp": "2023-07-19T00:00:00.00Z"})

print(gods_deposits.deposits)
