class Position:
    def __init__(self, pos=0, depth=0):
        self.pos = pos
        self.depth = depth

    def add_pos(self, value):
        self.pos += value

    def add_depth(self, value):
        self.depth += value

    def get_coordinates(self):
        return self.pos, self.depth

    def __str__(self):
        return f'({self.pos}, {self.depth})'


class AimedPosition(Position):
    def __init__(self, pos=0, depth=0, aim=0):
        super().__init__(pos, depth)
        self.aim = aim

    def add_pos(self, value):
        super().add_pos(value)
        self.depth += value * self.aim

    def add_depth(self, value):
        self.aim += value

    def get_coordinates(self):
        return self.pos, self.depth

    def __str__(self):
        return f'({self.pos}, {self.depth}, {self.aim})'


class Command:
    FORWARD_COMMAND = 'forward'
    DOWN_COMMAND = 'down'
    UP_COMMAND = 'up'

    TYPE = 'Abstract Command class'

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.TYPE} --> {self.value}'

    def update_position(self, position):
        raise NotImplementedError('This method shall be implemented!')


class ForwardCommand(Command):
    TYPE = Command.FORWARD_COMMAND

    def update_position(self, position):
        position.add_pos(self.value)


class DownCommand(Command):
    TYPE = Command.DOWN_COMMAND

    def update_position(self, position):
        position.add_depth(self.value)


class UpCommand(Command):
    TYPE = Command.UP_COMMAND

    def update_position(self, position):
        position.add_depth(-self.value)


def first_task(file_path):
    data = load_data(file_path)
    position = Position()
    for command in data:
        command.update_position(position)
    print(position)
    x, y = position.get_coordinates()
    return x * y


def load_data(file_path):
    with open(file_path) as f:
        data = [create_command(line.strip()) for line in f.readlines()]
    return data


def create_command(command_line):
    command, value = command_line.split(' ')
    if command == Command.FORWARD_COMMAND:
        return ForwardCommand(int(value))
    elif command == Command.DOWN_COMMAND:
        return DownCommand(int(value))
    elif command == Command.UP_COMMAND:
        return UpCommand(int(value))
    else:
        raise ValueError(f'Could not parse command from line "{command_line}"')


def second_task(file_path):
    data = load_data(file_path)
    position = AimedPosition()
    for command in data:
        command.update_position(position)
    print(position)
    x, y = position.get_coordinates()
    return x * y


if __name__ == '__main__':
    FILE_PATH = 'input.txt'
    res_1 = first_task(FILE_PATH)
    print(res_1)
    res_2 = second_task(FILE_PATH)
    print(res_2)
