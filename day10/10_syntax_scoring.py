class SyntaxStack:
    OPENS = '([{<'
    CLOSES = ')]}>'

    def __init__(self, line):
        self.stack = []
        for item in line:
            self.put(item)

    def is_empty(self):
        return len(self.stack) == 0

    def put(self, item):
        if item in self.OPENS:
            self.stack.append(item)
        elif item in self.CLOSES:
            i = self.CLOSES.index(item)
            if self.stack[-1] == self.OPENS[i]:
                self.stack = self.stack[:-1]
            else:
                raise ValueError(f'Invalid syntax because of {item}')
        else:
            raise IOError(f'Unknown character: {item}')

    def get_completion_chars(self):
        res = ''
        for item in reversed(self.stack):
            i = self.OPENS.index(item)
            res += self.CLOSES[i]
        return res

    def __str__(self):
        return ''.join(self.stack)


def first_task(file_path):
    lines = read_data(file_path)
    illegal_chars = collect_illegal_chars(lines)
    res = score_errors(illegal_chars)
    return res


def read_data(file_path):
    with open(file_path) as f:
        data = [line.strip() for line in f.readlines()]
    return data


def collect_illegal_chars(lines):
    illegal_chars = []
    for line in lines:
        try:
            SyntaxStack(line)
        except ValueError as e:
            illegal_chars.append(str(e)[-1])
    return illegal_chars


def score_errors(illegal_chars):
    res = 0
    for char in illegal_chars:
        if char == ')':
            res += 3
        elif char == ']':
            res += 57
        elif char == '}':
            res += 1197
        elif char == '>':
            res += 25137
    return res


def second_task(file_path):
    lines = read_data(file_path)
    scores = []
    for s in collect_incompletes(lines):
        to_complete = s.get_completion_chars()
        scores.append(get_completion_score(to_complete))
    scores.sort()
    return scores[len(scores) // 2]


def collect_incompletes(lines):
    incompletes = []
    for line in lines:
        try:
            stack = SyntaxStack(line)
            if not stack.is_empty():
                incompletes.append(stack)
            else:
                print('COMPLETE')
        except ValueError:
            pass
    return incompletes


def get_completion_score(to_complete):
    res = 0
    for char in to_complete:
        res *= 5
        if char == ')':
            res += 1
        elif char == ']':
            res += 2
        elif char == '}':
            res += 3
        elif char == '>':
            res += 4
    return res


if __name__ == '__main__':
    FILE_PATH = 'input.txt'
    res_1 = first_task(FILE_PATH)
    print(res_1)
    res_2 = second_task(FILE_PATH)
    print(res_2)
