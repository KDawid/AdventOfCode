import re
from typing import List

_INPUT = """    [D]
[N] [C]
[Z] [M] [P]
1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

_INSTRUCTION_PATTERN = r"move (?P<num>\d+)\s+from\s+(?P<from>\d+)\s+to\s+(?P<to>\d+)"


class Stacks:
    def __init__(self, lines: List[str]):
        self._stacks = dict()
        self._fill_stacks(lines)

    def move(self, num: int, from_stack: str, to_stack: str):
        self._stacks[to_stack] += reversed(self._stacks[from_stack][-num:])
        self._stacks[from_stack] = self._stacks[from_stack][:-num]

    def advanced_move(self, num: int, from_stack: str, to_stack: str):
        self._stacks[to_stack] += self._stacks[from_stack][-num:]
        self._stacks[from_stack] = self._stacks[from_stack][:-num]

    def get_tops(self) -> str:
        result = ""
        for name in self._stack_names:
            result += self._stacks[name][-1]
        return result

    def _fill_stacks(self, lines):
        self._stack_names = list()
        lines[-1] = f" {lines[-1]} "
        number_of_stacks = (len(lines[-1])+1) // 4
        for i in range(number_of_stacks):
            position = 4 * i + 1
            stack_name = lines[-1][position]
            self._stack_names.append(stack_name)
            self._stacks[stack_name] = list()
            for j in reversed(range(len(lines[:-1]))):
                if len(lines[j]) <= position:
                    continue
                stack_item = lines[j][position]
                if stack_item != ' ':
                    self._stacks[stack_name].append(stack_item)


if __name__ == '__main__':
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    #lines = _INPUT.split("\n")
    separator = lines.index('')
    stacks = Stacks(lines[:separator])

    for i in range(separator+1, len(lines)):
        if len(lines[i]) == 0:
            continue
        matches = re.search(_INSTRUCTION_PATTERN, lines[i])
        stacks.move(int(matches.group('num')), matches.group('from'), matches.group('to'))
    print(stacks.get_tops())

    stacks = Stacks(lines[:separator])

    for i in range(separator+1, len(lines)):
        if len(lines[i]) == 0:
            continue
        matches = re.search(_INSTRUCTION_PATTERN, lines[i])
        stacks.advanced_move(int(matches.group('num')), matches.group('from'), matches.group('to'))
    print(stacks.get_tops())



