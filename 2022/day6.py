_INPUT = """zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"""


if __name__ == '__main__':
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    #lines = _INPUT.split("\n")
    line = lines[0]

    for i in range(4, len(line)):
        if len(set(line[i-4: i])) == 4:
            print(i)
            break
    for i in range(14, len(line)):
        print(line[i-14: i])
        if len(set(line[i-14: i])) == 14:
            print(i)
            break

