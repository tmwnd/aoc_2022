import numpy as np

with open("data.txt") as f:
    file = [line.strip() for line in f.readlines()]

data = []
for x, line in enumerate(file):
    for y, c in enumerate(line):
        if c == "#": data.append((x, y))


def eq(a, b):
    for i in range(len(a)):
        if a[i] != b[i]: return False
    return True


def op_add(a, b):
    return tuple([a[i] + b[i] for i in range(len(a))])


def to_string(data):
    for x in range(min([elf[0] for elf in data]), max([elf[0] for elf in data]) + 1):
        for y in range(min([elf[1] for elf in data]), max([elf[1] for elf in data]) + 1):
            if any([eq(elf, (x, y)) for elf in data]): print("#", end="")
            else: print(".", end="")
        print()


# NW, N, NE, E, SE, S, SW, W, NW
directions = [
    (-1, -1), (-1, 0), (-1, 1),
    (1, 1), (1, 0), (1, -1),
    (1, -1), (0, -1), (-1, -1),
    (-1, 1), (0, 1), (1, 1),
]


def simulate_elves(elves, rounds=10, stop_on_idle=False):
    global directions

    round = 0
    while True:
        if round == rounds and not stop_on_idle: break

        data_unique = set(data)
        proposes_unique = set()
        proposes = []

        for elf in data:
            is_valid = []
            for direction in directions:
                is_valid.append(not op_add(elf, direction) in data_unique)

            if all(is_valid):
                proposes.append(None)
                continue
            elif all(is_valid[:3]): value = op_add(elf, directions[1])
            elif all(is_valid[3:6]): value = op_add(elf, directions[4])
            elif all(is_valid[6:9]): value = op_add(elf, directions[7])
            elif all(is_valid[9:12]): value = op_add(elf, directions[10])
            else:
                proposes.append(None)
                continue

            if value in proposes_unique:
                for i in range(len(proposes))[::-1]:
                    if proposes[i] is None: continue
                    if eq(proposes[i], value): proposes[i] = None
                proposes.append(None)
            else:
                proposes_unique.add(value)
                proposes.append(value)

        if stop_on_idle and len(proposes_unique) == 0: return round + 1

        for i in range(len(data)):
            if proposes[i] is None: continue
            data[i] = proposes[i]

        directions = directions[3:] + directions[0:3]
        round += 1

    # to_string(data)
    return (max([elf[0] for elf in data]) + 1 - min([elf[0] for elf in data])) * (max([elf[1] for elf in data]) + 1 - min([elf[1] for elf in data])) - len(data)


def part_one():
    print("--- part one ---")
    print(simulate_elves(data))


def part_two():
    print("--- part two ---")
    print(10 + simulate_elves(data, stop_on_idle=True))


part_one()
part_two()
