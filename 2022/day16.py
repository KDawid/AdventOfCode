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
from scipy.sparse import csr_matrix

_INPUT = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

_LINE_PATTERN = r"Valve (?P<name>[A-Z]+) has flow rate=(?P<flow_rate>\d+); tunnels? leads? to valves? (?P<tunnels>[A-Z, ]+)"
_START_POINT = "AA"


class Valve:
    def __init__(self, name: str, flow_rate: int, tunnels: Set[str]):
        self.name = name
        self.flow_rate = flow_rate
        self.tunnels = tunnels
        self.released = False

    def __str__(self):
        return f"{self.name} with flow rate {self.flow_rate} leads to {sorted(self.tunnels)}"


class Graph:
    def __init__(self, lines: List[str]):
        self._valves = Graph._read_lines(lines)
        self._distance_map = self._create_distance_map(self._valves)

    def get(self, valve_name) -> Valve:
        return self._valves[valve_name]

    def get_valve_names(self) -> List[str]:
        return sorted(self._valves.keys())

    def get_distance_map(self):
        return self._distance_map

    def get_distances_from(self, start_point: str) -> Dict[str, int]:
        return self._distance_map[start_point]

    def release_valve(self, name: str):
        if self._valves[name].released:
            raise ValueError("Could not open twice")
        self._valves[name].released = True

    def get_relevant_valves(self) -> List[str]:
        return [valve.name for valve in self._valves.values() if 0 < valve.flow_rate and not valve.released]

    @staticmethod
    def _read_lines(lines: List[str]) -> Dict[str, Valve]:
        result = dict()
        for line in lines:
            match = re.search(_LINE_PATTERN, line)
            valve_name = match.group("name")
            flow_rate = int(match.group("flow_rate"))
            tunnels = {tunnel.strip() for tunnel in match.group("tunnels").split(",")}
            result[valve_name] = Valve(valve_name, flow_rate, tunnels)
        return result

    def _create_distance_map(self, valves: Dict[str, Valve]) -> Dict[str, Dict[str, int]]:
        result = {valve_name: {to_name: None for to_name in self.get_valve_names() if to_name != valve_name} for valve_name in valves.keys()}
        for valve in valves.values():
            for tunnel_to in valve.tunnels:
                result[valve.name][tunnel_to] = 1
        while any([any([x is None for x in r.values()]) for r in result.values()]):
            for from_valve in result:
                for to_valve in result[from_valve]:
                    if result[from_valve][to_valve] is None:
                        result[from_valve][to_valve] = self._try_to_fill(result, from_valve, to_valve)
        relevant_valves = self.get_relevant_valves()
        return {n: {valve: distance+1 for valve, distance in r.items() if valve in relevant_valves + [_START_POINT]} for n, r in result.items() if n in relevant_valves + [_START_POINT]}

    def _try_to_fill(self, result, from_valve, to_valve):
        min_path = 9999999
        for link_valve in self.get_valve_names():
            if link_valve in result[from_valve] and to_valve in self._valves[link_valve].tunnels:
                value = result[from_valve][link_valve]
                if value is not None and value + 1 < min_path:
                    min_path = value + 1
        return min_path if min_path < 9999999 else None


def _simple_task(graph: Graph, minutes: int):
    valid_paths = _generate_all_valid_paths(graph, minutes)
    distance_map = graph.get_distance_map()
    new_map = {graph.get(valve).name: graph.get(valve).flow_rate for valve in distance_map}

    calculated_pressures = dict()
    max_released_pressure = 0
    for path in valid_paths:
        released_pressure = _calculate_released_pressure(calculated_pressures, path, distance_map, new_map, minutes)
        if max_released_pressure < released_pressure:
            max_released_pressure = released_pressure
    print("-----------------------------")
    print(max_released_pressure)
    print("-----------------------------")


def _permutation(distance_map, lst, node, minutes_left):
    if len(lst) == 0:
        return []
    if len(lst) == 1 or minutes_left <= 0:
        return [lst]

    l = []
    for i in range(len(lst)):
        m = lst[i]
        new_minutes = minutes_left - distance_map[node][m]

        rem_lst = lst[:i] + lst[i + 1:]

        for p in _permutation(distance_map, rem_lst, m, new_minutes):
            l.append([m] + p)
    return l


