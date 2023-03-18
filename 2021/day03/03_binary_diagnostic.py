import pandas as pd


def first_task(file_path):
    df = load_data(file_path)
    gamma = get_gamma(df)
    epsilon = 2 ** len(df.columns.values) - gamma - 1
    return gamma * epsilon


def load_data(file_path):
    with open(file_path, 'r') as f:
        data = [line.strip() for line in f.readlines()]
    df = pd.DataFrame(data, columns=['data'])
    return df['data'].apply(lambda x: pd.Series(list(x), dtype=int))


def get_gamma(df):
    mode = df.mode().to_string(header=False,
                               index=False,
                               index_names=False).replace(' ', '')
    return to_decimal(mode)


def to_decimal(binary_string):
    return int(binary_string, 2)


def second_task(file_path):
    df = load_data(file_path)
    ogr = calculate_oxygen_generator_rating(df)
    csr = calculate_co2_scrubber_rating(df)
    return ogr * csr


def calculate_oxygen_generator_rating(df):
    tmp = df.copy(deep=True)
    for column in tmp.columns.values:
        bit = 1
        mode_df = tmp[column].mode()
        if len(mode_df) == 1:
            bit = int(mode_df.to_string(header=False, index=False))
        tmp = tmp[tmp[column] == bit]
        if len(tmp) == 1:
            return to_decimal(tmp.to_string(header=False,
                                            index=False,
                                            index_names=False).replace(' ', ''))


def calculate_co2_scrubber_rating(df):
    tmp = df.copy(deep=True)
    for column in tmp.columns.values:
        bit = 0
        mode_df = tmp[column].mode()
        if len(mode_df) == 1:
            bit = 1 - int(mode_df.to_string(header=False, index=False))
        tmp = tmp[tmp[column] == bit]
        if len(tmp) == 1:
            return to_decimal(tmp.to_string(header=False,
                                            index=False,
                                            index_names=False).replace(' ', ''))


if __name__ == '__main__':
    FILE_PATH = 'input.txt'
    res_1 = first_task(FILE_PATH)
    print(res_1)
    res_2 = second_task(FILE_PATH)
    print(res_2)
