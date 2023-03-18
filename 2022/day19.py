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


_INPUT = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""


@dataclass
class State:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def add(self, state):
        if state.ore:
            self.ore += state.ore
        if state.clay:
            self.clay += state.clay
        if state.obsidian:
            self.obsidian += state.obsidian
        if state.geode:
            self.geode += state.geode

    def remove(self, state):
        self.ore -= state.ore
        self.clay -= state.clay
        self.obsidian -= state.obsidian
        self.geode -= state.geode

    def any(self) -> bool:
        return 0 < self.ore + self.clay + self.obsidian + self.geode

    def is_valid(self):
        return 0 <= self.ore and 0 <= self.clay and 0 <= self.obsidian and 0 <= self.geode

    @staticmethod
    def copy(state):
        return State(ore=state.ore, clay=state.clay, obsidian=state.obsidian, geode=state.geode)

    def __str__(self):
        return f"(ore={self.ore}, clay={self.clay}, obsidian={self.obsidian}, geode={self.geode})"

    def __hash__(self):
        return hash(str(self))


@dataclass
class Configuration:
    minerals: State = State()
    robots: State = State(ore=1)

    @staticmethod
    def copy(configuraiton):
        return Configuration(minerals=State.copy(configuraiton.minerals),
                             robots=State.copy(configuraiton.robots))

    def __str__(self):
        return f"[minerals={self.minerals}; robots={self.robots}]"

    def __hash__(self):
        return hash(str(self))


