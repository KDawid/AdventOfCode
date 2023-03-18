from typing import List, Iterator

from dataclasses import dataclass

_INPUT = """noop
addx 3
addx -5"""

_INPUT2 = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""


def _check(signal, circle):
    if circle in [20, 60, 100, 140, 180, 220]:
        # print(circle, signal, signal * circle)
        return signal * circle
    return 0


def _simple_task(lines: List[str]):
    result = 0
    signal = 1
    circle = 1
    for line in lines:
        # print(line)
        result += _check(signal, circle)
        if line == "noop":
            circle += 1
        elif line.startswith("addx "):
            circle += 1
            value = int(line[5:])
            result += _check(signal, circle)
            circle += 1
            signal += value
    print(result)


def _advanced_check(draw_pos, sprite_pos, result, step=1):
    if draw_pos in sprite_pos:
        result[draw_pos] = '#'
    draw_pos += step
    if draw_pos % 40 == 0 and step > 0:
        print(''.join(result))
        return 0, sprite_pos, ['.' for _ in range(40)]
    return draw_pos, sprite_pos, result


def _advanced_task(lines: List[str]):
    result = ['.' for _ in range(40)]
    draw_pos = 0
    sprite_pos = [0, 1, 2]
    for line in lines:
        # print(line)
        if line == "noop":
            draw_pos, sprite_pos, result = _advanced_check(draw_pos, sprite_pos, result)
        elif line.startswith("addx "):
            draw_pos, sprite_pos, result = _advanced_check(draw_pos, sprite_pos, result)
            draw_pos, sprite_pos, result = _advanced_check(draw_pos, sprite_pos, result)
            value = int(line[5:])
            sprite_pos = [value + pos for pos in sprite_pos]
            draw_pos, sprite_pos, result = _advanced_check(draw_pos, sprite_pos, result, step=0)
        #print(draw_pos, sprite_pos, ''.join(result))


if __name__ == '__main__':
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    #lines = _INPUT2.split("\n")
    _simple_task(lines)
    _advanced_task(lines)

