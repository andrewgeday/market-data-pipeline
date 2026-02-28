# Market Data Pipeline

This repository implements a simple but realistic financial market data pipeline.
It demonstrates ingestion, validation, and storage of OHLCV equity data in a
reproducible and extensible manner.

## Overview
The pipeline:
- Fetches daily OHLCV equity data
- Performs basic schema and sanity validation
- Stores clean data in Parquet format

This project is intended to demonstrate data engineering and quantitative data
hygiene principles. It is not a trading system.

## Data Source
Data is retrieved using the `yfinance` API.

## Validation
The pipeline checks for:
- Required schema presence
- Non-negative prices and volumes
- Minimum data availability

## How to Run
```bash
pip install -r requirements.txt
python pipeline.py
```

## Notes
- Generated data and build artifacts (e.g., `__pycache__`, output files) are excluded from version control.
- This repository focuses on data ingestion and validation mechanics, not trading strategy performance.
