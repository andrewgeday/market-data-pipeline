import pandas as pd
from pathlib import Path

def write_parquet(df: pd.DataFrame, path: str, filename: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)
    full_path = Path(path) / filename
    df.to_parquet(full_path, index=False)