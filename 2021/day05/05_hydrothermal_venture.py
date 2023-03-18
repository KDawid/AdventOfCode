import re


class LineSegment:
    X1_GROUP = 'x1'
    X2_GROUP = 'x2'
    Y1_GROUP = 'y1'
    Y2_GROUP = 'y2'

    INPUT_PATTERN = rf'(?P<{X1_GROUP}>\d+),(?P<{Y1_GROUP}>\d+) -> (?P<{X2_GROUP}>\d+),(?P<{Y2_GROUP}>\d+)'
    MATCHER = re.compile(INPUT_PATTERN)

    def __init__(self, str):
        m = self.MATCHER.match(str)
        if m:
            self.x1 = int(m.group(self.X1_GROUP))
            self.x2 = int(m.group(self.X2_GROUP))
            self.y1 = int(m.group(self.Y1_GROUP))
            self.y2 = int(m.group(self.Y2_GROUP))
        else:
            raise IOError(f'Could not parse input: {str}')

    def get_points(self):
        raise NotImplementedError('This method shall be implemented')

    @staticmethod
    def _generate_straight_line_points(point1, point2):
        p1, p2 = (point1, point2) if point1 < point2 else (point2, point1)
        return [num for num in range(p1, p2+1)]

    def __str__(self):
        return f'({self.x1}, {self.y1}) -> ({self.x2}, {self.y2})'


class StraightLineSegment(LineSegment):
    def __init__(self, str):
        super().__init__(str)

    def get_points(self):
        if self.x1 == self.x2:
            return [(self.x1, y) for y in self._generate_straight_line_points(self.y1, self.y2)]
        if self.y1 == self.y2:
            return [(x, self.y1) for x in self._generate_straight_line_points(self.x1, self.x2)]
        print('Points only can be generated for straight lines')
        return []


class DiagonalLineSegment(LineSegment):
    def __init__(self, str):
        super().__init__(str)

    def get_points(self):
        if self.x1 == self.x2:
            return [(self.x1, y) for y in self._generate_straight_line_points(self.y1, self.y2)]
        if self.y1 == self.y2:
            return [(x, self.y1) for x in self._generate_straight_line_points(self.x1, self.x2)]
        return self.__generate_diagonal_points()

    def __generate_diagonal_points(self):
        if abs(self.x2 - self.x1) != abs(self.y2 - self.y1):
            print(f'Error! This does ot seem diagonal: {self}')
        x, y = self.x1, self.y1
        x_direction = 1 if self.x1 < self.x2 else -1
        y_direction = 1 if self.y1 < self.y2 else -1
        res = [(x, y)]
        for _ in range(abs(self.x1-self.x2)):
            x += x_direction
            y += y_direction
            res.append((x, y))
        return res


class OceanMap:
    def __init__(self):
        self.points = dict()

    def add(self, coordinates):
        if coordinates not in self.points:
            self.points[coordinates] = 1
        else:
            self.points[coordinates] += 1

    def get_dangerous_num(self, level=2):
        return sum(value >= level for value in self.points.values())

    def __str__(self):
        x_max = max([p[0] for p in self.points])
        y_max = max([p[1] for p in self.points])

        res = ''
        for y in range(y_max+1):
            line = ''
            for x in range(x_max+1):
                line += str(self.points[(x, y)]) if (x, y) in self.points else '.'
            res += line + '\n'
        return res


def first_task(file_path):
    data = read_straight_line_data(file_path)
    map = OceanMap()
    for d in data:
        for point in d.get_points():
            map.add(point)
    # print(map)
    return map.get_dangerous_num(level=2)


def read_straight_line_data(file_path):
    with open(file_path) as f:
        return [StraightLineSegment(line.strip()) for line in f.readlines()]


def second_task(file_path):
    data = read_data(file_path)
    map = OceanMap()
    for d in data:
        for point in d.get_points():
            map.add(point)
    # print(map)
    return map.get_dangerous_num(level=2)


def read_data(file_path):
    with open(file_path) as f:
        return [DiagonalLineSegment(line.strip()) for line in f.readlines()]


if __name__ == '__main__':
    FILE_PATH = 'input.txt'
    res_1 = first_task(FILE_PATH)
    print(res_1)
    res_2 = second_task(FILE_PATH)
    print(res_2)
