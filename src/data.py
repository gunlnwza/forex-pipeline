import os
from datetime import datetime, timedelta, timezone

import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class DataLoader:
    def __init__(self):
        pass

    def download(self, tickers: list[str], *, timeframe="1d", start=None, end=None):
        raise NotImplementedError
    
    def cache(self, data: dict[str, pd.DataFrame]):
        raise NotImplementedError


class PolygonDataLoader(DataLoader):
    def __init__(self, api_key=None):
        super().__init__()
        self.api_key = api_key or os.getenv("POLYGON_API_KEY")
        self.base_url = "https://api.polygon.io"
        self.data_dir = "data/raw/polygon"

    def download(self, tickers: list[str], *, timeframe="1D", start=None, end=None) -> dict[str, pd.DataFrame]:
        data = {}
        for ticker in tickers:
            df = self._download_single_ticker(ticker, timeframe, start, end)
            data[ticker] = df
        self.cache(data)
        return data
    
    def cache(self, data: dict[str, pd.DataFrame]):
        for ticker, df in data.items():
            self._cache_single_df(ticker, df)

    def _map_tf_params(self, timeframe: str):
        match timeframe:
            case "1D": return 1, "day"
            case "1W": return 1, "week"
            case "1M": return 1, "month"
            case _: raise ValueError(f"timeframe '{timeframe}' not supported")

    def _solve_time_range(self, start, end):
        # Default to last 30 days
        if not end:
            end = datetime.now(timezone.utc)
            end_str = end.strftime("%Y-%m-%d")
        else:
            end_str = end
            
        if not start:
            start = end - timedelta(days=30)
            start_str = start.strftime("%Y-%m-%d")
        else:
            start_str = start
        
        return start_str, end_str
    
    def _format_df(self, df: pd.DataFrame) -> pd.DataFrame:
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

    def _download_single_ticker(self, ticker: str, timeframe: str, start=None, end=None) -> pd.DataFrame:
        tf_multiplier, tf_unit = self._map_tf_params(timeframe)
        start, end = self._solve_time_range(start, end)

        url = f"{self.base_url}/v2/aggs/ticker/C:{ticker}/range/{tf_multiplier}/{tf_unit}/{start}/{end}"
        params = {"adjusted": "true", "sort": "asc", "apiKey": self.api_key}
        response = requests.get(url, params)
        if not response.ok:
            raise RuntimeError(f"Polygon API error: {response.status_code} {response.text}")

        data = response.json().get("results", [])
        if not data:
            raise ValueError(f"No data returned for {ticker}")

        df = pd.DataFrame(data)
        df = self._format_df(df)
        return df

    def _cache_single_df(self, ticker: str, df: pd.DataFrame):
        filename = f"{self.data_dir}/{ticker}.csv"
        df.to_csv(filename)


class AlphaVantageDataLoader(DataLoader):
    def __init__(self):
        super().__init__()

    def download(self, tickers: list[str], *, timeframe="1d", start=None, end=None):
        pass


class OandaDataLoader(DataLoader):
    def __init__(self):
        super().__init__()

    def download(self, tickers: list[str], *, timeframe="1d", start=None, end=None):
        pass


def get_loader(name: str) -> DataLoader:
    match name.lower():
        case "polygon": return PolygonDataLoader()
        case "alpha": return AlphaVantageDataLoader()
        case "oanda": return OandaDataLoader()
        case _: raise ValueError("Unknown data loader")
