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

_INPUT = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"


class SHAPES:
    HORIZONTAL = ["@@@@"]
    CROSS = [".@.", "@@@", ".@."]
    CORNER = ["..@", "..@", "@@@"]
    VERTICAL = ["@", "@", "@", "@"]
    SQUARE = ["@@", "@@"]


class RockGenerator:
    _ROCKS = [SHAPES.HORIZONTAL, SHAPES.CROSS, SHAPES.CORNER, SHAPES.VERTICAL, SHAPES.SQUARE]

    def __init__(self):
        self._index = 0
        self._shapes_len = len(RockGenerator._ROCKS)

    def get_rock(self):
        rock = self._ROCKS[self._index]
        self._index = (self._index + 1) % self._shapes_len
        return rock

    def index(self):
        return self._index


class WindGenerator:
    def __init__(self, directions: str):
        self._direcitons = directions
        self._dir_len = len(self._direcitons)
        self._index = 0

    def get_wind(self):
        wind = self._direcitons[self._index]
        self._index = (self._index + 1) % self._dir_len
        return wind

    def index(self):
        return self._index


class Chamber:
    _WIDTH = 7
    _EMPTY_LINE = "." * _WIDTH

    def __init__(self, directions: str):
        self._wind_generator = WindGenerator(directions)
        self._rock_generator = RockGenerator()
        self._chamber = []
        self._rock_nums = 0
        self._stats = dict()

    def add_rock(self):
        self._rock_nums += 1
        self._stats[self._rock_nums] = {"wind_index": self._wind_generator.index(), "rock": self._rock_generator.index()}
        self._add_empty_lines()
        rock = self._rock_generator.get_rock()
        self._add_rock_to_chamber(rock)
        f, t = self._move_to_the_bottom(len(self._chamber)-len(rock), len(self._chamber))
        self._freeze(f, t)
        self._stats[self._rock_nums]["height"] = self.get_chamber_size()

    def get_line(self, i):
        return self._chamber[i]

    def get_chamber_size(self):
        return len(self._chamber)

    def get_stats(self):
        return self._stats

    def rock_index(self):
        return self._rock_generator.index()

    def wind_index(self):
        return self._wind_generator.index()

    def _add_empty_lines(self):
        if len(self._chamber) < 1 or self._chamber[-1] != self._EMPTY_LINE:
            self._chamber += [self._EMPTY_LINE] * 3
        if len(self._chamber) < 2 or self._chamber[-2] != self._EMPTY_LINE:
            self._chamber += [self._EMPTY_LINE] * 2
        if len(self._chamber) < 3 or self._chamber[-3] != self._EMPTY_LINE:
            self._chamber += [self._EMPTY_LINE] * 1

    def _add_rock_to_chamber(self, rock: List[str]):
        rock_lines = [".." + rock_line + "." * (self._WIDTH-len(rock_line)-2) for rock_line in rock]
        self._chamber += reversed(rock_lines)

    def _move_to_the_bottom(self, f: int, t: int) -> (int, int):
        while True:
            self._blow_wind(f, t)
            if not self._can_drop(f, t):
                return f, t
            f, t = self._drop_one(f, t)

    def _blow_wind(self, f: int, t: int):
        wind = self._wind_generator.get_wind()
        if wind == ">":
            self._move_right(f, t)
        elif wind == "<":
            self._move_left(f, t)
        else:
            raise ValueError("No wind to that")

    def _move_right(self, f: int, t: int):
        if all([not line.endswith('@') and "@#" not in line for line in self._chamber[f:t]]):
            for i in range(f, t):
                new_line = [char for char in self._chamber[i]]
                for j in reversed(range(len(new_line)-1)):
                    if new_line[j] == "@":
                        new_line[j] = "."
                        new_line[j+1] = "@"
                self._chamber[i] = "".join(new_line)

    def _move_left(self, f: int, t: int):
        if all([not line.startswith('@') and "#@" not in line for line in self._chamber[f:t]]):
            for i in range(f, t):
                new_line = [char for char in self._chamber[i]]
                for j in range(1, len(new_line)):
                    if new_line[j] == "@":
                        new_line[j] = "."
                        new_line[j-1] = "@"
                self._chamber[i] = "".join(new_line)

    def _can_drop(self, f: int, t: int):
        if 0 < f:
            if self._chamber[f-1] == self._EMPTY_LINE:
                return True
            for i in range(f, t):
                for j in range(self._WIDTH):
                    if self._chamber[i][j] == "@" and self._chamber[i-1][j] == "#":
                        return False
            return True
        return False

    def _drop_one(self, f: int, t: int) -> (int, int):
        for i in range(f, t):
            for j in range(self._WIDTH):
                if self._chamber[i][j] == "@":
                    line = [c for c in self._chamber[i-1]]
                    line[j] = "@"
                    self._chamber[i-1] = "".join(line)

                    line = [c for c in self._chamber[i]]
                    line[j] = "."
                    self._chamber[i] = "".join(line)
        return f-1, t-1

    def _freeze(self, f: int, t: int):
        for i in range(f, t):
            self._chamber[i] = self._chamber[i].replace("@", "#")
        while self._chamber[-1] == self._EMPTY_LINE:
            self._chamber.pop(-1)

    def __str__(self):
        return "\n".join(["|" + line + "|" for line in reversed(self._chamber)] + ["+" + "-" * self._WIDTH + "+"])


