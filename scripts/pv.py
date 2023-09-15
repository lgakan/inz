from lib.config import Config, PhotovoltaicDirection
from lib.config import DataTypes
from lib.file_manager import CSVFile


class Pv:
    """
    A class representing household photovoltaic system.

    Attributes:
        production (float): The amount of energy generated by photovoltaics expressed in kWh.
        csv_file (CSVFile): The CSVFile class object for csv files management.
        size (float): The size of photovoltaic installation expressed in kWp.
        efficiency (int): The efficiency of photovoltaic installation expressed in percentages.
        direction (PhotovoltaicDirection): The photovoltaic installation: east-west or south.
    """

    def __init__(self,
                 production: float = 0.0,
                 size: float = 10.0,  # TODO: Not implemented!
                 efficiency: int = 100,  # TODO: Not implemented!
                 direction: PhotovoltaicDirection = PhotovoltaicDirection.EAST_WEST):  # TODO: Not implemented!
        self.production = production
        self.csv_file = CSVFile(Config.DATA_ENERGY_PRODUCTION)
        self.size = size
        self.efficiency = efficiency
        self.direction = direction

    def get_production_by_date(self, date: DataTypes.TIMESTAMP) -> float:
        return self.csv_file.get_colum_value_by_date("PV gen (kW)", date)


# Example
# if __name__ == "__main__":
#     pv = Pv()
#     print(pv.get_production_by_date(pd.to_datetime("01.01.2015 06:00:00")))
