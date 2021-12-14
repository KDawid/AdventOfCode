def add_substr(string_dict, substr, cnt):
    if substr not in string_dict:
        string_dict[substr] = cnt
    else:
        string_dict[substr] += cnt


class InsertionRules:
    def __init__(self, rules):
        self.rules = rules

    def apply_rules(self, string):
        res = string[0]
        for i in range(len(string)-1):
            res += self.rules[string[i:i+2]]
            res += string[i+1]
        return res

    def apply_advanced_rules(self, string_dict):
        res = dict()
        for substr, cnt in string_dict.items():
            new_char = self.rules[substr]
            add_substr(res, substr[0] + new_char, cnt)
            add_substr(res, new_char + substr[1], cnt)
        return res


def first_task(file_path, iter_num=10):
    string, rules = read_data(file_path)
    for _ in range(iter_num):
        string = rules.apply_rules(string)
    res = get_first_task_result(string)
    return res


def read_data(file_path):
    rules = dict()
    with open(file_path) as f:
        start = f.readline().strip()
        f.readline()
        for line in f.readlines():
            from_rule, to_rule = line.strip().split(' -> ')
            rules[from_rule] = to_rule
    return start, InsertionRules(rules)


def get_first_task_result(string):
    counts = {e: string.count(e) for e in set(string)}
    return max(counts.values()) - min(counts.values())


def second_task(file_path, iter_num=40):
    string, rules = read_data(file_path)
    string_dict = create_string_dict(string)
    for _ in range(iter_num):
        string_dict = rules.apply_advanced_rules(string_dict)
    res = get_second_task_result(string_dict)
    return res


def create_string_dict(string):
    res = dict()
    for i in range(len(string)-1):
        substr = string[i:i+2]
        if substr not in res:
            res[substr] = 1
        else:
            res[substr] += 1
    return res


def get_second_task_result(string_dict):
    char_counts = dict()
    for substr, cnt in string_dict.items():
        add_substr(char_counts, substr[0], cnt)
        add_substr(char_counts, substr[1], cnt)
    char_counts = normalize_char_counts(char_counts)
    return max(char_counts.values()) - min(char_counts.values())


def normalize_char_counts(char_counts):
    res = dict()
    for char, cnt in char_counts.items():
        if cnt % 2 == 0:
            res[char] = cnt // 2
        else:
            res[char] = cnt // 2 + 1
    return res


if __name__ == '__main__':
    FILE_PATH = 'input.txt'
    res_1 = first_task(FILE_PATH, iter_num=10)
    print(res_1)
    res_2 = second_task(FILE_PATH, iter_num=40)
    print(res_2)
