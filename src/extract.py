import requests 

class Orders:
    
    def __init__(self, base_url, endpoint, params):
        self.base_url = base_url 
        self.endpoint = endpoint 
        self.cursor = ""
        self.params = params 
    

    def get_main_session(self):
        session = requests.get(f"{self.base_url}{self.endpoint}?cursor={self.cursor}", params=self.params) 
        session.raise_for_status()
        return session.json()
    
    def cursor_helper(self):
        pass 


query_params = {
    "sell_token_address" : "0xacb3c6a43d15b907e8433077b6d38ae40936fe2c"
}

gods_orders = Orders("https://api.x.immutable.com/v3/", "orders", query_params)
print(gods_orders.get_main_session())