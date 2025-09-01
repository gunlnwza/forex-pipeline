from src.loaders import PolygonDataLoader

loader = PolygonDataLoader()
data = loader.download(["AUDUSD", "GBPUSD"], start="2023-01-01")

print(data)
