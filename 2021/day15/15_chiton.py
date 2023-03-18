class RiskCalculator:
    def __init__(self, density_map):
        self.density_map = density_map
        self.costs = [[None for _ in range(len(self.density_map[i]))] for i in range(len(self.density_map))]
        self.__calculate_costs()

    def __calculate_costs(self):
        for i in range(len(self.density_map)):
            for j in range(len(self.density_map[i])):
                self.costs[i][j] = self.__calculate_cost(i, j)

    def __calculate_cost(self, i, j):
        if self.costs[i][j] is not None:
            return self.costs[i][j]
        if i == 0 and j == 0:
            return 0
        if i == 0:
            return self.density_map[i][j] + self.costs[i][j - 1]
        if j == 0:
            return self.density_map[i][j] + self.costs[i - 1][j]
        return self.density_map[i][j] + min([self.costs[i - 1][j], self.costs[i][j - 1]])

    def get_cost(self, i, j):
        return self.__calculate_cost(i, j)


def first_task(file_path):
    density_map = read_data(file_path)
    calculator = RiskCalculator(density_map)
    return calculator.get_cost(len(density_map) - 1, len(density_map[len(density_map) - 1]) - 1)


def read_data(file_path):
    res = []
    with open(file_path) as f:
        for line in f.readlines():
            res.append([int(c) for c in line.strip()])
    return res


def second_task(file_path, extend_scale=5):
    density_map = read_data(file_path)
    density_map = extend_density_map(density_map, times=extend_scale)

    calculator = RiskCalculator(density_map)
    return calculator.get_cost(len(density_map) - 1, len(density_map[len(density_map) - 1]) - 1)


def extend_density_map(density_map, times):
    input_len = len(density_map)
    res = [[None for _ in range(input_len * times)] for _ in range(input_len * times)]

    for i in range(len(res)):
        for j in range(len(res[i])):
            orig_x, orig_y = i % input_len, j % input_len
            extra = i // input_len + j // input_len
            res[i][j] = get_map_value(density_map[orig_x][orig_y] + extra)
    return res


def get_map_value(num):
    if num <= 9:
        return num
    return num % 9


if __name__ == '__main__':
    FILE_PATH = 'input.txt'
    res_1 = first_task(FILE_PATH)
    print(res_1)
    res_2 = second_task(FILE_PATH, extend_scale=5)  # THIS GIVES WRONG ANSWER - 2926 is too high
    print(res_2)
