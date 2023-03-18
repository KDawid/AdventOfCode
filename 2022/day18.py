import json
import operator
import re
import time
from functools import reduce, cmp_to_key
from itertools import product, permutations
from typing import List, Iterator, Callable, Tuple, Set, Dict

import numpy as np
import pandas as pd
from dataclasses import dataclass


_INPUT_SMALL = """1,1,1
2,1,1"""


_INPUT = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""


@dataclass
class Cube:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def is_neighbour(self, cube):
        if self.x == cube.x and self.y == cube.y and self.z == cube.z:
            raise ValueError(f"Cubes are the same: {cube}")
        if self.x == cube.x and self.y == cube.y:
            return abs(self.z - cube.z) == 1
        if self.x == cube.x and self.z == cube.z:
            return abs(self.y - cube.y) == 1
        if self.y == cube.y and self.z == cube.z:
            return abs(self.x - cube.x) == 1

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __hash__(self):
        return hash(f"{self.x}-{self.y}-{self.z}")


class Grid:
    def __init__(self):
        self._cubes: Set[Cube] = set()
        self._waters: Set[Cube] = set()
        self._free_sides = 0
        self._max_x, self._max_y, self._max_z = -1, -1, -1

    def add_cube(self, new_cube: Cube):
        self._free_sides += 6
        for cube in self._cubes:
            if cube.is_neighbour(new_cube):
                self._free_sides -= 2
        self._cubes.add(new_cube)
        self._update_maxes(new_cube)

    def get_free_sides_num(self) -> int:
        return self._free_sides

    def _update_maxes(self, new_cube: Cube):
        if self._max_x < new_cube.x:
            self._max_x = new_cube.x
        if self._max_y < new_cube.y:
            self._max_y = new_cube.y
        if self._max_z < new_cube.z:
            self._max_z = new_cube.z

    def add_water(self):
        self._waters = set()
        initial_waters_num = len(self._waters)
        self._waters.add(Cube(self._max_x+1, self._max_y+1, self._max_z+1))
        new_waters_num = len(self._waters)
        while initial_waters_num < new_waters_num:
            initial_waters_num = new_waters_num
            self._flow_water([water for water in self._waters])
            new_waters_num = len(self._waters)

    def _flow_water(self, waters: List[Cube]):
        for water in waters:
            x, y, z = water.x, water.y, water.z
            if x + 1 <= self._max_x+1:
                cube = Cube(x+1, y, z)
                if cube not in self._cubes and cube not in self._waters:
                    self._waters.add(cube)
            if 0 <= x:
                cube = Cube(x-1, y, z)
                if cube not in self._cubes and cube not in self._waters:
                    self._waters.add(cube)
            ###############################
            if y + 1 <= self._max_y+1:
                cube = Cube(x, y+1, z)
                if cube not in self._cubes and cube not in self._waters:
                    self._waters.add(cube)
            if 0 <= y:
                cube = Cube(x, y-1, z)
                if cube not in self._cubes and cube not in self._waters:
                    self._waters.add(cube)
            ###############################
            if z + 1 <= self._max_z+1:
                cube = Cube(x, y, z+1)
                if cube not in self._cubes and cube not in self._waters:
                    self._waters.add(cube)
            if 0 <= z:
                cube = Cube(x, y, z-1)
                if cube not in self._cubes and cube not in self._waters:
                    self._waters.add(cube)

    def get_watered_sides_num(self):
        result = 0
        for cube in self._cubes:
            x, y, z = cube.x, cube.y, cube.z
            for i in (x-1, x+1):
                new_cube = Cube(i, y, z)
                if new_cube in self._waters:
                    result += 1
            ###############################
            for i in (y-1, y+1):
                new_cube = Cube(x, i, z)
                if new_cube in self._waters:
                    result += 1
            ###############################
            for i in (z-1, z+1):
                new_cube = Cube(x, y, i)
                if new_cube in self._waters:
                    result += 1
        return result

    def print_grid(self):
        for z in range(self._max_z + 2):
            print(f"z={z}")
            lines = []
            for x in range(self._max_x + 2):
                line = []
                for y in range(self._max_y + 2):
                    cube = Cube(x, y, z)
                    if cube in self._cubes:
                        line.append("#")
                    elif cube in self._waters:
                        line.append("~")
                    else:
                        line.append(" ")
                lines.append("".join(line))
            print("\n".join(lines))
            print()


def _simple_task(lines: List[str]):
    grid = Grid()
    for line in lines:
        x, y, z = [int(coord) for coord in line.split(",")]
        cube = Cube(x, y, z)
        grid.add_cube(cube)
    print(grid.get_free_sides_num())


def _advanced_task(lines: List[str]):
    grid = Grid()
    for line in lines:
        x, y, z = [int(coord) for coord in line.split(",")]
        cube = Cube(x, y, z)
        grid.add_cube(cube)
    grid.add_water()
    grid.print_grid()
    print(grid.get_watered_sides_num())
    #grid.print_grid()


if __name__ == '__main__':
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    #lines = _INPUT.split("\n")
    #lines = _INPUT_SMALL.split("\n")
    _simple_task(lines)
    _advanced_task(lines)
