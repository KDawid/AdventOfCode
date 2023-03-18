import numpy as np


class BingoBoard:
    def __init__(self, data):
        self.board = data
        self.marked = np.full(data.shape, False, dtype=bool)
        self.won = False

    def mark(self, number):
        check = np.where(self.board == number, True, False)
        if np.any(check):
            self.marked |= check
            self.__check_if_won()

    def __check_if_won(self):
        for i in range(len(self.marked)):
            if np.all(self.marked[i, :]) or np.all(self.marked[:, i]):
                self.won = True

    def get_sum_of_unmarked(self):
        return np.sum(self.board[np.where(self.marked, False, True)])

    def __str__(self):
        return str(self.board)


def first_task(file_path):
    numbers, boards = load_data(file_path)
    for number in numbers:
        for board in boards:
            board.mark(number)
            if board.won:
                return board.get_sum_of_unmarked() * number
    return 0


def load_data(file_path):
    with open(file_path) as f:
        numbers = [int(num) for num in f.readline().split(',')]
        boards = []
        try:
            while f.readline():
                board_data = np.array([next(f).strip().replace('  ', ' ').split(' ') for _ in range(5)], dtype=np.uint8)
                boards.append(BingoBoard(board_data))
        except StopIteration:
            pass
    return numbers, boards


def second_task(file_path):
    numbers, boards = load_data(file_path)
    board_statuses = np.full((len(boards)), False, dtype=bool)
    for number in numbers:
        for i in range(len(boards)):
            boards[i].mark(number)
            if boards[i].won:
                board_statuses[i] = True
                if np.all(board_statuses):
                    return boards[i].get_sum_of_unmarked() * number
    return 0


if __name__ == '__main__':
    FILE_PATH = 'input.txt'
    res_1 = first_task(FILE_PATH)
    print(res_1)
    res_2 = second_task(FILE_PATH)
    print(res_2)
