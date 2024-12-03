from extract.mints import Mint
from extract.orders import Order

import logging
import pandas as pd


def pipeline():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s][%(asctime)s][%(filename)s]: %(message)s",
    )

    logging.info("orders endpoint extraction start")
    hro_orders = Order(
        parameters=(
            {
                "sell_token_address": "0x8cb332602d2f614b570c7631202e5bf4bb93f3f6",
                "min_timestamp": "2023-07-18T00:00:00.00Z",
                "max_timestamp": "2023-07-30T00:30:59.99Z",
                "status": "filled",
            }
        ),
    )
    logging.info("orders endpoint extraction complete")

    logging.info("mints endpoint extraction start")
    hro_mints = Mint(
        parameters=(
            {
                "token_address": "0x8cb332602d2f614b570c7631202e5bf4bb93f3f6",
                "min_timestamp": "2023-07-18T00:00:00.00Z",
                "max_timestamp": "2023-07-30T00:30:59.99Z",
                "status": "success",
            }
        ),
    )
    logging.info("mints endpoint extraction complete")

    logging.info("converting lists to pandas dataframe start")
    orders_df = pd.DataFrame(hro_orders.orders)
    mints_df = pd.DataFrame(hro_mints.mints)

    logging.info("converting lists to pandas dataframe end")

    output_directory = "/Users/fitz/Coding/immutable_x/src/immutable/analysis"

    logging.info("creating csv start")

    orders_df.to_csv(f"{output_directory}/orders.csv", index=False)
    mints_df.to_csv(f"{output_directory}/mints.csv", index=False)

    logging.info("creating csv end")


if __name__ == "__main__":
    pipeline()
