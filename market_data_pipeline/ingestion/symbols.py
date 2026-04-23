import pandas as pd
import requests


def get_sp500_symbols(limit: int = 50) -> list:
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    tables = pd.read_html(response.text)
    symbols = tables[0]["Symbol"].tolist()

    # Fix Yahoo format
    symbols = [s.replace(".", "-") for s in symbols]

    return symbols[:limit]