def _simple_task(directions: str, rocks):
    chamber = Chamber(directions)
    for i in range(rocks):
        chamber.add_rock()
    print(chamber.get_chamber_size())


def _calculate_height_after(directions, prefix):
    chamber = Chamber(directions)
    for _ in range(prefix):
        chamber.add_rock()
    return chamber.get_chamber_size()


def _calculate_circle_height(directions, prefix, circle_length):
    chamber = Chamber(directions)
    for _ in range(prefix):
        chamber.add_rock()
    start_length = chamber.get_chamber_size()
    for _ in range(circle_length):
        chamber.add_rock()
    end_length = chamber.get_chamber_size()
    for _ in range(circle_length):
        chamber.add_rock()
    s = chamber.get_stats()
    #print(json.dumps(s, indent=4))
    return end_length - start_length, {key: value for key, value in s.items() if prefix <= key}


def _advanced_task(directions: str, rocks):
    prefix = 50_000
    prefix_height = _calculate_height_after(directions, prefix)
    print(f"Prefix height = {prefix_height}")
    circle_length = _guess_circle(directions, after=prefix)
    print(f"Circle length = {circle_length}")

    circle_height, stats = _calculate_circle_height(directions, prefix, circle_length)
    print(f"Circle height = {circle_height}")
    # print(json.dumps(stats, indent=4))

    circle_number = (rocks - prefix) // circle_length

    print(f"Circle number = {circle_number}")
    middle_height = circle_number * circle_height
    print(f"Middle height = {middle_height}")

    steps_applied = circle_number * circle_length + prefix
    left_num = rocks - steps_applied

    left_start_index = prefix + (steps_applied % circle_length)
    left_start_height = stats[left_start_index]["height"]
    left_end_height = stats[left_start_index + left_num]["height"]
    end_height = left_end_height - left_start_height
    print(f"End height = {end_height}")
    #left_num = rocks - steps_applied
    #print("LEFT", left_num)


    print(prefix_height + middle_height + end_height)
    print(1_514_285_714_288)
    print(1_514_285_714_288 - (prefix_height + middle_height + end_height))


def _guess_circle(directions, after):
    chamber = Chamber(directions)
    for _ in range(after):
        chamber.add_rock()
    for i in range(1, after):
        # if all([chamber.get_line(j) == chamber.get_line(i+j) for j in range(500, after)]):
        if all([chamber.get_stats()[j]["wind_index"] == chamber.get_stats()[i+j]["wind_index"] and chamber.get_stats()[j]["rock"] == chamber.get_stats()[i+j]["rock"] for j in range(5000, after-i)]):
            print(f"Suspicious repeat: {i}")
            return i
    raise ValueError("No circle")
    #return 35
    #return 1725


if __name__ == '__main__':
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    #lines = _INPUT.split("\n")
    _simple_task(lines[0], rocks=2022)
    _advanced_task(lines[0], rocks=1_000_000_000_000)
    # 1541449275364 --> LOW
    # 1541449275365 --> YES!!!
    # 1541449275366 --> X
    # 1541449275367 --> HIGH
    # 1541449275368 --> HIGH
    # 1541449275369 --> HIGH