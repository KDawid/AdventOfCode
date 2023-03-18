class LanternFishPool:
    NEWBY_TIMER = 8
    RESET_TIMER = 6

    def __init__(self, initial_state):
        self.pool = initial_state

    def next_day(self):
        newbies_num = 0
        for i in range(len(self.pool)):
            if self.pool[i] == 0:
                self.pool[i] = self.RESET_TIMER
                newbies_num += 1
            else:
                self.pool[i] -= 1
        self.pool += [self.NEWBY_TIMER for _ in range(newbies_num)]

    def get_number_of_fish(self):
        return len(self.pool)

    def __str__(self):
        return str(self.pool)


class AdvancedLanternFishPool:
    NEWBY_TIMER = 8
    RESET_TIMER = 6

    def __init__(self, initial_state):
        self.pool = dict({x: 0 for x in range(self.NEWBY_TIMER+1)})
        for fish_state in initial_state:
            self.pool[fish_state] += 1

    def next_day(self):
        newbies_num = self.pool[0]
        for i in range(self.NEWBY_TIMER):
            self.pool[i] = self.pool[i+1]
        self.pool[self.NEWBY_TIMER] = newbies_num
        self.pool[self.RESET_TIMER] += newbies_num

    def get_number_of_fish(self):
        return sum([num for num in self.pool.values()])

    def __str__(self):
        return str(self.pool)


def first_task(file_path, days):
    fish_states = read_numbers(file_path)
    pool = LanternFishPool(fish_states)
    # print(fish_states)
    for i in range(days):
        pool.next_day()
        # print(f'Day {i+1}: {pool}')
    return pool.get_number_of_fish()


def read_numbers(file_path):
    with open(file_path) as f:
        return [int(num) for num in f.readline().strip().split(',')]


def second_task(file_path, days):
    fish_states = read_numbers(file_path)
    pool = AdvancedLanternFishPool(fish_states)
    # print(fish_states)
    for i in range(days):
        pool.next_day()
        # print(f'Day {i+1}: {pool}')
    return pool.get_number_of_fish()


if __name__ == '__main__':
    FILE_PATH = 'input.txt'
    res_1 = first_task(FILE_PATH, days=80)
    print(res_1)
    res_2 = second_task(FILE_PATH, days=256)
    print(res_2)
