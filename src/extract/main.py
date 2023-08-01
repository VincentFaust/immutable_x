from mints import Mint
from orders import Order
from transfers import Transfer

import logging


def pipeline():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s][%(asctime)s][%(filename)s]: %(message)s",
    )

    logging.info("orders endpoint extraction start")
    gods_orders = Order(
        parameters=(
            {
                "sell_token_address": "0xacb3c6a43d15b907e8433077b6d38ae40936fe2c",
                "min_timestamp": "2023-07-18T00:00:00.00Z",
                "max_timestamp": "2023-07-18T00:30:59.99Z",
            }
        ),
    )
    logging.info("orders endpoint extraction complete")

    logging.info("mints endpoint extraction start")
    gods_mints = Mint(
        parameters=(
            {
                "token_address": "0xacb3c6a43d15b907e8433077b6d38ae40936fe2c",
                "min_timestamp": "2023-07-18T00:00:00.00Z",
                "max_timestamp": "2023-07-18T00:30:59.99Z",
                "status": "success",
            }
        ),
    )
    logging.info("mints endpoint extraction complete")

    logging.info("transfers endpoint extraction start")
    gods_transfers = Transfer(
        parameters=(
            {
                "token_address": "0xacb3c6a43d15b907e8433077b6d38ae40936fe2c",
                "min_timestamp": "2023-07-18T00:00:00.00Z",
                "max_timestamp": "2023-07-18T00:30:59.99Z",
                "status": "success",
            }
        ),
    )

    logging.info("transfers endpoint extraction complete")

    print(gods_orders.orders)
    print(gods_mints.mints)
    print(gods_transfers.transfers)


if __name__ == "__main__":
    pipeline()
