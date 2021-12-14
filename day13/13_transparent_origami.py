class Fold:
    UP = 'y'
    LEFT = 'x'

    def __init__(self, axes, coord):
        self.axes = axes
        self.coord = coord

    def __str__(self):
        return f'fold along {self.axes}={self.coord}'


class Paper:
    def __init__(self, dots):
        self.dots = set(dots)
        self.__update_maxes()

    def __update_maxes(self):
        self.max_x = self.__get_max_x()
        self.max_y = self.__get_max_y()

    def __get_max_x(self):
        return self.__get_max(axes=0)

    def __get_max_y(self):
        return self.__get_max(axes=1)

    def __get_max(self, axes):
        res = -1
        for dot in self.dots:
            if dot[axes] > res:
                res = dot[axes]
        return res

    def fold(self, fold: Fold):
        if fold.axes == Fold.UP:
            new_dots = self.__create_folded_dots(fold.coord, axes=1)
        elif fold.axes == Fold.LEFT:
            new_dots = self.__create_folded_dots(fold.coord, axes=0)
        else:
            raise ValueError(f'Unknown axes to fold: {fold.axes}')
        self.dots = new_dots
        self.__update_maxes()

    def __create_folded_dots(self, coord, axes):
        res = set()
        for dot in self.dots:
            if dot[axes] < coord:
                res.add(dot)
            else:
                new_dot = list(dot)
                a = new_dot[axes] - coord
                new_dot[axes] = new_dot[axes] - 2*a
                res.add((new_dot[0], new_dot[1]))
        return res

    def get_number_of_dots(self):
        return len(self.dots)

    def __str__(self):
        res = ''
        for y in range(self.max_y+1):
            line = ''
            for x in range(self.max_x+1):
                line += '#' if (x, y) in self.dots else '.'
            res += line + '\n'
        return res


def first_task(file_path):
    dots, folds = read_data(file_path)
    paper = Paper(dots)
    paper.fold(folds[0])
    return paper.get_number_of_dots()


def read_data(file_path):
    dots, folds = [], []
    with open(file_path) as f:
        for line in f.readlines():
            if ',' in line:
                coords = [int(coord) for coord in line.strip().split(',')]
                dots.append((coords[0], coords[1]))
            elif 'fold along ' in line:
                folding = line.strip()[11:]
                axes, coord = folding.split('=')
                folds.append(Fold(axes, int(coord)))
    return dots, folds


def second_task(file_path):
    dots, folds = read_data(file_path)
    paper = Paper(dots)
    for fold in folds:
        paper.fold(fold)
    print(paper)
    return paper.get_number_of_dots()


if __name__ == '__main__':
    FILE_PATH = 'input.txt'
    res_1 = first_task(FILE_PATH)
    print(res_1)
    res_2 = second_task(FILE_PATH)
    print(res_2)
