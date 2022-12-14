import numpy as np
import copy

with open("data.txt") as f:
    file = [[np.array([int(c) for c in point.split(",")])
             for point in line.split(" -> ")] for line in f.readlines()]


def append(p, list, y0=0):
    if p[1] < y0:
        for _ in range(y0 - p[1]):
            list.insert(0, [])
        y0 = p[1]
    elif p[1] - y0 >= len(list):
        for _ in range(p[1] - y0 - len(list) + 1):
            list.append([])
    if p[0] not in list[p[1] - y0]:
        list[p[1] - y0].append(p[0])
    return y0


def plot(start, end, list, y0):
    d = end - start
    for dx in range(np.abs(d[0]) + 1):
        for dy in range(np.abs(d[1]) + 1):
            y0 = append(start + [np.sign(d[0]) * dx,
                                 np.sign(d[1]) * dy], list, y0)
    return y0


def drop(sand, abbr, pouring_point=[500, 0]):
    x, y = pouring_point

    while y < len(sand):
        if x not in sand[y]:
            y += 1
        else:
            if x-1 not in sand[y]:
                x -= 1
            elif x+1 not in sand[y]:
                x += 1
            else:
                break

    if abbr(x, y, x0, xn, sand):
        return False

    append([x, y-1], sand)
    return True


def show(stones, sand, y0, x0, xn, pouring=-1):
    for i in range(y0):
        for j in range(xn - x0 + 1):
            if i == 0 and j+x0 == 500:
                print("+", end="")
            elif j+x0 in sand[i]:
                print("o", end="")
            else:
                if j+x0+1 == pouring and j+x0+1 in sand[i]:
                    pouring -= 1
                if j+x0 == pouring:
                    print("~", end="")
                else:
                    print(".", end="")
        print()

    for i, line in enumerate(stones):
        for j in range(xn - x0 + 1):
            if j+x0 in line:
                print("#", end="")
            elif j+x0 in sand[i+y0]:
                print("o", end="")
            else:
                if j+x0+1 == pouring and j+x0+1 in sand[i+y0]:
                    pouring -= 1
                if j+x0 == pouring:
                    print("~", end="")
                else:
                    print(".", end="")
        print()


y0 = file[0][0][1]
stones = [[]]

for line in file:
    for i in range(len(line)-1):
        y0 = plot(line[i], line[i+1], stones, y0)

for line in stones:
    line.sort()

x0 = np.min([line[0] if len(line) > 0 else 500 for line in stones])
xn = np.max([line[-1] if len(line) > 0 else 0 for line in stones])

sand = copy.deepcopy(stones)
for _ in range(y0):
    sand.insert(0, [])


def part_one():

    print("--- part one ---")

    while drop(sand, lambda x, y, x0, xn, list: x < x0 or x > xn or y == len(list)):
        ...

    print(np.sum([len(line) for line in sand]) -
          np.sum([len(line) for line in stones]))
    # show(stones, sand, y0, x0, xn, 500)


def part_two():
    print("--- part two ---")
    stones.append([])
    sand.append([])

    while drop(sand, lambda x, y, x0, xn, list: y == 1):
        ...

    print(np.sum([len(line) for line in sand]) -
          np.sum([len(line) for line in stones]) + 1)
    # show(stones, sand, y0, x0, xn, 499)


part_one()
part_two()
