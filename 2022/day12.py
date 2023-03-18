from functools import reduce
from typing import List, Iterator, Callable, Tuple

import numpy as np
from dataclasses import dataclass

_INPUT = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


class HeightMap(object):
    _ORDER = "SabcdefghijklmnopqrstuvwxyzE"

    def __init__(self, lines: List[str]):
        self._heightmap = np.ndarray((len(lines), len(lines[0])), dtype=int)
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                self._heightmap[i, j] = self._ORDER.index(lines[i][j])
                if lines[i][j] == "S":
                    self._start = (i, j)
                elif lines[i][j] == "E":
                    self._end = (i, j)

    def get_map(self):
        return self._heightmap

    def set_start(self, i, j):
        self._start = (i, j)

    def shortest_path_length(self):
        minimum_distance_map = np.full((len(self._heightmap), len(self._heightmap[0])), self._heightmap.size*100)
        minimum_distance_map[self._start[0], self._start[1]] = 0
        nodes_to_update = [self._start]
        while len(nodes_to_update) > 0:
            nodes_to_update = self._find_path(minimum_distance_map, nodes_to_update)
        # print(minimum_distance_map)
        return minimum_distance_map[self._end[0], self._end[1]]

    def _find_path(self, minimum_distance_map: np.ndarray, nodes_to_update: List) -> List:
        coord, nodes_left = nodes_to_update[0], nodes_to_update[1:]
        current_symbol = self._heightmap[coord[0], coord[1]]
        for i, j in [(i, j) for i, j in ((coord[0]-1,  coord[1]), (coord[0]+1, coord[1]), (coord[0], coord[1]-1), (coord[0], coord[1]+1)) if 0 <= i < len(self._heightmap) and 0 <= j < len(self._heightmap[i])]:
            if self._heightmap[i, j] <= current_symbol + 1:
                if minimum_distance_map[coord[0], coord[1]] + 1 < minimum_distance_map[i, j]:
                    minimum_distance_map[i, j] = minimum_distance_map[coord[0], coord[1]] + 1
                    nodes_left.append((i, j))
        return nodes_left

    def __str__(self):
        return f"{str(self._heightmap)}, {str(self._start)}, {str(self._end)}"


def _simple_task(heightmap: HeightMap):
    print(heightmap)
    print(heightmap.shortest_path_length())


def _advanced_task(lines: List[str]):
    heightmap = HeightMap(lines)
    print(heightmap)
    possible_start_points = []
    for i in range(len(heightmap.get_map())):
        for j in range(len(heightmap.get_map()[i])):
            if heightmap.get_map()[i, j] == 0:
                possible_start_points.append((i, j))
            elif heightmap.get_map()[i, j] == 1:
                possible_start_points.append((i, j))
    minimal_path = heightmap.get_map().size * 100
    for x, y in possible_start_points:
        heightmap.set_start(x, y)
        res = heightmap.shortest_path_length()
        if res < minimal_path:
            minimal_path = res
            print(minimal_path)
    #print(heightmap.shortest_path_length())


if __name__ == '__main__':
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    #lines = _INPUT.split("\n")
    heightmap = HeightMap(lines)
    _simple_task(heightmap)
    _advanced_task(lines)

