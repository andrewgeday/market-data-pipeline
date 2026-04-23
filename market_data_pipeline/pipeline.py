import yaml
import pandas as pd
from pathlib import Path
from datetime import datetime
import json

from market_data_pipeline.ingestion.fetch_prices import fetch_ohlcv
from market_data_pipeline.ingestion.symbols import get_sp500_symbols
from market_data_pipeline.validation.checks import (
    validate_schema,
    validate_prices,
    validate_row_count
)
from market_data_pipeline.storage.write_csv import write_csv

BASE_DIR = Path(__file__).resolve().parents[1]

def load_config(path: str = "config.yaml") -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def run_pipeline(config_path: str = "config.yaml") -> str:
    config = load_config(path=config_path)

    all_data = []

    symbols = get_sp500_symbols(limit=50)
    
    for symbol in symbols:
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

    output_dir = BASE_DIR / config["storage"]["directory"]
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    base_filename = config["storage"]["filename"].replace(".csv", "")
    filename = f"{base_filename}_{timestamp}.csv"

    full_path = output_dir / filename

    write_csv(
        final_df,
        directory=str(output_dir),
        filename=filename
    )

    print(f"Output file: {full_path}")

    metadata = {
    "timestamp": timestamp,
    "symbols": get_sp500_symbols(),
    "start_date": config["data"]["start_date"],
    "end_date": config["data"]["end_date"],
    "n_rows": len(final_df),
    "output_file": str(full_path)
    }

    metadata_path = output_dir / f"metadata_{timestamp}.json"

    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"Metadata saved: {metadata_path}")

    print("Pipeline completed successfully.")

    return str(full_path)

if __name__ == "__main__":
    run_pipeline()