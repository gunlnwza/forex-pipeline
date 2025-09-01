import pandas as pd

from base_strategy import Strategy


class RowByRowStrategy(Strategy):
    def __init__(self, name: str):
        super().__init__(name)

    def generate_signal(self, history_df: pd.DataFrame):
        # return the best action: BUY, HOLD, or SELL
        raise NotImplementedError
