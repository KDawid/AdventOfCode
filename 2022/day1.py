
with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

elves = []
calories = 0
for line in lines:
    if len(line) == 0:
        if calories > 0:
            elves.append(calories)
            calories = 0
    else:
        calories += int(line)

print(max(elves))
print(sum(sorted(elves, reverse=True)[:3]))
