HEX_TO_BIN = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}

BIN_TO_HEX = {h: b for (b, h) in HEX_TO_BIN.items()}


def first_task(file_path):
    hex_string = read_data(file_path)
    hex_string = '38006F45291200'
    print(hex_string)
    binary = to_binary(hex_string)
    print(binary)
    res = calculate_result(binary, 0)
    print(res)
    return res


def calculate_result(binary, res):
    if len(binary) < 6:
        return res
    version = get_binary_value(binary[:3])
    res += version
    type_id = get_binary_value(binary[3:6])
    if type_id == 4:
        # res.append(get_literal_result(binary[6:], step=5))
        pass
    len_type_id = int(binary[6])
    data = binary[7:]
    if len_type_id == 0:
        sub_packages_len = int(data[:15], 2)
        for d in break_data(data[15:15+sub_packages_len]):
            calculate_result(d, res)
    elif len_type_id == 1:
        num_packets = int(data[:11], 2)
        data = data[11:]
        index = 0
        for _ in range(num_packets):
            print(data[index+3:index+6])
            if data[index+3:index+6] == '100':
                print('literal')
            index += 11
            #from_index = 11 * (i + 1)
            #to_index = 11 * (i + 2)
            #calculate_result(data[from_index:to_index], res)
    return res


def break_data(data):
    res = []
    start_id = 0
    print('BREAKING')
    if int(data[3:6], 2) == 4:
        print('PARSE LITERAL')
        i = 0
        while i < len(data)-6 and data[i+6] == 1:
            i += 5
        end_index = i + 5
        res.append((start_id, end_index+6))
    elif int(data[6]) == 1:
        print('PARSE FIX NUMBER')
    elif int(data[6]) == 0:
        print('PARSE FIX LENGTH')

    print(data)
    return res


def get_broken_part(data):
    start_index = 0
    if int(data[3:6], 2) == 4:
        print('PARSE LITERAL')
        i = 0
        while i < len(data)-6 and data[i+6] == 1:
            i += 5
        end_index = i + 5
        return (start_index, end_index+6), end_index+7
    elif int(data[6]) == 1:
        print('PARSE FIX NUMBER')
    elif int(data[6]) == 0:
        print('PARSE FIX LENGTH')



def read_data(file_path):
    with open(file_path) as f:
        return f.readline().strip()


def to_binary(hex_string):
    res = ''
    for c in hex_string:
        res += HEX_TO_BIN[c]
    return res


def get_binary_value(c):
    return int(c, 2)


def get_literal_result(data, step):
    res = ''
    i = 0
    while data[i] == '1':
        res += data[i+1:i+step]
        i += step
    res += data[i + 1:i + step]
    return int(res, 2)


def get_operator_result_with_fixed_packet_size(data):
    res = ''
    num_packets = int(data[:11], 2)
    print(num_packets)
    print(data)
    for i in range(num_packets):
        from_index = 11 * i
        to_index = 11 * (i + 1)
        print(from_index, to_index, data[from_index: to_index], int(data[from_index: to_index], 2))
        res += data[from_index: to_index]
    print('------------------')
    print(res)
    return int(res, 2)


if __name__ == '__main__':
    FILE_PATH = 'input_demo3.txt'
    res_1 = first_task(FILE_PATH)
    print(res_1)
    #res_2 = second_task(FILE_PATH)
    #print(res_2)
