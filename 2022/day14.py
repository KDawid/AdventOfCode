import json
from functools import reduce, cmp_to_key
from typing import List, Iterator, Callable, Tuple

import numpy as np
from dataclasses import dataclass

_INPUT = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return hash(f"({self.x}, {self.y})")


class Structure:
    _ENTRY = "+"
    _ROCK = "#"
    _EMPTY = "."
    _SAND = "o"

    def __init__(self):
        self._rock_coordinates = set()
        self._sand_num = 0

        self._map = None
        self._min_x = None

        self._full = False

    def add_rock_coordinate(self, point: Point):
        self._rock_coordinates.add(point)

    def get_deepest_line_num(self) -> int:
        return max([p.y for p in self._rock_coordinates] + [0])

    def init_map(self):
        self._min_x, max_x = min([p.x for p in self._rock_coordinates]), max([p.x for p in self._rock_coordinates])
        min_y, max_y = min([p.y for p in self._rock_coordinates] + [0]), max([p.y for p in self._rock_coordinates])
        self._map = np.full((max_y - min_y + 1, max_x - self._min_x + 1), self._EMPTY, dtype=object)
        for rock_point in self._rock_coordinates:
            self._map[rock_point.y - min_y, rock_point.x - self._min_x] = self._ROCK
        self._map[0, 500 - self._min_x] = self._ENTRY

    def add_sand(self):
        try:
            self._add_sand()
        except:
            self._full = True

    def get_sand_num(self) -> int:
        return self._sand_num

    def is_full(self) -> bool:
        return self._full

    def _add_sand(self):
        can_move = True
        x, y = 0, 500 - self._min_x
        while can_move:
            if self._map[x + 1, y] == self._EMPTY:
                x += 1
            elif self._map[x + 1, y - 1] == self._EMPTY:
                x += 1
                y -= 1
            elif self._map[x + 1, y + 1] == self._EMPTY:
                x += 1
                y += 1
            else:
                can_move = False
        self._map[x, y] = self._SAND
        self._sand_num += 1
        if x == 0 and y == 500-self._min_x:
            self._full = True

    def __str__(self):
        return str('\n'.join([''.join(line) for line in self._map]))


def _add_coordinates_from_lines(structure: Structure, lines: List[str]) -> Structure:
    for line in lines:
        print(line)
        edges = line.split(" -> ")
        current_edge_strs = edges[0].split(",")
        current_edge = Point(x=int(current_edge_strs[0]), y=int(current_edge_strs[1]))
        structure.add_rock_coordinate(current_edge)
        for next_edge_data in edges[1:]:
            next_edge_strs = next_edge_data.split(",")
            next_edge = Point(x=int(next_edge_strs[0]), y=int(next_edge_strs[1]))
            if current_edge.x == next_edge.x:
                _from = min(current_edge.y, next_edge.y)
                _to = max(current_edge.y, next_edge.y)
                for i in range(_from, _to+1):
                    structure.add_rock_coordinate(Point(x=next_edge.x, y=i))
            if current_edge.y == next_edge.y:
                _from = min(current_edge.x, next_edge.x)
                _to = max(current_edge.x, next_edge.x)
                for i in range(_from, _to + 1):
                    structure.add_rock_coordinate(Point(x=i, y=next_edge.y))
            current_edge = next_edge
    return structure


def _build_structure(lines: List[str]) -> Structure:
    structure = Structure()
    structure = _add_coordinates_from_lines(structure, lines)
    structure.init_map()
    return structure


def _build_advanced_structure(lines: List[str]) -> Structure:
    structure = Structure()
    structure = _add_coordinates_from_lines(structure, lines)
    max_x = structure.get_deepest_line_num() + 2
    print(max_x)
    for i in range(500-max_x+1, 500+max_x+1):
        structure.add_rock_coordinate(Point(x=i, y=max_x))
    structure.init_map()
    return structure


def _simple_task(lines: List[str]):
    structure = _build_structure(lines)
    print(structure)
    while not structure.is_full():
        structure.add_sand()
    print(structure)
    print(structure.get_sand_num())


def _advanced_task(lines: List[str]):
    structure = _build_advanced_structure(lines)
    print(structure)
    print()
    while not structure.is_full():
        structure.add_sand()
    print(structure)
    print(structure.get_sand_num())


if __name__ == '__main__':
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    #lines = _INPUT.split("\n")
    _simple_task(lines)
    _advanced_task(lines)
