import os
from datetime import datetime, timedelta, timezone

import requests
import pandas as pd

from data_loader import DataLoader


class PolygonDataLoader(DataLoader):
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key
        self.base_url = "https://api.polygon.io"

    def download(self, tickers: list[str], timeframe="1d", start=None, end=None) -> dict:
        result = {}
        for ticker in tickers:
            df = self._download_single_ticker(ticker, timeframe, start, end)
            result[ticker] = df
        return result
    
    def _download_single_ticker(self, ticker: str, timeframe: str, start=None, end=None) -> pd.DataFrame:  # TODO
        match timeframe:
            case "1d":
                tf_multiplier = 1
                tf_unit = "day"
            case "1w":
                tf_multiplier = 1
                tf_unit = "week"
            case "1m":
                tf_multiplier = 1
                tf_unit = "month"
            case _:
                raise ValueError(f"timeframe '{timeframe}' not supported")

        # Default to last 30 days
        if not end:
            end = datetime.now(timezone.utc)
        if not start:
            start = end - timedelta(days=30)

        url = f"{self.base_url}/v2/aggs/ticker/C:{ticker}/range/{tf_multiplier}/{tf_unit}/{start}/{end}"
        params = {"adjusted": "true", "sort": "asc", "apiKey": self.api_key}

        response = requests.get(url, params)
        if not response.ok:
            raise RuntimeError(f"Polygon API error: {response.status_code} {response.text}")

        data = response.json().get("results", [])
        if not data:
            raise ValueError(f"No data returned for {ticker}")
        
        df = pd.DataFrame(data)
        df["t"] = pd.to_datetime(df["t"], unit="ms")
        df = df.rename(columns={
            "t": "timestamp",
            "o": "open",
            "h": "high",
            "l": "low",
            "c": "close",
            "v": "volume"
        })
        df.set_index("timestamp", inplace=True)
        return df
