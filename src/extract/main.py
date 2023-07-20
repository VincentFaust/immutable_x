from mints import Mint
from orders import Order
from transfers import Transfer


def main():
    gods_orders = Order(
        parameters=(
            {
                "sell_token_address": "0xacb3c6a43d15b907e8433077b6d38ae40936fe2c",
                "min_timestamp": "2023-07-18T00:00:00.00Z",
                "max_timestamp": "2023-07-18T00:59:59.99Z",
            }
        ),
    )

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

    gods_transfers = Transfer(
        parameters=(
            {
                "token_address": "0xacb3c6a43d15b907e8433077b6d38ae40936fe2c",
                "min_timestamp": "2023-07-18T00:00:00.00Z",
                "max_timestamp": "2023-07-18T01:59:59.99Z",
                "status": "success",
            }
        ),
    )

    print(gods_orders.orders)
    print(gods_mints.mints)
    print(gods_transfers.transfers)


if __name__ == "__main__":
    main()
