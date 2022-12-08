import numpy as np

with open("data.txt") as f:
    data = np.array([[int(tree) for tree in line.strip()]
                    for line in f.readlines()])


def is_visible(directions):
    for direction in directions:
        if np.all(direction[:-1] < direction[-1]):
            return True
    return False


def scenic_score(height, directions):
    ret = 1
    for direction in directions:
        for s, d in enumerate(direction):
            if d >= height or s == len(direction)-1:
                ret *= s+1
                break
    return ret


def part_one():
    print("--- part one ---")

    sum = len(data)*2 + len(data[0])*2 - 4
    for i in range(1, len(data)-1):
        for j in range(1, len(data[0])-1):
            directions = [
                data[0:i+1, j],
                data[i:len(data), j][::-1],
                data[i, 0:j+1],
                data[i, j:len(data[0])][::-1]
            ]

            sum += int(is_visible(directions))
    print(sum)


def part_two():
    print("--- part two ---")

    max = 0
    for i in range(1, len(data)-1):
        for j in range(1, len(data[0])-1):
            directions = [
                data[0:i, j][::-1],
                data[i+1:len(data), j],
                data[i, 0:j][::-1],
                data[i, j+1:len(data[0])]
            ]

            max = np.max([max, scenic_score(data[i, j], directions)])
    print(max)


part_one()
part_two()
