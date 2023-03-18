class DigitGuesser:
    # length --> digit
    EASY_DIGIT_SEGMENTS = {
        2: 1,
        4: 4,
        3: 7,
        7: 8
    }

    def __init__(self, data):
        self.digits = dict()
        self.__fill_digits(data)

    def __fill_digits(self, digits):
        self.__update_digits_with_trivials(digits)
        self.__update_five_length_digits([digit for digit in digits if len(digit) == 5])
        self.__update_six_length_digits([digit for digit in digits if len(digit) == 6])
        # print(self.digits)

    def __update_digits_with_trivials(self, digits):
        for digit in digits:
            sections = set(digit)
            if len(sections) == 2:
                self.digits[1] = sections
            elif len(sections) == 3:
                self.digits[7] = sections
            elif len(sections) == 4:
                self.digits[4] = sections
            elif len(sections) == 7:
                self.digits[8] = sections

    def __update_five_length_digits(self, digits):
        for digit in digits:
            sections = set(digit)
            if len(self.digits[4].intersection(sections)) == 2:
                self.digits[2] = sections
            elif len(self.digits[1].intersection(sections)) == 2:
                self.digits[3] = sections
            elif len(self.digits[1].intersection(sections)) == 1 and len(self.digits[4].intersection(sections)) == 3:
                self.digits[5] = sections
            else:
                raise ValueError(f'Could not parse {sections}')

    def __update_six_length_digits(self, digits):
        for digit in digits:
            sections = set(digit)
            if len(self.digits[3].intersection(sections)) == 5:
                self.digits[9] = sections
            elif len(self.digits[5].intersection(sections)) == 4:
                self.digits[0] = sections
            elif len(self.digits[1].intersection(sections)) == 1:
                self.digits[6] = sections
            else:
                raise ValueError(f'Could not parse {sections}')

    def guess_digit(self, digits):
        res = ''
        for digit in digits:
            segments = set(digit)
            number = list(self.digits.keys())[list(self.digits.values()).index(segments)]
            res += str(number)
        return int(res)


def first_task(file_path):
    _, after_sep = read_digit_codes(file_path)
    return naive_count_of_digits(after_sep)


def naive_count_of_digits(data):
    res = 0
    for signals in data:
        for signal in signals:
            if len(signal) in DigitGuesser.EASY_DIGIT_SEGMENTS:
                res += 1
    return res


def read_digit_codes(file_path):
    SEPARATOR = '|'
    with open(file_path) as f:
        data = [line.strip().split(' ') for line in f.readlines()]
    before, after = [line[:line.index(SEPARATOR)] for line in data], [line[line.index(SEPARATOR)+1:] for line in data]
    return before, after


def second_task(file_path):
    before_sep, after_sep = read_digit_codes(file_path)
    res = 0
    for i in range(len(before_sep)):
        digit_guesser = DigitGuesser(before_sep[i])
        res += digit_guesser.guess_digit(after_sep[i])
    return res


if __name__ == '__main__':
    FILE_PATH = 'input.txt'
    res_1 = first_task(FILE_PATH)
    print(res_1)
    res_2 = second_task(FILE_PATH)
    print(res_2)
