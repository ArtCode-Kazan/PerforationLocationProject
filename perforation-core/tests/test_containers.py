from random import randint

import pytest
from core.containers import (Coordinate, Interval, Layer, ObservationSystem,
                             Station, VelocityModel)
from core.models import (PyCoordinate, PyInterval, PyLayer,
                         PyObservationSystem, PyStation, PyVelocityModel)
from hamcrest import assert_that, equal_to, is_
from helpers import generate_layers, generate_stations


class TestCoordinate:
    def test_tuple_view(self):
        obj = Coordinate(x=1, y=2, altitude=3)
        expected_value = (1, 2, 3)
        assert_that(
            actual_or_assertion=obj.tuple_view,
            matcher=equal_to(expected_value)
        )

    def test_from_pymodel(self):
        obj = Coordinate(x=1, y=2, altitude=3)

        py_model = PyCoordinate(x=obj.x, y=obj.y, altitude=obj.altitude)
        assert_that(
            actual_or_assertion=Coordinate.from_pymodel(model=py_model),
            matcher=equal_to(obj)
        )


class TestStation:
    def test_tuple_view(self):
        obj = Station(
            number=1, coordinate=Coordinate(x=2.1, y=3.2, altitude=4.3)
        )
        expected_value = (1, 2.1, 3.2, 4.3)
        assert_that(
            actual_or_assertion=obj.tuple_view,
            matcher=equal_to(expected_value)
        )

    def test_from_pymodel(self):
        obj = Station(
            number=1, coordinate=Coordinate(x=2, y=3, altitude=4)
        )

        py_model = PyStation(
            number=obj.number,
            coordinate=PyCoordinate(
                x=obj.coordinate.x,
                y=obj.coordinate.y,
                altitude=obj.coordinate.altitude
            )
        )
        assert_that(
            actual_or_assertion=Station.from_pymodel(model=py_model),
            matcher=equal_to(obj)
        )


class TestObservationSystem:
    def test_base_altitude(self):
        stations = generate_stations()
        altitudes = [x.coordinate.altitude for x in stations]
        observation_system = ObservationSystem(
            stations=stations
        )
        assert_that(
            actual_or_assertion=observation_system.base_altitude,
            matcher=equal_to(min(altitudes))
        )

    def test_from_pymodel(self):
        stations = generate_stations()
        obj = ObservationSystem(stations=stations)

        py_stations = []
        for station in stations:
            py_stations.append(
                PyStation(
                    number=station.number,
                    coordinate=PyCoordinate(
                        x=station.coordinate.x,
                        y=station.coordinate.y,
                        altitude=station.coordinate.altitude
                    )
                )
            )

        py_model = PyObservationSystem(stations=py_stations)
        assert_that(
            actual_or_assertion=ObservationSystem.from_pymodel(
                model=py_model),
            matcher=equal_to(obj)
        )


class TestInterval:
    def test_from_pymodel(self):
        obj = Interval(min_val=-1, max_val=1)
        py_model = PyInterval(min_val=obj.min_val, max_val=obj.max_val)

        assert_that(
            actual_or_assertion=Interval.from_pymodel(model=py_model),
            matcher=equal_to(obj)
        )

    @pytest.mark.parametrize(
        argnames=['min_val', 'max_val'], argvalues=[(10, 0)])
    def test_invalid_input(self, min_val, max_val):
        try:
            Interval(min_val=min_val, max_val=max_val)
            is_success = False
        except ValueError:
            is_success = True
        assert_that(
            actual_or_assertion=is_success,
            matcher=is_(True)
        )

    def test_tuple_view(self):
        vals = randint(-100, 100), randint(-100, 100)
        min_val, max_val = min(vals), max(vals)
        interval = Interval(min_val=min_val, max_val=max_val)
        assert_that(
            actual_or_assertion=interval.tuple_view,
            matcher=equal_to((min_val, max_val))
        )

    def test_length(self):
        vals = randint(-100, 100), randint(-100, 100)
        min_val, max_val = min(vals), max(vals)
        interval = Interval(min_val=min_val, max_val=max_val)
        assert_that(
            actual_or_assertion=interval.length,
            matcher=equal_to(max_val - min_val)
        )

    def test_middle(self):
        vals = randint(-100, 100), randint(-100, 100)
        min_val, max_val = min(vals), max(vals)
        interval = Interval(min_val=min_val, max_val=max_val)
        assert_that(
            actual_or_assertion=interval.middle,
            matcher=equal_to((max_val + min_val) / 2)
        )


