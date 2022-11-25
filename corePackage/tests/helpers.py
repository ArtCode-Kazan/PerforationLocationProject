"""Module with helpful function for test designs."""

from random import randint
from typing import List

from core.containers import Coordinate, Interval, Layer, Station


def generate_stations() -> List[Station]:
    """Return list of random stations.

    Returns: list of stations

    """
    stations = []
    for i in range(randint(1, 100)):
        stations.append(
            Station(
                number=i + 1,
                coordinate=Coordinate(
                    x=randint(-1000, 1000),
                    y=randint(-1000, 1000),
                    altitude=randint(-200, 200)
                )
            )
        )
    return stations


def generate_layers() -> List[Layer]:
    """Return list of random layers.

    Returns: list of random layers

    """
    layers = []
    edges = list(set([randint(-2000, 200) for _ in range(100)]))
    edges.sort()
    for i in range(len(edges) - 1):
        min_value, max_value = edges[i: i + 2]
        interval = Interval(min_val=min_value, max_val=max_value)
        vp = randint(100, 2000)
        layers.append(Layer(altitude_interval=interval, vp=vp))
    return layers
