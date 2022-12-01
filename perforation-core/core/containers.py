"""Module with common containers (dataclasses).

This module organize information about objects.

"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from core.models import (PyCoordinate, PyInterval, PyLayer,
                         PyObservationSystem, PyStation, PyVelocityModel)


@dataclass
class Coordinate:
    """Container with coordinate.

    Args:
        x: x-coordinate
        y: y-coordinate
        altitude: absolute altitude

    """

    x: float
    y: float
    altitude: float

    @property
    def tuple_view(self) -> Tuple[float, float, float]:
        """Return tuple class representation.

        Returns: tuple with x, y, altitude values

        """
        return self.x, self.y, self.altitude

    @classmethod
    def from_pymodel(cls, model: PyCoordinate) -> Coordinate:
        """Help create class from Pydantic model.

        Args:
            model: PyCoordinate class

        Returns: Coordinate class

        """
        return cls(x=model.x, y=model.y, altitude=model.altitude)

    def __eq__(self, other: Coordinate) -> bool:
        """Check equality of objects.

        Args:
            other: Coordinate class

        Returns: True if equal else False if not

        """
        return self.tuple_view == other.tuple_view


@dataclass
class Station:
    """Container with station info.

    Args:
        number: station number
        coordinate: Coordinate class with station coordinate

    """

    number: int
    coordinate: Coordinate

    @property
    def tuple_view(self) -> Tuple[int, float, float, float]:
        """Return tuple class representation.

        Returns: tuple with station number and coordinates

        """
        return (
            self.number, self.coordinate.x, self.coordinate.y,
            self.coordinate.altitude
        )

    @classmethod
    def from_pymodel(cls, model: PyStation) -> Station:
        """Help create class from Pydantic model.

        Args:
            model: PyStation class

        Returns: Station class

        """
        return cls(
            number=model.number,
            coordinate=Coordinate.from_pymodel(model=model.coordinate)
        )

    def __eq__(self, other: Station) -> bool:
        """Check equality of objects.

        Args:
            other: Station class

        Returns: True if equal else False if not

        """
        return self.tuple_view == other.tuple_view


@dataclass
class ObservationSystem:
    """Container for saving observation stations.

    Args:
        stations: list with Station objects

    """

    stations: List[Station]

    @classmethod
    def from_pymodel(cls, model: PyObservationSystem) -> ObservationSystem:
        """Help create class from Pydantic model.

        Args:
            model: PyObservationSystem class

        Returns: ObservationSystem class

        """
        stations = [Station.from_pymodel(model=x) for x in model.stations]
        return cls(stations=stations)

    @property
    def base_altitude(self) -> float:
        """Return minimal stations altitude.

        Returns: minimal altitude

        """
        return min((x.coordinate.altitude for x in self.stations))

    @property
    def stations_count(self) -> int:
        """Return stations count.

        Returns: stations count

        """
        return len(self.stations)

    def __eq__(self, other: ObservationSystem) -> bool:
        """Check equality of objects.

        Args:
            other: ObservationSystem class

        Returns: True if equal else False if not

        """
        if self.stations_count != other.stations_count:
            return False
        for i in range(self.stations_count):
            if self.stations[i] != other.stations[i]:
                return False
        return True


class Interval:
    """Container for Interval abstraction."""

    def __init__(self, min_val: float, max_val: float):
        """Initialize class method.

        Args:
            min_val: minimal interval value
            max_val: maximal interval value

        """
        if min_val > max_val:
            raise ValueError('Invalid max and min values')

        self.min_val = min_val
        self.max_val = max_val

    @classmethod
    def from_pymodel(cls, model: PyInterval) -> Interval:
        """Help create class from Pydantic model.

        Args:
            model: PyInterval class

        Returns: Interval class

        """
        return cls(min_val=model.min_val, max_val=model.max_val)

    @property
    def tuple_view(self) -> Tuple[float, float]:
        """Return interval limit in tuple.

        Returns: tuple with minimal and maximal values

        """
        return self.min_val, self.max_val

    @property
    def length(self) -> float:
        """Return interval size.

        Returns: float value with interval size

        """
        return self.max_val - self.min_val

    @property
    def middle(self) -> float:
        """Return center of interval.

        Returns:float value with center point of interval

        """
        return (self.max_val + self.min_val) / 2

    def __eq__(self, other: Interval) -> bool:
        """Check equality of objects.

        Args:
            other: Interval class

        Returns: True if equal else False if not

        """
        return self.tuple_view == other.tuple_view


@dataclass
class Layer:
    """Container with description Layer class.

    Args:
        altitude_interval: Interval with altitudes of layer top and bottom
        vp: velocity value (m/s)

    """

    altitude_interval: Interval
    vp: float

    @classmethod
    def from_pymodel(cls, model: PyLayer) -> Layer:
        """Help create class from Pydantic model.

        Args:
            model: PyLayer class

        Returns: Layer class

        """
        return cls(
            altitude_interval=Interval.from_pymodel(
                model=model.altitude_interval
            ),
            vp=model.vp
        )

    @property
    def thickness(self) -> float:
        """Return layer thickness in meters.

        Returns: layer thickness in meters

        """
        return self.altitude_interval.length

    @property
    def middle_altitude(self) -> float:
        """Return middle layer altitude.

        Returns: middle layer altitude

        """
        return self.altitude_interval.middle

    @property
    def travel_time(self) -> float:
        """Return ray travel time in layer body.

        Returns: ray travel time

        """
        return self.thickness / self.vp

    def __str__(self) -> str:
        """Return string presentation in print methods.

        Returns: string presentation

        """
        interval = self.altitude_interval
        return f'interval={interval.max_val}/{interval.min_val} v={self.vp}'

    def __eq__(self, other: Layer) -> bool:
        """Check equality of objects.

        Args:
            other: Layer class

        Returns: True if equal else False if not

        """
        origin_tuple_view = self.altitude_interval.tuple_view
        other_tuple_view = other.altitude_interval.tuple_view
        if origin_tuple_view != other_tuple_view:
            return False

        if self.vp != other.vp:
            return False
        return True


class VelocityModel:
    """Class with Model description."""

    def __init__(self, layers: List[Layer]):
        """Initialize class method.

        Args:
            layers: list of Layer objects

        """
        if not layers:
            raise ValueError('Empty layers list')

        layers.sort(key=lambda x: x.altitude_interval.max_val, reverse=True)
        self.__layers = layers

    @classmethod
    def from_pymodel(cls, model: PyVelocityModel) -> VelocityModel:
        """Help create class from Pydantic model.

        Args:
            model: PyVelocityModel class

        Returns: VelocityModel class

        """
        layers = [Layer.from_pymodel(model=x) for x in model.layers]
        return cls(layers=layers)

    @property
    def layers(self) -> List[Layer]:
        """Return list of sorted model layers by descending altitudes.

        Returns: list of model layers

        """
        return self.__layers

    @property
    def min_altitude(self) -> float:
        """Return minimal model altitude.

        Returns: minimal model altitude

        """
        return self.layers[-1].altitude_interval.min_val

    @property
    def max_altitude(self) -> float:
        """Return maximal model altitude.

        Returns: maximal model altitude

        """
        return self.layers[0].altitude_interval.max_val

    def get_velocity_by_altitude(self, altitude: float) -> float:
        """Return model velocity value by altitude.

        Args:
            altitude: altitude value

        Returns: velocity value

        """
        if altitude < self.min_altitude:
            raise ValueError('Invalid altitude value')

        if altitude == self.min_altitude:
            return self.layers[-1].vp

        if altitude > self.max_altitude:
            raise ValueError('Invalid altitude value')

        for layer in self.layers:
            bottom_altitude, top_altitude = layer.altitude_interval.tuple_view
            if bottom_altitude < altitude <= top_altitude:
                return layer.vp

    def get_interval_velocity(self, altitude_interval: Interval) -> float:
        """Return velocity in altitude interval.

        Args:
            altitude_interval: interval with needed altitudes

        Returns: velocity value in altitude interval

        """
        if altitude_interval.min_val < self.min_altitude:
            raise ValueError('Invalid altitude interval')

        if altitude_interval.max_val > self.max_altitude:
            raise ValueError('Invalid altitude interval')

        if altitude_interval.length == 0:
            return self.get_velocity_by_altitude(
                altitude=altitude_interval.max_val
            )

        total_thickness, total_time = 0, 0
        for layer in self.layers:
            bottom_altitude, top_altitude = layer.altitude_interval.tuple_view
            if bottom_altitude > altitude_interval.max_val:
                continue

            if top_altitude < altitude_interval.min_val:
                break

            if bottom_altitude <= altitude_interval.max_val < top_altitude:
                thickness = altitude_interval.max_val - bottom_altitude
            elif bottom_altitude < altitude_interval.min_val <= top_altitude:
                thickness = top_altitude - altitude_interval.min_val
            else:
                thickness = layer.thickness

            total_time += thickness / layer.vp
            total_thickness += thickness
        return total_thickness / total_time

    def __eq__(self, other: VelocityModel) -> bool:
        """Check equality of objects.

        Args:
            other: VelocityModel class

        Returns: True if equal else False if not

        """
        if len(self.layers) != len(other.layers):
            return False

        for i in range(len(self.layers)):
            if self.layers[i] != other.layers[i]:
                return False
        return True


@dataclass
class Correction:
    """Container with description Correction class.

    Args:
        station_number: station number
        value: correction value

    """

    station_number: int
    value: float
