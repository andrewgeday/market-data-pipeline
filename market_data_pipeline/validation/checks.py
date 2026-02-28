import pandas as pd

REQUIRED_COLUMNS = {
    "date",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "symbol",
}

OPTIONAL_COLUMNS = {"adj_close"}

def validate_schema(df: pd.DataFrame) -> None:
    columns = set(df.columns)

    missing_required = REQUIRED_COLUMNS - columns
    if missing_required:
        raise ValueError(f"Missing required columns: {missing_required}")

    unknown = columns - REQUIRED_COLUMNS - OPTIONAL_COLUMNS
    if unknown:
        raise ValueError(f"Unexpected columns detected: {unknown}")

def validate_row_count(df: pd.DataFrame, min_rows: int) -> None:
    if len(df) < min_rows:
        raise ValueError("Insufficient data rows")
    
def validate_prices(df: pd.DataFrame) -> None:
    price_cols = ["open", "high", "low", "close"]

    if (df[price_cols] < 0).any().any():
        raise ValueError("Negative prices detected")

    if (df["volume"] < 0).any():
        raise ValueError("Negative volume detected")