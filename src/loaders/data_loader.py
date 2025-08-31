class DataLoader:
    def __init__(self):
        pass

    def download(self, tickers: list[str], timeframe="1d", start=None, end=None):
        raise NotImplementedError
