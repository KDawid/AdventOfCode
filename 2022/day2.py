class OPPONENT:
    ROCK = "A"
    PAPER = "B"
    SCRISSORS = "C"


class PLAYER:
    ROCK = "X"
    PAPER = "Y"
    SCRISSORS = "Z"


def _get_symbol_point(player_symbol: str) -> int:
    if player_symbol == PLAYER.ROCK:
        return 1
    if player_symbol == PLAYER.PAPER:
        return 2
    if player_symbol == PLAYER.SCRISSORS:
        return 3


def _player_win(opponent_symbol: str, player_symbol: str) -> bool:
    return (opponent_symbol == OPPONENT.ROCK and player_symbol == PLAYER.PAPER
           ) or (opponent_symbol == OPPONENT.PAPER and player_symbol == PLAYER.SCRISSORS
                 ) or (opponent_symbol == OPPONENT.SCRISSORS and player_symbol == PLAYER.ROCK)


def _is_draw(opponent_symbol: str, player_symbol: str) -> bool:
    return (opponent_symbol == OPPONENT.ROCK and player_symbol == PLAYER.ROCK
           ) or (opponent_symbol == OPPONENT.PAPER and player_symbol == PLAYER.PAPER
                 ) or (opponent_symbol == OPPONENT.SCRISSORS and player_symbol == PLAYER.SCRISSORS)


def _get_result_point(opponent_symbol: str, player_symbol: str) -> int:
    if _player_win(opponent_symbol, player_symbol):
        return 6
    if _is_draw(opponent_symbol, player_symbol):
        return 3
    return 0

with open("input.txt") as f:
    lines = [line.strip().split() for line in f.readlines()]


lines2 = [line.split() for line in ["A Y",
"B X",
"C Z"]]

score = 0

for line in lines:
    base_point = _get_symbol_point(line[1])
    result_point = _get_result_point(line[0], line[1])
    score += base_point + result_point

print(score)


#######################################################


class OUTCOME:
    LOSE = "X"
    DRAW = "Y"
    WIN = "Z"


def _get_advanced_result_point(symbol: str) -> int:
    if symbol == OUTCOME.WIN:
        return 6
    if symbol == OUTCOME.DRAW:
        return 3
    if symbol == OUTCOME.LOSE:
        return 0


def _shall_choose_rock(opponent_symbol: str, outcome_symbol: str) -> bool:
    return (opponent_symbol == OPPONENT.ROCK and outcome_symbol == OUTCOME.DRAW
            ) or (opponent_symbol == OPPONENT.PAPER and outcome_symbol == OUTCOME.LOSE
                  ) or (opponent_symbol == OPPONENT.SCRISSORS and outcome_symbol == OUTCOME.WIN)


def _shall_choose_paper(opponent_symbol: str, outcome_symbol: str) -> bool:
    return (opponent_symbol == OPPONENT.ROCK and outcome_symbol == OUTCOME.WIN
            ) or (opponent_symbol == OPPONENT.PAPER and outcome_symbol == OUTCOME.DRAW
                  ) or (opponent_symbol == OPPONENT.SCRISSORS and outcome_symbol == OUTCOME.LOSE)


def _get_advanced_symbol_point(opponent_symbol: str, outcome_symbol: str) -> int:
    if _shall_choose_rock(opponent_symbol, outcome_symbol):
        return 1
    if _shall_choose_paper(opponent_symbol, outcome_symbol):
        return 2
    return 3


score = 0
for line in lines:
    result_point = _get_advanced_result_point(line[1])
    base_point = _get_advanced_symbol_point(line[0], line[1])
    score += result_point + base_point

print(score)
