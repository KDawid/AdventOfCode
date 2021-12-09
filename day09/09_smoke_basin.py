import numpy as np


def first_task(file_path):
    heightmap = read_data(file_path)
    return get_sum_of_low_points(heightmap)


def read_data(file_path):
    with open(file_path) as f:
        data = [[int(num) for num in line.strip()] for line in f.readlines()]
    return data


def get_sum_of_low_points(heightmap):
    res = 0
    for i in range(len(heightmap)):
        for j in range(len(heightmap[0])):
            if is_local_minimum(heightmap, i, j):
                res += heightmap[i][j] + 1
    return res


def is_local_minimum(heightmap, i, j):
    act_height = heightmap[i][j]
    if 0 < i and heightmap[i-1][j] <= act_height:
        return False
    if i < len(heightmap) - 1 and heightmap[i+1][j] <= act_height:
        return False
    if 0 < j and heightmap[i][j-1] <= act_height:
        return False
    if j < len(heightmap[i]) - 1 and heightmap[i][j+1] <= act_height:
        return False
    return True


def second_task(file_path):
    heightmap = read_data(file_path)
    return get_multiplication_of_largest_basins(heightmap)


def get_multiplication_of_largest_basins(heightmap):
    basin_map = (np.array(heightmap) < 9).astype(int)
    basin_coordinates_dict = create_basin_coordinates_dict(basin_map)
    basin_sizes = get_basin_sizes(basin_coordinates_dict)
    return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]


def create_basin_coordinates_dict(basin_map):
    res = dict()
    used_coordinates = set()
    basin_coordinates = create_basin_coordinates(basin_map)
    for coordinate in basin_coordinates:
        if coordinate not in used_coordinates:
            new_key = len(res)
            res[new_key] = create_basin_set(coordinate, basin_coordinates, used_coordinates)
    return res


def create_basin_coordinates(basin_map):
    x_coord, y_coord = np.nonzero(basin_map == 1)
    return list(zip(list(x_coord), list(y_coord)))


def create_basin_set(coordinate, basin_coordinates, used_coordinates):
    res = set()
    res.add(coordinate)
    used_coordinates.add(coordinate)
    x, y = coordinate
    for new_coord in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        if new_coord in basin_coordinates and new_coord not in used_coordinates:
            res.add(new_coord)
            used_coordinates.add(new_coord)
            res = res.union(create_basin_set(new_coord, basin_coordinates, used_coordinates))
    return res


def get_basin_sizes(basin_coordinates_dict):
    res = []
    for coords in basin_coordinates_dict.values():
        res.append(len(coords))
    return sorted(res, reverse=True)


if __name__ == '__main__':
    FILE_PATH = 'input.txt'
    res_1 = first_task(FILE_PATH)
    print(res_1)
    res_2 = second_task(FILE_PATH)
    print(res_2)