class TestLayer:
    def test_from_pymodel(self):
        obj = Layer(
            altitude_interval=Interval(min_val=-1, max_val=1),
            vp=10
        )

        py_model = PyLayer(
            altitude_interval=PyInterval(
                min_val=obj.altitude_interval.min_val,
                max_val=obj.altitude_interval.max_val
            ),
            vp=obj.vp
        )

        assert_that(
            actual_or_assertion=Layer.from_pymodel(model=py_model),
            matcher=equal_to(obj)
        )

    def test_thickness(self):
        interval = Interval(min_val=-100, max_val=120)
        obj = Layer(altitude_interval=interval, vp=1000)
        assert_that(
            actual_or_assertion=obj.thickness,
            matcher=equal_to(interval.max_val - interval.min_val)
        )

    def test_middle_altitude(self):
        interval = Interval(min_val=-100, max_val=120)
        obj = Layer(altitude_interval=interval, vp=1000)
        assert_that(
            actual_or_assertion=obj.middle_altitude,
            matcher=equal_to(interval.middle)
        )

    def test_travel_time(self):
        interval = Interval(min_val=-100, max_val=120)
        obj = Layer(altitude_interval=interval, vp=1000)
        assert_that(
            actual_or_assertion=obj.travel_time,
            matcher=equal_to(interval.length / obj.vp)
        )


