from data_loader import DataLoader
from polygon_data_loader import PolygonDataLoader
from alpha_vantage_data_loader import AlphaVantageDataLoader
from oanda_data_loader import OandaDataLoader


def get_loader(name: str) -> DataLoader:
    match name.lower():
        case "polygon": return PolygonDataLoader()
        case "alpha": return AlphaVantageDataLoader()
        case "oanda": return OandaDataLoader()
        case _: raise ValueError("Unknown data loader")
