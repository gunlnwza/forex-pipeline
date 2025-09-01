import pandas as pd

from src.strategy import Strategy, VectorizedStrategy, RowByRowStrategy

# Runs strategies on historical data


class Backtester:
    def __init__(self, full_df: pd.DataFrame):
        self._full_df = full_df

    def run(self, strategy: Strategy):
        raise NotImplementedError
    
    
class VectorizedBacktester(Backtester):
    def __init__(self, full_df: pd.DataFrame):
        super().__init__(full_df)

    def run(self, strategy: VectorizedStrategy):
        df = self._full_df.copy()
        df["signal"] = strategy.generate_signal(df)

        # Example: assume 1 unit per trade
        position = None
        trades = []

        for i in range(len(df)):
            sig = df.iloc[i]["signal"]
            price = df.iloc[i]["close"]

            if sig == 1 and position is None:
                position = (i, price)
            elif sig == -1 and position is not None:
                entry_i, entry_price = position
                pnl = price - entry_price
                trades.append({"entry": entry_i, "exit": i, "pnl": pnl})
                position = None

        return BacktestResults(trades)


class RowByRowBacktester(Backtester):
    def __init__(self, full_df: pd.DataFrame):
        super().__init__(full_df)

    def run(self, strategy: RowByRowStrategy):
        df = self._full_df.copy()
        lookback = 20  # or strategy-defined
        trades = []
        position = None
        for i in range(lookback, len(df)):
            history = df.iloc[i - lookback:i]
            row = df.iloc[i]
            sig = strategy.generate_signal(history)

            if sig == "BUY" and position is None:
                position = (i, row["close"])
            elif sig == "SELL" and position is not None:
                entry_i, entry_price = position
                pnl = row["close"] - entry_price
                trades.append({"entry": entry_i, "exit": i, "pnl": pnl})
                position = None
        
        return BacktestResults(trades)


class BacktestResults:
    def __init__(self, trades):
        self.trades = trades
        self._make_summary()
        
    def _make_summary(self):
        self.profit = sum(t["pnl"] for t in self.trades if t["pnl"] > 0)
        self.loss = sum(t["pnl"] for t in self.trades if t["pnl"] <= 0)
        self.pnl = self.profit + self.loss

        self.win_trades = sum(1 for t in self.trades if t["pnl"] > 0)
        self.loss_trades = sum(1 for t in self.trades if t["pnl"] <= 0)
        self.total_trades = len(self.trades)
        self.win_rate = self.win_trades / self.total_trades

        self.mean = (self.profit + self.loss) / self.total_trades
        self.std = sum(t["pnl"] - self.mean for t in self.trades) / self.total_trades
        risk_free_rate = 0.02
        self.sharpe = (self.mean - risk_free_rate) / self.std

        data = (self.profit, self.loss, self.pnl,
                self.win_trades, self.loss_trades, self.total_trades, self.win_rate,
                self.mean, self.std, self.sharpe)
        index = ("profit", "loss", "pnl",
                 "win_trades", "loss_trades", "total_trades", "win_rate",
                 "mean", "std", "sharpe")
        self.serie = pd.Series(data, index)

    def __str__(self):
        return str(self.serie)

    def plot():
        pass
    