from typing import List


class Assignment:
    def __init__(self, start: int, end: int):
        self.start = int(start)
        self.end = int(end)

    def __str__(self):
        return f"({self.start}, {self.end})"


class Pair:
    def __init__(self, elf_1: Assignment, elf_2: Assignment):
        self.elf_1 = elf_1
        self.elf_2 = elf_2
        self.fully_contain = self._is_fully_contained()
        self.any_overlap = self._is_any_overlap()

    def _is_fully_contained(self) -> bool:
        return _is_contained_by(self.elf_1, self.elf_2) or _is_contained_by(self.elf_2, self.elf_1)

    def _is_any_overlap(self):
        return _is_ovelapping(self.elf_1, self.elf_2) or _is_ovelapping(self.elf_2, self.elf_1)


def _is_contained_by(elf_1: Assignment, elf_2: Assignment) -> bool:
    return elf_2.start <= elf_1.start and elf_1.end <= elf_2.end


def _is_ovelapping(elf_1: Assignment, elf_2: Assignment) -> bool:
    return elf_2.start <= elf_1.start <= elf_2.end


def _create_pair(line: str):
    elf_str_1, elf_str_2 = line.split(",")
    elf_1, elf_2 = Assignment(*elf_str_1.split("-")), Assignment(*elf_str_2.split("-"))
    return Pair(elf_1, elf_2)


def _part_one(pairs: List[Pair]):
    fully_contained_num = 0
    for pair in pairs:
        if pair.fully_contain:
            fully_contained_num += 1
    print(fully_contained_num)


def _part_two(pairs: List[Pair]):
    overlapping_num = 0
    for pair in pairs:
        if pair.any_overlap:
            overlapping_num += 1
    print(overlapping_num)


if __name__ == '__main__':
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    pairs: List[Pair] = list()

    for line in lines:
        pairs.append(_create_pair(line))

    _part_one(pairs)
    _part_two(pairs)