def _calculate_released_pressure(calculated_pressures, path, distance_map, pressures, minutes):
    if path in calculated_pressures:
        return calculated_pressures[path]
    released_pressure = 0
    act_minutes = minutes
    current_node = _START_POINT
    for next_node in path:
        new_minutes = act_minutes - distance_map[current_node][next_node]
        if new_minutes > 0:
            released_pressure += new_minutes * pressures[next_node]
        current_node = next_node
        act_minutes = new_minutes
    calculated_pressures[path] = released_pressure
    return released_pressure


def _advanced_task(graph: Graph, minutes: int):
    valid_path_set = _generate_all_valid_paths(graph, minutes)
    all_path_and_subpaths_set = _create_all_path_and_subpaths_set(valid_path_set)

    distance_map = graph.get_distance_map()
    relevant_valves = sorted(distance_map.keys())
    flow_rates = {graph.get(valve).name: graph.get(valve).flow_rate for valve in distance_map}
    reached_nodes_map = _create_reached_nodes_map(all_path_and_subpaths_set, relevant_valves)

    calculated_pressures = dict()
    max_released_pressure = 0
    for i, path in enumerate(all_path_and_subpaths_set):
        released_pressure = _calculate_released_pressure(calculated_pressures, path, distance_map, flow_rates, minutes)
        max_elephant_pressure = 0
        for elephant_path in _get_elephant_paths(path, all_path_and_subpaths_set, reached_nodes_map):
            elephant_pressure = _calculate_released_pressure(calculated_pressures, elephant_path, distance_map, flow_rates, minutes)
            if max_elephant_pressure < elephant_pressure:
                max_elephant_pressure = elephant_pressure
        common_pressure = released_pressure + max_elephant_pressure
        if max_released_pressure < common_pressure:
            max_released_pressure = common_pressure
        if (i+1) % 1000 == 0:
            print(i+1)
    print("-----------------------------")
    print(max_released_pressure)
    print("-----------------------------")


def _generate_all_valid_paths(graph: Graph, minutes: int) -> Set[Tuple[str]]:
    distance_map = graph.get_distance_map()
    df = pd.DataFrame().from_dict(distance_map)
    print(df.sort_index()[sorted(df.columns.values)].to_string())
    print()
    new_map = {graph.get(valve).name: graph.get(valve).flow_rate for valve in distance_map}
    print(new_map)
    points = sorted(new_map.keys())
    print(points)
    paths = _permutation(distance_map, points[1:], _START_POINT, minutes)
    valid_paths = set([_make_path_valid(path, distance_map, minutes) for path in paths])
    print(len(valid_paths))
    return valid_paths


def _make_path_valid(path: List[str], distance_map: Dict[str, Dict[str, int]], minutes: int) -> Tuple[str]:
    act_minutes = minutes
    current_node = _START_POINT
    result = []
    for next_node in path:
        new_minutes = act_minutes - distance_map[current_node][next_node]
        if new_minutes <= 0:
            return tuple(result)
        result.append(next_node)
        current_node = next_node
        act_minutes = new_minutes
    return tuple(result)


def _create_all_path_and_subpaths_set(valid_path_set: Set[Tuple[str]]) -> Set[Tuple[str]]:
    result = set()
    for path in valid_path_set:
        for i in range(len(path)):
            result.add(path[:i+1])
    return result


def _create_reached_nodes_map(all_path_and_subpaths_set: Set[Tuple[str]], valves: List[str]) -> Dict[str, Set[Tuple[str]]]:
    result = {valve: set() for valve in valves}
    for path in all_path_and_subpaths_set:
        for valve in valves:
            if valve in path:
                result[valve].add(path)
    return result


def _get_elephant_paths(path: Tuple[str], all_paths: Set[Tuple[str]], reached_nodes_map: Dict[str, Set[Tuple[str]]]) -> Set[Tuple[str]]:
    result = set([path for path in all_paths])
    for node in reached_nodes_map.keys():
        if node in path:
            result = result.difference(reached_nodes_map[node])
    return result


if __name__ == '__main__':
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    #lines = _INPUT.split("\n")
    graph = Graph(lines)
    _simple_task(graph, minutes=30)  # 1991
    _advanced_task(graph, minutes=26)  # 2705
