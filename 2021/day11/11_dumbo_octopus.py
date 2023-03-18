class OctopusBehavior:
    WAITING = 'waiting'
    FLASHES = 'flashes'
    FLASHED = 'flashed'


class Octopus:
    def __init__(self, num):
        self.state = num
        self.behavior = OctopusBehavior.WAITING

    def next_state(self):
        self.state += 1
        if self.state > 9:
            self.behavior = OctopusBehavior.FLASHES

    def can_flash(self):
        return self.behavior == OctopusBehavior.FLASHES

    def flash(self):
        self.behavior = OctopusBehavior.FLASHED

    def be_flashed(self):
        if self.behavior == OctopusBehavior.WAITING:
            self.next_state()

    def has_flashed(self):
        return self.behavior == OctopusBehavior.FLASHED

    def reset(self):
        if self.state > 9:
            self.state = 0
        self.behavior = OctopusBehavior.WAITING

    def __str__(self):
        return str(self.state)


class OctopusGarden:
    def __init__(self, data):
        self.octopus_array = [[Octopus(num) for num in line] for line in data]
        self.octopus_num = sum([len(line) for line in data])
        self.flash_numbers = []

    def next_step(self):
        self.__increase_all_state()
        self.__flash_octopuses()
        self.__reset_octopus_states()

    def __increase_all_state(self):
        for line in self.octopus_array:
            for octopus in line:
                octopus.next_state()

    def __flash_octopuses(self):
        for i in range(len(self.octopus_array)):
            for j in range(len(self.octopus_array[i])):
                if self.octopus_array[i][j].can_flash():
                    self.__flash_octopus(i, j)

    def __flash_octopus(self, x, y):
        self.octopus_array[x][y].flash()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if 0 <= x+i < len(self.octopus_array) and 0 <= y+j < len(self.octopus_array[x+i]):
                    self.octopus_array[x+i][y+j].be_flashed()
                    if self.octopus_array[x+i][y+j].can_flash():
                        self.__flash_octopus(x+i, y+j)

    def __reset_octopus_states(self):
        flashes = 0
        for line in self.octopus_array:
            for octopus in line:
                if octopus.has_flashed():
                    flashes += 1
                octopus.reset()
        self.flash_numbers.append(flashes)

    def get_flash_number(self):
        return sum(self.flash_numbers)

    def was_perfect_synch(self):
        return len(self.flash_numbers) > 0 and self.flash_numbers[-1] == self.octopus_num

    def get_generation(self):
        return len(self.flash_numbers)

    def __str__(self):
        res = ''
        for line in self.octopus_array:
            res += ''.join([str(octopus) for octopus in line]) + '\n'
        return res


def first_task(file_path, steps=100):
    octopus_garden = OctopusGarden(read_data(file_path))
    for _ in range(steps):
        octopus_garden.next_step()
    return octopus_garden.get_flash_number()


def read_data(file_path):
    with open(file_path) as f:
        data = [[int(num) for num in line.strip()] for line in f.readlines()]
    return data


def second_task(file_path):
    octopus_garden = OctopusGarden(read_data(file_path))
    while not octopus_garden.was_perfect_synch():
        octopus_garden.next_step()
    return octopus_garden.get_generation()


if __name__ == '__main__':
    FILE_PATH = 'input.txt'
    res_1 = first_task(FILE_PATH, steps=100)
    print(res_1)
    res_2 = second_task(FILE_PATH)
    print(res_2)
