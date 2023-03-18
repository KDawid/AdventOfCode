from typing import List, Iterator

from dataclasses import dataclass

_INPUT = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

_INPUT_2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

@dataclass
class Position:
    x: int = 0
    y: int = 0

    def copy(self):
        return Position(x=self.x, y=self.y)

    def __hash__(self):
        return hash(f"({self.x},{self.y})")

    def __str__(self):
        return f"({self.x},{self.y})"


def _move_on_x(head: Position, tail: Position, direction: int):
    head.x += direction
    if abs(head.x - tail.x) > 1:
        tail.x += direction
        if head.y != tail.y:
            tail.y = head.y


def _move_on_y(head: Position, tail: Position, direction: int):
    head.y += direction
    if abs(head.y - tail.y) > 1:
        tail.y += direction
        if head.x != tail.x:
            tail.x = head.x


def _simple_task(lines: List[str]):
    head, tail = Position(), Position()
    visited = {tail.copy()}
    for line in lines:
        direction, volume = line[0], int(line[2:])
        if direction == "R":
            for _ in range(volume):
                _move_on_x(head, tail, 1)
                visited.add(tail.copy())
        elif direction == "L":
            for _ in range(volume):
                _move_on_x(head, tail, -1)
                visited.add(tail.copy())
        elif direction == "U":
            for _ in range(volume):
                _move_on_y(head, tail, 1)
                visited.add(tail.copy())
        elif direction == "D":
            for _ in range(volume):
                _move_on_y(head, tail, -1)
                visited.add(tail.copy())
    print(head, tail)
    print(len(visited))


def _normalize_rope(rope: List[Position]):
    for i in range(1, len(rope)):
        if rope[i-1].x - rope[i].x > 1:
            # moves rope to the right
            rope[i].x += 1
            if rope[i-1].y != rope[i].y:
                rope[i].y = rope[i].y + 1 if rope[i].y < rope[i-1].y else rope[i].y - 1
        elif rope[i].x - rope[i-1].x > 1:
            # moves rope to the left
            rope[i].x -= 1
            if rope[i - 1].y != rope[i].y:
                rope[i].y = rope[i].y + 1 if rope[i].y < rope[i-1].y else rope[i].y - 1
        elif rope[i-1].y - rope[i].y > 1:
            # moves rope up
            rope[i].y += 1
            if rope[i-1].x != rope[i].x:
                rope[i].x = rope[i].x + 1 if rope[i].x < rope[i-1].x else rope[i].x - 1
        elif rope[i].y - rope[i-1].y > 1:
            # moves rope down
            rope[i].y -= 1
            if rope[i - 1].x != rope[i].x:
                rope[i].x = rope[i].x + 1 if rope[i].x < rope[i-1].x else rope[i].x - 1


def _advanced_move_on_x(rope: List[Position], direction: int):
    rope[0].x += direction
    _normalize_rope(rope)


def _advanced_move_on_y(rope: List[Position], direction: int):
    rope[0].y += direction
    _normalize_rope(rope)


def _print_rope(rope):
    print([str(rope[i]) for i in range(len(rope))])
    min_x, max_x = min([r.x for r in rope]), max([r.x for r in rope])
    min_y, max_y = min([r.y for r in rope]), max([r.y for r in rope])
    result = []
    for i in range(max_y - min_y + 1):
        result.append(["." for _ in range (max_x - min_x + 1)])
    for i, r in enumerate(rope):
        if result[r.y - min_y][r.x - min_x] == ".":
            result[r.y - min_y][r.x - min_x] = str(i) if i != 0 else "H"
    for line in reversed(result):
        print(''.join(line))
    print()


def _advanced_task(lines: List[str], rope_line: int=10):
    rope = [Position() for _ in range(rope_line)]
    visited = {rope[-1].copy()}

    _print_rope(rope)
    for line in lines:
        direction, volume = line[0], int(line[2:])
        if direction == "R":
            for _ in range(volume):
                _advanced_move_on_x(rope, 1)
                visited.add(rope[-1].copy())
        elif direction == "L":
            for _ in range(volume):
                _advanced_move_on_x(rope, -1)
                visited.add(rope[-1].copy())
        elif direction == "U":
            for _ in range(volume):
                _advanced_move_on_y(rope, 1)
                visited.add(rope[-1].copy())
        elif direction == "D":
            for _ in range(volume):
                _advanced_move_on_y(rope, -1)
                visited.add(rope[-1].copy())
        _print_rope(rope)
        print("====================================")
    _print_rope(rope)
    print(visited)
    print(len(visited))


if __name__ == '__main__':
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    #lines = _INPUT_2.split("\n")
    _simple_task(lines)
    _advanced_task(lines)

