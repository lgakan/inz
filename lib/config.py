from enum import Enum
from typing import Union


class CustomEnum(Enum):
    def __get__(self, instance, owner):
        return self.value


class Config(CustomEnum):
    # local_links
    LOG_FILE_PATH = "lib/program_log.log"
    DATA_ENERGY_PRODUCTION = "lib/data/energy_production2.csv"
    DATA_ENERGY_USAGE = "lib/data/energy_production2.csv"
    DATA_PRICES = "lib/data/prices.csv"
    PATH_DOWNLOAD_DIR = "C:/Users/Pawel/Downloads/PL_CENY_RYN_EN_20230830_20230829144234.csv"

    # http_links
    CSV_DOWNLOAD = f"https://www.pse.pl/getcsv/-/export/csv/PL_CENY_RYN_EN/"


class PhotovoltaicDirection(CustomEnum):
    SOUTH = "south"
    EAST_WEST = "east_west"


class DataTypes(CustomEnum):
    DF_VALUES = Union[str, int, float]