@dataclass
class Blueprint:
    _BLUEPRINT_PATTERN = r"^Blueprint (?P<blueprint_num>\d+): Each ore robot costs (?P<ore_robot_cost_ore>\d+) ore. " \
                         r"Each clay robot costs (?P<clay_robot_cost_ore>\d+) ore. " \
                         r"Each obsidian robot costs (?P<obsidian_robot_cost_ore>\d+) ore and (?P<obsidian_robot_cost_clay>\d+) clay. " \
                         r"Each geode robot costs (?P<geode_robot_cost_ore>\d+) ore and (?P<geode_robot_cost_obsidian>\d+) obsidian.$"

    def __init__(self, line: str):
        m = re.match(self._BLUEPRINT_PATTERN, line)
        self._blueprint_num = int(m.group("blueprint_num"))
        self._ore_robot_cost_ore = int(m.group("ore_robot_cost_ore"))
        self._clay_robot_cost_ore = int(m.group("clay_robot_cost_ore"))
        self._obsidian_robot_cost_ore = int(m.group("obsidian_robot_cost_ore"))
        self._obsidian_robot_cost_clay = int(m.group("obsidian_robot_cost_clay"))
        self._geode_robot_cost_ore = int(m.group("geode_robot_cost_ore"))
        self._geode_robot_cost_obsidian = int(m.group("geode_robot_cost_obsidian"))

    def get_num(self) -> int:
        return self._blueprint_num

    def how_many_robots_can_be_created(self, mineral_state: State) -> State:
        return State(ore=mineral_state.ore // self._ore_robot_cost_ore,
                     clay=mineral_state.ore // self._clay_robot_cost_ore,
                     obsidian=min(mineral_state.ore // self._obsidian_robot_cost_ore,
                                  mineral_state.clay // self._obsidian_robot_cost_clay),
                     geode=min(mineral_state.ore // self._geode_robot_cost_ore,
                               mineral_state.obsidian // self._geode_robot_cost_obsidian)
                     )

    def create_robots(self, robots: State, mineral_state: State) -> State:
        mineral_state.ore -= self._ore_robot_cost_ore * robots.ore
        mineral_state.clay -= self._clay_robot_cost_ore * robots.clay

        if 0 < robots.obsidian:
            mineral_state.ore -= self._obsidian_robot_cost_ore * robots.obsidian
            mineral_state.clay -= self._obsidian_robot_cost_clay * robots.obsidian
        if 0 < robots.geode:
            mineral_state.ore -= self._geode_robot_cost_ore * robots.geode
            mineral_state.obsidian -= self._geode_robot_cost_obsidian * robots.geode
        return mineral_state

    def create_possible_configurations(self, configuration: Configuration):
        result = set()
        can_create = self.how_many_robots_can_be_created(configuration.minerals)
        if self._can_create_too_many(can_create):
            return result
        if can_create.any():
            for num in range(1, can_create.ore+1):
                minerals = State.copy(configuration.minerals)
                minerals.ore -= self._ore_robot_cost_ore * num
                robots = State.copy(configuration.robots)
                robots.ore += num
                if minerals.is_valid():
                    result.add(Configuration(minerals=minerals, robots=robots))
                #print(f"\tSpend {self._ore_robot_cost_ore} ore to start building an ore-collecting robot.")
            for num in range(1, can_create.clay+1):
                minerals = State.copy(configuration.minerals)
                minerals.ore -= self._clay_robot_cost_ore * num
                robots = State.copy(configuration.robots)
                robots.clay += num
                if minerals.is_valid():
                    result.add(Configuration(minerals=minerals, robots=robots))
                #print(f"\tSpend {self._clay_robot_cost_ore} ore to start building a clay-collecting robot.")
            for num in range(1, can_create.obsidian+1):
                minerals = State.copy(configuration.minerals)
                minerals.ore -= self._obsidian_robot_cost_ore * num
                minerals.clay -= self._obsidian_robot_cost_clay * num
                robots = State.copy(configuration.robots)
                robots.obsidian += num
                if minerals.is_valid():
                    result.add(Configuration(minerals=minerals, robots=robots))
                #print(f"\tSpend {self._obsidian_robot_cost_ore} ore and {self._obsidian_robot_cost_clay} clay to start building an obsidian-collecting robot.")
            for num in range(1, can_create.geode+1):
                minerals = State.copy(configuration.minerals)
                minerals.ore -= self._geode_robot_cost_ore * num
                minerals.obsidian -= self._geode_robot_cost_obsidian * num
                robots = State.copy(configuration.robots)
                robots.geode += num
                if minerals.is_valid():
                    result.add(Configuration(minerals=minerals, robots=robots))
                #print(f"\tSpend {self._geode_robot_cost_ore} ore and {self._geode_robot_cost_obsidian} obsidian to start building a geode-collecting robot.")
        return result

    @staticmethod
    def _can_create_too_many(can_create: State) -> bool:
        return (can_create.ore >= 2 and can_create.clay >= 2 and can_create.obsidian >= 2) or (
                can_create.ore >= 2 and can_create.obsidian >= 2 and can_create.geode >= 2) or (
                can_create.ore >= 2 and can_create.obsidian >= 2 and can_create.geode >= 2) or (
                can_create.clay >= 2 and can_create.obsidian >= 2 and can_create.geode >= 2)


class Simulation:
    def __init__(self, blueprint: Blueprint):
        self._blueprint = blueprint

    def simulate(self, minutes: int):
        old_configurations = {Configuration()}
        for minute in range(minutes):
            #print(f"== Minute {minute+1} ==")
            new_configurations = set()
            for configuration in old_configurations:
                new_config = Configuration.copy(configuration)
                new_config.minerals.add(new_config.robots)
                new_configurations.add(new_config)
                configurations_with_new_robots = self._blueprint.create_possible_configurations(configuration)
                for conf in configurations_with_new_robots:
                    conf.minerals.add(new_config.robots)
                new_configurations = new_configurations.union(configurations_with_new_robots)
            old_configurations = self._keep_better(new_configurations)
            #print(f"\t{len(new_configurations)} config(s) -> max {max([configuration.minerals.geode for configuration in old_configurations])} geode")
            #print()
            print(f"\t{minute+1}. {len(old_configurations)}")
        return max([configuration.minerals.geode for configuration in old_configurations])

    def _keep_better(self, configurations: Set[Configuration]) -> Set[Configuration]:
        drop_indices = set()
        config_list = list(configurations)
        for i in range(len(config_list)):
            for j in range(i+1, len(config_list)):
                if self._is_better_config(config_list[i], config_list[j]):
                    drop_indices.add(j)
                if self._is_better_config(config_list[j], config_list[i]):
                    drop_indices.add(i)
        return set([config_list[i] for i in range(len(config_list)) if i not in drop_indices])

    def _is_better_config(self, config1: Configuration, config2: Configuration) -> bool:
        return self._is_better_state(config1.minerals, config2.minerals) and self._is_better_state(config1.robots, config2.robots)

    def _is_better_state(self, state1: State, state2: State) -> bool:
        return (state1.ore >= state2.ore and state1.clay >= state2.clay and state1.obsidian >= state2.obsidian and state1.geode >= state2.geode) or (state1.geode > state2.geode)


def _simple_task(blueprints: List[Blueprint]):
    result = 0
    for blueprint in blueprints:
        simulation = Simulation(blueprint)
        num = blueprint.get_num()
        print(f"Blueprint {num}")
        max_geode = simulation.simulate(minutes=24)
        print(num, max_geode)
        print()
        result += num * max_geode
    print(result)


if __name__ == '__main__':
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    lines = _INPUT.split("\n")

    blueprints = [Blueprint(line) for line in lines]

    _simple_task(blueprints)
    #_advanced_task(lines)
