def first_task(file_path):
    data = read_numbers(file_path)
    increased_num = get_number_on_increased(data)
    return increased_num


def read_numbers(file_path):
    with open(file_path) as f:
        data = [int(line.strip()) for line in f.readlines()]
    return data


def get_number_on_increased(data):
    res = 0
    for i in range(len(data)-1):
        if data[i] < data[i+1]:
            res += 1
    return res


def second_task(file_path):
    data = read_numbers(file_path)
    refined_data = aggregate_data(data, window_size=3)
    increased_num = get_number_on_increased(refined_data)
    return increased_num


def aggregate_data(data, window_size=3):
    res = []
    for i in range(len(data)-window_size+1):
        res.append(sum(data[i:i+window_size]))
    return res


if __name__ == '__main__':
    FILE_PATH = 'input.txt'
    res_1 = first_task(FILE_PATH)
    print(res_1)
    res_2 = second_task(FILE_PATH)
    print(res_2)
