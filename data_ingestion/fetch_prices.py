import yfinance as yf
import pandas as pd

def fetch_ohlcv(symbol: str, start: str, end: str | None) -> pd.DataFrame:
    """
    Fetch OHLCV price data for a single symbol.
    Handles yfinance MultiIndex column edge cases.
    """
    data = yf.download(
        symbol,
        start=start,
        end=end,
        auto_adjust=False,
        progress=False,
        group_by="column"
    )

    if data.empty:
        raise ValueError(f"No data returned for symbol {symbol}")

    # --- FIX: flatten columns safely ---
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # Normalize column names
    data.columns = (
        pd.Series(data.columns)
        .str.lower()
        .str.replace(" ", "_")
        .tolist()
    )

    data = data.reset_index()
    data.columns = [c.lower() for c in data.columns]

    data["symbol"] = symbol

    return data