class TestVelocityModel:
    def test_from_pymodel(self):
        layers = generate_layers()
        py_layers = []
        for layer in layers:
            py_interval = PyInterval(
                min_val=layer.altitude_interval.min_val,
                max_val=layer.altitude_interval.max_val
            )
            py_layers.append(
                PyLayer(
                    altitude_interval=py_interval,
                    vp=layer.vp
                )
            )
        py_model = PyVelocityModel(layers=py_layers)
        assert_that(
            actual_or_assertion=VelocityModel.from_pymodel(model=py_model),
            matcher=equal_to(VelocityModel(layers=layers))
        )

    def test_empty_layers_list(self):
        try:
            VelocityModel(layers=[])
            is_success = False
        except ValueError:
            is_success = True
        assert_that(
            actual_or_assertion=is_success,
            matcher=is_(True)
        )

    def test_layers(self):
        layers = [
            Layer(altitude_interval=Interval(min_val=-90, max_val=-80), vp=3),
            Layer(altitude_interval=Interval(min_val=-80, max_val=-70), vp=2),
            Layer(altitude_interval=Interval(min_val=-70, max_val=-60), vp=1)
        ]
        sorted_layers = [
            Layer(altitude_interval=Interval(min_val=-70, max_val=-60), vp=1),
            Layer(altitude_interval=Interval(min_val=-80, max_val=-70), vp=2),
            Layer(altitude_interval=Interval(min_val=-90, max_val=-80), vp=3)
        ]

        model = VelocityModel(layers=layers)
        for i, layer in enumerate(model.layers):
            assert_that(
                actual_or_assertion=layer.altitude_interval.max_val,
                matcher=equal_to(sorted_layers[i].altitude_interval.max_val)
            )

    def test_altitude_limits(self):
        layers = generate_layers()
        min_altitude = min((x.altitude_interval.min_val for x in layers))
        max_altitude = max((x.altitude_interval.max_val for x in layers))

        model = VelocityModel(layers=layers)

        assert_that(
            actual_or_assertion=model.min_altitude,
            matcher=equal_to(min_altitude)
        )
        assert_that(
            actual_or_assertion=model.max_altitude,
            matcher=equal_to(max_altitude)
        )

    def test_get_velocity_by_altitude(self):
        layers = generate_layers()
        model = VelocityModel(layers=layers)

        min_altitude = min((x.altitude_interval.min_val for x in layers))
        max_altitude = max((x.altitude_interval.max_val for x in layers))

        try:
            model.get_velocity_by_altitude(
                altitude=min_altitude - 1
            )
            is_success = False
        except ValueError:
            is_success = True

        assert_that(
            actual_or_assertion=is_success,
            matcher=is_(True)
        )

        velocity_value = model.get_velocity_by_altitude(altitude=min_altitude)
        most_bottom_layer = min(
            layers, key=lambda x: x.altitude_interval.min_val
        )
        assert_that(
            actual_or_assertion=velocity_value,
            matcher=equal_to(most_bottom_layer.vp)
        )

        try:
            model.get_velocity_by_altitude(
                altitude=max_altitude + 1
            )
            is_success = False
        except ValueError:
            is_success = True

        assert_that(
            actual_or_assertion=is_success,
            matcher=is_(True)
        )

        for i in range(1, len(layers) - 1):
            layer = model.layers[i]
            min_altitude, max_altitude = layer.altitude_interval.tuple_view
            avg_altitude = (min_altitude + max_altitude) / 2

            velocity_value = model.get_velocity_by_altitude(
                altitude=max_altitude
            )
            assert_that(
                actual_or_assertion=velocity_value,
                matcher=equal_to(layer.vp)
            )

            velocity_value = model.get_velocity_by_altitude(
                altitude=avg_altitude
            )
            assert_that(
                actual_or_assertion=velocity_value,
                matcher=equal_to(layer.vp)
            )

            velocity_value = model.get_velocity_by_altitude(
                altitude=min_altitude
            )
            assert_that(
                actual_or_assertion=velocity_value,
                matcher=equal_to(model.layers[i + 1].vp)
            )

    def test_get_interval_velocity_bad_intervals(self):
        layers = generate_layers()
        model = VelocityModel(layers=layers)

        min_altitude = min((x.altitude_interval.min_val for x in layers))
        max_altitude = max((x.altitude_interval.max_val for x in layers))

        interval = Interval(min_val=min_altitude - 1, max_val=max_altitude)
        try:
            model.get_interval_velocity(altitude_interval=interval)
            is_success = False
        except ValueError:
            is_success = True
        assert_that(actual_or_assertion=is_success, matcher=is_(True))

        interval = Interval(min_val=min_altitude, max_val=max_altitude + 1)
        try:
            model.get_interval_velocity(altitude_interval=interval)
            is_success = False
        except ValueError:
            is_success = True
        assert_that(actual_or_assertion=is_success, matcher=is_(True))

    def test_get_interval_velocity_zero_intervals(self):
        layers = generate_layers()
        model = VelocityModel(layers=layers)

        for layer in model.layers:
            altitudes = [
                layer.altitude_interval.max_val,
                layer.altitude_interval.middle
            ]
            for altitude in altitudes:
                interval = Interval(min_val=altitude, max_val=altitude)
                velocity_value = model.get_interval_velocity(
                    altitude_interval=interval
                )
                expected_velocity_value = layer.vp
                assert_that(
                    actual_or_assertion=velocity_value,
                    matcher=equal_to(expected_velocity_value)
                )

        most_bottom_layer = min(
            layers, key=lambda x: x.altitude_interval.min_val
        )
        min_altitude = min((x.altitude_interval.min_val for x in layers))
        interval = Interval(min_val=min_altitude, max_val=min_altitude)
        velocity_value = model.get_interval_velocity(
            altitude_interval=interval
        )
        assert_that(
            actual_or_assertion=velocity_value,
            matcher=equal_to(most_bottom_layer.vp)
        )

    def test_get_interval_velocity_between_middle(self):
        layers = generate_layers()
        model = VelocityModel(layers=layers)

        for i in range(len(layers) - 1):
            top_layer, bottom_layer = model.layers[i], model.layers[i + 1]
            top_altitude = top_layer.middle_altitude
            bottom_altitude = bottom_layer.middle_altitude

            interval = Interval(min_val=bottom_altitude, max_val=top_altitude)
            velocity_value = model.get_interval_velocity(
                altitude_interval=interval
            )

            dh_top = top_altitude - top_layer.altitude_interval.min_val
            dh_bottom = (
                bottom_layer.altitude_interval.max_val - bottom_altitude
            )
            total_time = dh_top / top_layer.vp + dh_bottom / bottom_layer.vp
            expected_velocity_value = (dh_top + dh_bottom) / total_time

            assert_that(
                actual_or_assertion=velocity_value,
                matcher=equal_to(expected_velocity_value)
            )

    def test_get_interval_velocity_between_top_middle(self):
        layers = generate_layers()
        model = VelocityModel(layers=layers)

        for i in range(len(layers) - 1):
            top_layer, bottom_layer = model.layers[i], model.layers[i + 1]
            top_altitude = top_layer.altitude_interval.max_val
            bottom_altitude = bottom_layer.middle_altitude

            interval = Interval(min_val=bottom_altitude, max_val=top_altitude)
            velocity_value = model.get_interval_velocity(
                altitude_interval=interval
            )

            dh_bottom = (
                bottom_layer.altitude_interval.max_val - bottom_altitude
            )
            total_time = top_layer.travel_time + dh_bottom / bottom_layer.vp
            dh_full = top_layer.thickness + dh_bottom
            expected_velocity_value = dh_full / total_time

            assert_that(
                actual_or_assertion=velocity_value,
                matcher=equal_to(expected_velocity_value)
            )

    def test_get_interval_velocity_between_middle_bottom(self):
        layers = generate_layers()
        model = VelocityModel(layers=layers)

        for i in range(len(layers) - 1):
            top_layer, bottom_layer = model.layers[i], model.layers[i + 1]
            top_altitude = top_layer.middle_altitude
            bottom_altitude = bottom_layer.altitude_interval.min_val

            interval = Interval(min_val=bottom_altitude, max_val=top_altitude)
            velocity_value = model.get_interval_velocity(
                altitude_interval=interval
            )

            dh_top = top_altitude - top_layer.altitude_interval.min_val
            total_time = dh_top / top_layer.vp + bottom_layer.travel_time
            dh_full = dh_top + bottom_layer.thickness
            expected_velocity_value = dh_full / total_time

            assert_that(
                actual_or_assertion=velocity_value,
                matcher=equal_to(expected_velocity_value)
            )

    def test_get_interval_velocity_between_top_bottom(self):
        layers = generate_layers()
        model = VelocityModel(layers=layers)

        for i in range(len(layers) - 1):
            top_layer, bottom_layer = model.layers[i], model.layers[i + 1]
            top_altitude = top_layer.altitude_interval.max_val
            bottom_altitude = bottom_layer.altitude_interval.min_val

            interval = Interval(min_val=bottom_altitude, max_val=top_altitude)
            velocity_value = model.get_interval_velocity(
                altitude_interval=interval
            )

            total_time = top_layer.travel_time + bottom_layer.travel_time
            dh_full = top_layer.thickness + bottom_layer.thickness
            expected_velocity_value = dh_full / total_time

            assert_that(
                actual_or_assertion=velocity_value,
                matcher=equal_to(expected_velocity_value)
            )
