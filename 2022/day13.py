import json
from functools import reduce, cmp_to_key
from typing import List, Iterator, Callable, Tuple

import numpy as np
from dataclasses import dataclass

_INPUT = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


def _compare_values(left, right, indent=0, verbose=False):
    if verbose:
        print(f"{' ' * indent}- Compare {left} vs {right}")
    if isinstance(left, int) and isinstance(right, int):
        if left != right:
            if verbose and left < right:
                print(f"{' ' * (indent + 2)}- Left side is smaller, so inputs are in the right order")
            if verbose and right < left:
                print(f"{' ' * (indent + 2)}- Right side is smaller, so inputs are not in the right order")
            raise ValueError(left < right)
    if isinstance(left, list) and isinstance(right, list):
        for i in range(max(len(left), len(right))):
            if i == len(left):
                if verbose:
                    print(f"{' ' * (indent + 2)}- Left side ran out of items, so inputs are in the right order")
                raise ValueError(True)
            if i == len(right):
                if verbose:
                    print(f"{' ' * (indent + 2)}- Right side ran out of items, so inputs are not in the right order")
                raise ValueError(False)
            _compare_values(left[i], right[i], indent+2, verbose)
    if isinstance(left, int) and isinstance(right, list):
        if verbose:
            print(f"{' ' * (indent + 2)}- Mixed types; convert left to {left} and retry comparison")
        _compare_values([left], right, indent+2, verbose)
    if isinstance(left, list) and isinstance(right, int):
        if verbose:
            print(f"{' ' * (indent + 2)}- Mixed types; convert right to {right} and retry comparison")
        _compare_values(left, [right], indent+2, verbose)


def _simple_task(lines: List[str]):
    result = 0
    for i in range((len(lines) // 3) + 1):
        print()
        print(f"== Pair {i + 1} ==")
        left, right = json.loads(lines[i*3]), json.loads(lines[i*3+1])
        try:
            _compare_values(left, right, verbose=True)
        except ValueError as e:
            print("RESULT", str(e))
            if e.args[0]:
                result += i+1
    print(result)


def _advanced_task(lines: List[str]):
    values = [json.loads(line) for line in lines if 0 < len(line)]
    key_func = cmp_to_key(special_sorting_function)
    new_values = sorted(values, key=key_func)
    print((new_values.index([[2]])+1) * (new_values.index([[6]])+1))


def special_sorting_function(left, right):
    try:
        _compare_values(left, right)
    except ValueError as e:
        return -1 if e.args[0] else 1


if __name__ == '__main__':
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    #lines = _INPUT.split("\n")
    _simple_task(lines)

    lines.append("[[2]]")
    lines.append("[[6]]")

    _advanced_task(lines)
