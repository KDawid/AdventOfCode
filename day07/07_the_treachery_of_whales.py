class OptimaFinder:
    def find_optima(self, positions):
        val_res, val_fuel = None, float('inf')
        for value in range(min(positions), max(positions) + 1):
            fuel = self._calculate_fuel_needed(positions, value)
            if fuel < val_fuel:
                val_res, val_fuel = value, fuel
        return val_res, val_fuel

    def _calculate_fuel_needed(self, positions, value):
        res = 0
        for pos in positions:
            res += self._get_needed_fuel(abs(pos - value))
        return res

    def _get_needed_fuel(self, moving):
        return moving


class AdvancedOptimaFinder(OptimaFinder):
    def _get_needed_fuel(self, moving):
        return moving * (moving + 1) // 2


def first_task(file_path):
    positions = read_numbers(file_path)
    best_value, fuel = OptimaFinder().find_optima(positions)
    return fuel


def read_numbers(file_path):
    with open(file_path) as f:
        return [int(num) for num in f.readline().strip().split(',')]


def second_task(file_path):
    positions = read_numbers(file_path)
    best_value, fuel = AdvancedOptimaFinder().find_optima(positions)
    return fuel


if __name__ == '__main__':
    FILE_PATH = 'input.txt'
    res_1 = first_task(FILE_PATH)
    print(res_1)
    res_2 = second_task(FILE_PATH)
    print(res_2)
