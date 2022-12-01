"""Model with Pydantic models.

This module organize information for sending and receiving by http

"""

from typing import List, Union

from pydantic import BaseModel


class Response(BaseModel):
    """Http response model.

    Args:
        status: bool (True if request successful, False - if not)
        message: message text
        data: receiving data from server to client

    """

    status: bool
    message: str
    data: Union[dict, list]


class PyCoordinate(BaseModel):
    """Coordinate model.

    Args:
        x: x-coordinate
        y: y-coordinate
        altitude: absolute altitude

    """

    x: float
    y: float
    altitude: float


class PyStation(BaseModel):
    """Station model.

    Args:
        number: station number
        coordinate: PyCoordinate class with station coordinate

    """

    number: int
    coordinate: PyCoordinate


class PyObservationSystem(BaseModel):
    """ObservationSystem model.

    Args:
        stations: list with PyStation objects

    """

    stations: List[PyStation]


class PyInterval(BaseModel):
    """Interval model.

    Args:
        min_val: minimal interval value
        max_val: maximal interval value

    """

    min_val: float
    max_val: float


class PyLayer(BaseModel):
    """Layer model.

    Args:
        altitude_interval: PyInterval class
        vp: velocity value

    """

    altitude_interval: PyInterval
    vp: float


class PyVelocityModel(BaseModel):
    """Velocity model.

    Args:
        layers: list of PyLayer class

    """

    layers: List[PyLayer]


class PyCorrection(BaseModel):
    """Correction model.

    Args:
        station_number: number of observation station
        value: correction value

    """

    station_number: int
    value: float


class PyCorrections(BaseModel):
    """Corrections model.

    Args:
        corrections: list of PyCorrection

    """

    corrections: List[PyCorrection]
