from data_loader import DataLoader


class AlphaVantageDataLoader(DataLoader):
    def __init__(self):
        super().__init__()

    def download(self, tickers: list[str], timeframe="1d", start=None, end=None):
        pass
