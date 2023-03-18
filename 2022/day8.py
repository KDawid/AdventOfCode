from typing import List, Iterator

from dataclasses import dataclass

_INPUT = """30373
25512
65332
33549
35390"""


@dataclass
class Tree:
    height: int
    visible: bool


class AdvancedTree:
    height: int
    left: int = 0
    right: int = 0
    up: int = 0
    down: int = 0

    def __init__(self, height: int):
        self.height = height

    def get_scenic_score(self):
        return self.up * self.down * self.left * self.right

    def __str__(self):
        return str(self.height)


def _update_visibility(forest: List[List[Tree]]) -> List[List[Tree]]:
    result = [[Tree(item.height, False) for item in line] for line in forest]
    for i in range(len(forest)):
        _check([result[i][j] for j in range(len(result[i]))], direction="Left")
        _check([result[i][j] for j in reversed(range(len(result[i])))], direction="Right")
    for i in range(len(result[0])):
        _check([result[j][i] for j in range(len(result))], direction="Up")
        _check([result[j][i] for j in reversed(range(len(result)))], direction="Down")
    return result


def _check(line: List[Tree], direction=None):
    if direction:
        print(f"Check from {direction}")
    line[0].visible = True
    highest = line[0].height
    for tree in line:
        if tree.height > highest:
            tree.visible = True
            highest = tree.height
        if tree.height == 9:
            return


def _count_visibles(forest: List[List[Tree]]) -> int:
    result = 0
    for line in forest:
        for tree in line:
            if tree.visible:
                result += 1
    return result


def _update_advanced_visibility(forest: List[List[AdvancedTree]]) -> List[List[AdvancedTree]]:
    result = [[AdvancedTree(item.height) for item in line] for line in forest]
    for i in range(len(forest)):
        for j in range(len(forest[i])):
            _advanced_check(forest, i, j)
    return result


def _advanced_check(forest: List[List[AdvancedTree]], x: int, y: int):
    tree = forest[x][y]
    tree_height = tree.height
    # UP
    if x == 0:
        tree.up = 0
    else:
        for i in reversed(range(x)):
            tree.up += 1
            if tree_height <= forest[i][y].height:
                break
    # DOWN
    if x == len(forest)-1:
        tree.down = 0
    else:
        for i in range(x + 1, len(forest)):
            tree.down += 1
            if tree_height <= forest[i][y].height:
                break
    # LEFT
    if y == 0:
        tree.left = 0
    else:
        for i in reversed(range(y)):
            tree.left += 1
            if tree_height <= forest[x][i].height:
                break
    # RIGHT
    if y == len(forest[x]):
        tree.right = 0
    else:
        for i in range(y + 1, len(forest[x])):
            tree.right += 1
            if tree_height <= forest[x][i].height:
                break


if __name__ == '__main__':
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    #lines = _INPUT.split("\n")

    forest = [[Tree(int(height), False) for height in line] for line in lines]
    forest = _update_visibility(forest)
    number_of_visible = _count_visibles(forest)
    print(number_of_visible)

    advanced_forest = [[AdvancedTree(height=int(height)) for height in line] for line in lines]
    forest = _update_advanced_visibility(advanced_forest)

    max_score = max([max([tree.get_scenic_score() for tree in line]) for line in advanced_forest])
    print(max_score)
