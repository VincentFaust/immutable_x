from extract.orders import Order
from extract.deposits import Deposit

import logging
import pandas as pd


def pipeline():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s][%(asctime)s][%(filename)s]: %(message)s",
    )

    logging.info("deposits endpoint extraction start")

    gods_cards_deposits = Deposit(
        parameters={
            "min_timestamp": "2024-11-01T00:00:00.00Z",
            "max_timestamp": "2024-11-20T23:59:59.99Z",
        }
    )

    logging.info("deposits endpoint extraction end")

    logging.info("orders endpoint extraction start")
    gods_cards_orders = Order(
        parameters=(
            {
                "sell_token_address": "0xacb3c6a43d15b907e8433077b6d38ae40936fe2c",
                "min_timestamp": "2024-11-01T00:00:00.00Z",
                "max_timestamp": "2024-11-20T00:59:59.99Z",
                "status": "filled",
            }
        ),
    )
    logging.info("orders endpoint extraction complete")

    logging.info("converting lists to pandas dataframe start")
    deposits_df = pd.DataFrame(gods_cards_deposits.deposits)
    orders_df = pd.DataFrame(gods_cards_orders.orders)

    logging.info("converting lists to pandas dataframe end")

    output_directory = "/Users/fitz/Coding/immutable_x/src/immutable/analysis"

    logging.info("creating csv start")

    deposits_df.to_csv(f"{output_directory}/deposits.csv", index=False)
    orders_df.to_csv(f"{output_directory}/orders.csv", index=False)

    logging.info("creating csv end")


if __name__ == "__main__":
    pipeline()
