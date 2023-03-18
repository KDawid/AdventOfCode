from functools import reduce
from typing import List, Iterator, Callable, Tuple

from dataclasses import dataclass

_INPUT = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


class Monkey:
    def __init__(self, items: List[int], operation_params: Tuple, pass_params: Tuple):
        self._items = items

        operand, value = operation_params
        self._operation = lambda x: _operate(x, operand, value)

        to_if_true, self._divisible, to_if_false = pass_params
        self._pass_condition = lambda x: to_if_true if x % self._divisible == 0 else to_if_false

        self._chase = 0

    def get_items(self):
        return self._items

    def where_to_pass(self, item: int, normalizer: int = 1) -> (int, int):
        self._chase += 1
        worry_level = self._operation(item)
        monkey_worry = worry_level // normalizer
        pass_to = self._pass_condition(monkey_worry)
        return pass_to, monkey_worry

    def set_items(self, items: List[int]):
        self._items = items

    def add_item(self, item: int):
        self._items.append(item)

    def get_chase(self) -> int:
        return self._chase

    def get_divisible(self) -> int:
        return self._divisible

    def normalize_items(self, common_num: int):
        self._items = [item % common_num for item in self._items]

    def __str__(self) -> str:
        return ', '.join([str(i) for i in self._items])


class Monkeys:
    def __init__(self):
        self._monkeys = dict()
        self._sorted_keys = []

    def add_monkey(self, num: int, monkey: Monkey):
        self._monkeys[num] = monkey
        self._sorted_keys = sorted(self._monkeys.keys())

    def get(self, num: int) -> Monkey:
        return self._monkeys[num]

    def get_numbers(self) -> List[int]:
        return self._sorted_keys

    def pass_item(self, new_item: int, number: int, where_to_pass: int):
        new_items = self.get(number).get_items()[1:]
        self.get(number).set_items(new_items)
        self.get(where_to_pass).add_item(new_item)

    def get_monkey_business(self) -> int:
        chases = sorted([monkey.get_chase() for monkey in self._monkeys.values()], reverse=True)
        return chases[0] * chases[1]

    def get_chases_str(self) -> str:
        return '\n'.join([f'Monkey {number}: {self.get(number).get_chase()}' for number in self.get_numbers()])

    def normalize_items(self):
        common_num = reduce(lambda x, y: x * y, [monkey.get_divisible() for monkey in self._monkeys.values()])
        for monkey in self._monkeys.values():
            monkey.normalize_items(common_num)

    def __str__(self) -> str:
        return '\n'.join([f'Monkey {number}: {str(self.get(number))}' for number in self.get_numbers()])


def _one_round(monkeys: Monkeys, normalizer: int = 1) -> Monkeys:
    for number in monkeys.get_numbers():
        monkey = monkeys.get(number)
        for item in monkey.get_items():
            where_to_pass, new_item = monkey.where_to_pass(item, normalizer=normalizer)
            monkeys.pass_item(new_item, number, where_to_pass)
    return monkeys


def _simple_task(monkeys: Monkeys, rounds: int = 20):
    for _ in range(rounds):
        monkeys = _one_round(monkeys, normalizer=3)
        # print(monkeys)
        # print()
    print(monkeys.get_monkey_business())


def _operate(num: int, operand: str, value: int) -> int:
    int_val = num if value == "old" else int(value)
    if operand == "+":
        return num + int_val
    elif operand == "-":
        return num - int_val
    elif operand == "*":
        return num * int_val
    raise ValueError(f"Unknown operand: {operand}")


def _read_monkeys(lines: List[str]) -> Monkeys:
    monkeys = Monkeys()
    for plain_line in lines:
        line = plain_line.strip()
        if line.startswith("Monkey "):
            monkey_num = int(line[7:-1])
        elif line.startswith("Starting items: "):
            items = [int(item) for item in line[16:].split(', ')]
        elif line.startswith("Operation: new = old "):
            operand = line[21]
            value = line[23:]
        elif line.startswith("Test: divisible by "):
            divisible = int(line[19:])
        elif line.startswith("If true: throw to monkey "):
            to_if_true = int(line[25:])
        elif line.startswith("If false: throw to monkey "):
            to_if_false = int(line[26:])
            operation_params = (operand, value)
            pass_params = (to_if_true, divisible, to_if_false)
            monkey = Monkey(items, operation_params, pass_params)
            monkeys.add_monkey(monkey_num, monkey)
    return monkeys


def _advanced_task(monkeys: Monkeys, rounds: int = 10000):
    for i in range(1, rounds+1):
        monkeys = _one_round(monkeys)
        monkeys.normalize_items()
        if i in (1, 20, 100, 200, 300, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000):
            print(f"== After round {i} ==")
            print(monkeys.get_chases_str())
            # print(monkeys)
            print()
    print(monkeys.get_monkey_business())


if __name__ == '__main__':
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    # lines = _INPUT.split("\n")
    monkeys = _read_monkeys(lines)
    _simple_task(monkeys)

    monkeys = _read_monkeys(lines)
    _advanced_task(monkeys)
