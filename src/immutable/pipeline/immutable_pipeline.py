from extract.orders import Order
from extract.deposits import Deposit

import os
import logging
import pandas as pd


def save_to_csv(df, output_path):
    file_exists = os.path.exists(output_path)
    df.to_csv(output_path, mode="a", header=not file_exists, index=False)


def pipeline():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s][%(asctime)s][%(filename)s]: %(message)s",
    )

    output_directory = "/Users/fitz/Coding/immutable_x/src/immutable/analysis"
    deposits_csv = f"{output_directory}/deposits.csv"
    orders_csv = f"{output_directory}/orders.csv"

    logging.info("deposits endpoint extraction start")

    all_deposits = Deposit(
        parameters={
            "min_timestamp": "2024-11-01T00:00:00.00Z",
            "max_timestamp": "2024-11-07T23:59:59.99Z",
            "direction": "asc",
        }
    )

    logging.info("deposits endpoint extraction end")

    logging.info("orders endpoint extraction start")
    gods_cards_orders = Order(
        parameters=(
            {
                "sell_token_address": "0xacb3c6a43d15b907e8433077b6d38ae40936fe2c",
                "min_timestamp": "2024-11-01T00:00:00.00Z",
                "max_timestamp": "2024-11-07T00:59:59.99Z",
                "status": "filled",
                "direction": "asc",
            }
        ),
    )
    logging.info("orders endpoint extraction complete")

    logging.info("converting lists to pandas dataframe start")
    deposits_df = pd.DataFrame(all_deposits.deposits)
    orders_df = pd.DataFrame(gods_cards_orders.orders)

    logging.info("converting lists to pandas dataframe end")

    logging.info("creating csv start")
    save_to_csv(deposits_df, deposits_csv)
    save_to_csv(orders_df, orders_csv)

    logging.info("creating csv end")


if __name__ == "__main__":
    pipeline()
