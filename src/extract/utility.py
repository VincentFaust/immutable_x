import requests


class Crypto:
    def __init__(self, params):
        self.params = params
        self.base_url = (
            "https://api.x.immutable.com/v3/"
            if self.endpoint == "orders"
            else "https://api.x.immutable.com/v1/"
        )
        self.cursor = ""

        while True:
            data = self.get_main_session()
            if data["remaining"] == 1:
                self.get_main_session()
                self.json_elements(data)
                self.cursor = self.cursor_helper(data)

            else:
                break

    def get_main_session(self):
        session = requests.get(
            f"{self.base_url}{self.endpoint}?cursor={self.cursor}", params=self.params
        )
        session.raise_for_status()
        return session.json()

    def cursor_helper(self, data):
        return data["cursor"]
