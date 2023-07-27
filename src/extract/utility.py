from typing import Dict, Any
import requests


class Crypto:
    def __init__(self, params: Dict) -> None:
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

    def get_main_session(self) -> Dict[str, Any]:
        session = requests.get(
            f"{self.base_url}{self.endpoint}?cursor={self.cursor}", params=self.params
        )
        session.raise_for_status()
        return session.json()

    def cursor_helper(self, data: Dict[str, str]) -> str:
        return data["cursor"]
