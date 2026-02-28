from pathlib import Path
import pandas as pd

def write_csv(df: pd.DataFrame, directory: str, filename: str) -> None:
    """
    Write DataFrame to CSV, creating directories if needed.
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)

    full_path = path / filename
    df.to_csv(full_path, index=False)