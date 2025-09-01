import pandas as pd
import time

from src.backtest import VectorizedBacktester
from src.strategy import SMACrossover

# from src.loaders import PolygonDataLoader
# loader = PolygonDataLoader()
# data = loader.download(["AUDUSD", "GBPUSD"], start="2023-01-01")
# print(data)

time_start = time.perf_counter()

df = pd.read_csv("data/raw/polygon/EURUSD.csv", index_col="timestamp")
bt = VectorizedBacktester(df)
strategy = SMACrossover()
result = bt.run(strategy)
print(result)

time_end = time.perf_counter()
time_taken = time_end - time_start
print(f"Time: {time_taken:.1f}s")
