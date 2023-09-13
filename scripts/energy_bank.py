from lib.logger import logger


class EnergyBank:
    """
    A class representing an energy bank

    Attributes:
        capacity (float): Energy bank capacity expressed in kWh.
        lvl (float): Current energy bank level expressed in kWh.
        efficiency (int): The efficiency of energy bank expressed in percentages.
    """

    def __init__(self,
                 capacity: float = 3.0,
                 lvl: float = 1.0,
                 efficiency: int = 100):                 # TODO: Not implemented!
        self.capacity = capacity
        self._lvl = lvl
        self.efficiency = efficiency

    def get_lvl(self) -> float:
        return self._lvl

    def store_energy(self, given_energy: float) -> float:
        empty_space = self.capacity - self._lvl
        if empty_space <= given_energy:
            self._lvl += given_energy
            logger.info(f"Energy bank level: {self._lvl}kWh")
            return 0.0
        else:
            self._lvl += empty_space
            logger.info(f"Energy bank is fully charged!")
            return given_energy - empty_space

    def release_energy(self, request_energy: float) -> float:
        if request_energy <= self._lvl:
            self._lvl -= request_energy
            logger.info(f"Energy bank level: {self._lvl}kWh")
            return 0.0
        else:
            rest_energy = request_energy - self._lvl
            self._lvl = 0.0
            logger.info(f"Energy bank is empty!")
            return rest_energy
