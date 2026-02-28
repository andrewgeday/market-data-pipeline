import yaml
import pandas as pd

from data_ingestion.fetch_prices import fetch_ohlcv
from data_ingestion.symbols import EQUITY_SYMBOLS
from data_validation.checks import (
    validate_schema,
    validate_prices,
    validate_row_count
)
from storage.write_csv import write_csv


def load_config(path: str = "config.yaml") -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def run_pipeline() -> None:
    config = load_config()

    all_data = []

    for symbol in EQUITY_SYMBOLS:
        df = fetch_ohlcv(
            symbol,
            start=config["data"]["start_date"],
            end=config["data"]["end_date"]
        )
        print(df.columns.tolist())
        validate_schema(df)
        validate_prices(df)
        validate_row_count(df, config["validation"]["min_rows"])

        all_data.append(df)

    final_df = pd.concat(all_data, ignore_index=True)

    write_csv(
        final_df,
        directory=config["storage"]["directory"],
        filename=config["storage"]["filename"]
    )

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()