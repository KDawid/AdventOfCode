def _find_common_letter(line: str) -> str:
    half = len(line) // 2
    common_letters = set(line[:half]).intersection(set(line[half:]))
    if len(common_letters) == 1:
        return common_letters.pop()
    raise ValueError(line, common_letters)


def _get_priority(letter: str) -> int:
    return _PRIORITY_TABLE[letter]


_PRIORITY_TABLE = {letter: prio for letter, prio in zip("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", range(1, 53))}

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]


line3s = ["vJrwpWtwJgWrhcsFMMfFFhFp",
"jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
"PmmdzqPrVvPwwTWBwg",
"wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
"ttgJtRGJQctTZtZT",
"CrZsJsPPZsGzwwsLwLmpwMDw"]


score = 0
for line in lines:
    common_letter = _find_common_letter(line)
    score += _get_priority(common_letter)

print(score)


def _find_advanced_common_letter(line_1: str, line_2: str, line_3: str) -> str:
    common_letters = set(line_1).intersection(set(line_2)).intersection(set(line_3))
    if len(common_letters) == 1:
        return common_letters.pop()
    raise ValueError(line_1, common_letters)


new_score = 0
for i in range(len(lines) // 3):
    index = 3 * i
    common_letter = _find_advanced_common_letter(lines[index], lines[index+1], lines[index+2])
    new_score += _get_priority(common_letter)

print(new_score)
