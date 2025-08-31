import os

from dotenv import load_dotenv

from src.loaders import PolygonDataLoader


load_dotenv()

api_key = os.getenv("POLYGON_API_KEY")
loader = PolygonDataLoader(api_key)
dict_ = loader.download(["EURUSD"], start="2011-05-05", end="2012-05-05")

print(dict_)

df = dict_["EURUSD"]
print(df)

df.to_csv("EURUSD.csv")
print("Save to csv")