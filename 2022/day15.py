import json
import re
from functools import reduce, cmp_to_key
from typing import List, Iterator, Callable, Tuple, Set

import numpy as np
from dataclasses import dataclass
from scipy.sparse import csr_matrix

_INPUT = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

_LINE_PATTERN = r"Sensor at x=(?P<pos_x>-?\d+), y=(?P<pos_y>-?\d+): closest beacon is at x=(?P<beacon_x>-?\d+), y=(?P<beacon_y>-?\d+)"


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return hash(f"({self.x}, {self.y})")


class Sensor:
    def __init__(self, position: Point, closest_beacon: Point):
        self.position = position
        self.closest_beacon = closest_beacon
        self._manhattan_distance = abs(self.position.x - self.closest_beacon.x) + abs(self.position.y - self.closest_beacon.y)

    def get_manhattan_distance(self) -> int:
        return self._manhattan_distance

    def get_min_y(self) -> int:
        return self.position.y - self._manhattan_distance

    def get_max_y(self) -> int:
        return self.position.y + self._manhattan_distance

    def get_monitored_xs(self, desired_y: int) -> Set[int]:
        result = set()
        start_x = self.position.x
        y_distance = abs(desired_y - self.position.y)
        left_distance = self._manhattan_distance - y_distance
        for i in range(left_distance+1):
            result.add(start_x+i)
            result.add(start_x-i)
        return result

    def get_item_xs_in_row(self, desired_y: int) -> Set[int]:
        result = set()
        if self.position.y == desired_y:
            result.add(self.position.x)
        if self.closest_beacon.y == desired_y:
            result.add(self.closest_beacon.x)
        return result

    def __str__(self):
        return f"Sensor at {str(self.position)}: closest beacon is at {str(self.closest_beacon)} --> {self._manhattan_distance}"

    def __hash__(self):
        return hash(f"{self.position} - {self.closest_beacon}")


class SensorMap:
    def __init__(self, max_coord: int):
        self._max_coord = max_coord + 1
        self._intervals = [[] for _ in range(self._max_coord)]

    def add_sensor_info(self, sensor: Sensor):
        start_x = sensor.position.x
        start_y = sensor.position.y
        distance = sensor.get_manhattan_distance()
        for y_coord in range(max(start_y-distance, 0), min(start_y+distance+1, self._max_coord)):
            actual_width = distance - abs(start_y - y_coord)
            self._intervals[y_coord].append((max(start_x-actual_width, 0), min(start_x+actual_width, self._max_coord)))

    def get_solution(self) -> int:
        for i in range(len(self._intervals)):
            res = self._get_res(self._intervals[i])
            if res is not None:
                return res * 4000000 + i
        return -1

    def _get_res(self, intervals: List):
        sorted_intervals = sorted(intervals, key=lambda x: x[0])
        simplified_interval = [sorted_intervals[0][0], sorted_intervals[0][1]]
        if simplified_interval[0] != 0:
            return 0
        for inter in sorted_intervals[1:]:
            if inter[0] <= simplified_interval[1] <= inter[1]:
                simplified_interval[1] = inter[1]
            if simplified_interval[0] == 0 and simplified_interval[1] == self._max_coord:
                return None
        return simplified_interval[1] + 1


def _read_sensors(lines: List[str]) -> List[Sensor]:
    result = []
    for line in lines:
        match = re.search(_LINE_PATTERN, line)
        position = Point(x=int(match.group("pos_x")), y=int(match.group("pos_y")))
        closest_beacon = Point(x=int(match.group("beacon_x")), y=int(match.group("beacon_y")))
        sensor = Sensor(position=position, closest_beacon=closest_beacon)
        result.append(sensor)
    return result


def _simple_task(sensors: List[Sensor], desired_y: int=10):
    excluded_xs = set()
    items_in_row = set()
    for sensor in sensors:
        if sensor.get_min_y() <= desired_y <= sensor.get_max_y():
            monitored_xs_by_sensor = sensor.get_monitored_xs(desired_y)
            excluded_xs = excluded_xs.union(monitored_xs_by_sensor)
            items_from_sensor = sensor.get_item_xs_in_row(desired_y)
            items_in_row = items_in_row.union(items_from_sensor)
    excluded_xs = excluded_xs.difference(items_in_row)
    print(len(excluded_xs))


def _advanced_task(sensors: List[Sensor], max_coord: int):
    sensor_map = SensorMap(max_coord)
    for i, sensor in enumerate(sensors):
        print(i+1, sensor)
        sensor_map.add_sensor_info(sensor)
    solutions = sensor_map.get_solution()
    print(solutions)


if __name__ == '__main__':
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    #lines = _INPUT.split("\n")
    #sensors = _read_sensors(lines)
    #_simple_task(sensors, desired_y=10)
    #_advanced_task(sensors, max_coord=20)

    sensors = _read_sensors(lines)
    _simple_task(sensors, desired_y=2_000_000)
    _advanced_task(sensors, max_coord=4_000_000)
