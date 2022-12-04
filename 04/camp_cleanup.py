with open('data.txt') as f:
    file = f.readlines()
data = [[[int(id) for id in ids.split("-")]
         for ids in line.strip().split(",")] for line in file]


def part_one():
    print("--- part one ---")

    sum = 0
    for ids in data:
        sum += int(((ids[0][0] - ids[1][0]) * (ids[0][1] - ids[1][1])) <= 0)

    print(sum)


def part_two():
    print("--- part two ---")

    sum = 0
    for ids in data:
        sum += int(not (ids[0][0] > ids[1][1] or ids[1][0] > ids[0][1]))

    print(sum)


part_one()
part_two()
