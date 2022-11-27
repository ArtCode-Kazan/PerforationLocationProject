"""Module with corrections description."""

from typing import Dict, List

from core.containers import Correction, Interval, Model, ObservationSystem


class StaticCorrection:
    """Container with description static correction."""

    def __init__(self, observation_system: ObservationSystem, model: Model):
        """Initialize class method.

        Args:
            observation_system: observation system class
            model: velocity model class

        """
        self.__observation_system = observation_system
        self.__model = model
        self.__corrections = self.__get_corrections()

    @property
    def observation_system(self) -> ObservationSystem:
        """Return current observation system.

        Returns: ObservationSystem class

        """
        return self.__observation_system

    @property
    def model(self) -> Model:
        """Return velocity model class.

        Returns:Model class

        """
        return self.model

    @property
    def corrections(self) -> List[Correction]:
        """Return list of all static corrections.

        Returns: list of all static corrections

        """
        corrections = []
        for station_index, correction_value in self.__corrections.items():
            station = self.observation_system.stations[station_index]
            corrections.append(
                Correction(
                    station_number=station.number,
                    value=correction_value
                )
            )
        return corrections

    def __get_corrections(self) -> Dict[int, float]:
        """Return static corrections values in dict format.

        Returns: Dict with keys (station index in observation system) and
        values (static correction value)

        """
        corrections = {}
        for station_id, station in enumerate(self.observation_system.stations):
            altitude_interval = Interval(
                min_val=self.observation_system.base_altitude,
                max_val=station.coordinate.altitude
            )
            correction_value = self.model.get_interval_velocity(
                altitude_interval=altitude_interval
            )
            corrections[station_id] = correction_value
        return corrections
