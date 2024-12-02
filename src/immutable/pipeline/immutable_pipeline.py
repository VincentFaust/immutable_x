from extract.mints import Mint
from extract.orders import Order
from extract.transfers import Transfer

import logging
import pandas as pd


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

    logging.info("converting lists to pandas dataframe start")
    orders_df = pd.DataFrame(gods_orders.orders)
    mints_df = pd.DataFrame(gods_mints.mints)
    transfers_df = pd.DataFrame(gods_transfers.transfers)

    logging.info("converting lists to pandas dataframe end")

    output_directory = "/Users/fitz/Coding/immutable_x/src/immutable/analysis"

    logging.info("creating csv start")

    orders_df.to_csv(f"{output_directory}/orders.csv", index=False)
    mints_df.to_csv(f"{output_directory}/mints.csv", index=False)
    transfers_df.to_csv(f"{output_directory}/transfers.csv", index=False)

    logging.info("creating csv end")


if __name__ == "__main__":
    pipeline()
