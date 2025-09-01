import pandas as pd

# Abstract class for strategies


class Strategy:
    def __init__(self, name: str):
        self.name = name
    
    def __str__(self):
        return self.name


class VectorizedStrategy(Strategy):
    def __init__(self, name: str):
        super().__init__(name)

    def generate_signal(self, full_df: pd.DataFrame):
        # return series of best action: BUY, HOLD, or SELL
        raise NotImplementedError


class RowByRowStrategy(Strategy):
    def __init__(self, name: str):
        super().__init__(name)

    def generate_signal(self, history_df: pd.DataFrame):
        # return the best action: BUY, HOLD, or SELL
        raise NotImplementedError


class SMACrossover(VectorizedStrategy):
    def __init__(self, name="sma_crossover", *, fast=5, slow=20):
        super().__init__(name)
        self.fast = fast
        self.slow = slow

    def generate_signal(self, df: pd.DataFrame) -> pd.Series:
        df = df.copy()
        df["fast_sma"] = df["close"].rolling(self.fast).mean()
        df["slow_sma"] = df["close"].rolling(self.slow).mean()
        signal = pd.Series(0, index=df.index)

        signal[df["fast_sma"] > df["slow_sma"]] = 1
        signal[df["fast_sma"] < df["slow_sma"]] = -1
        return signal
