import numpy as np

with open("data.txt") as f:
    data = [[int(x) for x in line.strip().split(",")]
            for line in f.readlines()]


def get_d(list):
    d = []
    for cube in list:
        curr = []
        for v in list:
            curr.append(np.sum(np.abs(cube - v)))
        d.append(curr)
    return d


def surface(list):
    return np.sum([6 - np.sum([int(x == 1) for x in line]) for line in get_d(np.array(list))])


def part_one():
    print("--- part one ---")
    print(surface(data))


def part_two():
    print("--- part two ---")

    xmin, ymin, zmin = np.min(np.array(data), axis=0)
    xmax, ymax, zmax = np.max(np.array(data), axis=0)

    queue = [[xmin-1, ymin-1, zmin-1]]
    while len(queue) > 0:
        v = queue.pop()
        for dv in np.array([[-1, 0, 0], [0, -1, 0], [0, 0, -1], [1, 0, 0], [0, 1, 0], [0, 0, 1]]):
            dv += v
            if any(dv <= [xmin-2, ymin-2, zmin-2]) or any(dv >= [xmax+2, ymax+2, zmax+2]) or any([all(dv == cube) for cube in data]):
                continue
            data.append(list(dv))
            queue.append(dv)

    air = []
    for x in range(xmin+1, xmax):
        for y in range(ymin+1, ymax):
            for z in range(zmin+1, zmax):
                if any([all(np.array([x, y, z]) == cube) for cube in data]):
                    continue
                if all([cube[0] >= x for cube in data if cube[1] == y and cube[2] == z]) or all([cube[0] <= x for cube in data if cube[1] == y and cube[2] == z]):
                    continue
                if all([cube[1] >= y for cube in data if cube[0] == x and cube[2] == z]) or all([cube[1] <= y for cube in data if cube[0] == x and cube[2] == z]):
                    continue
                if all([cube[2] >= z for cube in data if cube[0] == x and cube[1] == y]) or all([cube[2] <= z for cube in data if cube[0] == x and cube[1] == y]):
                    continue
                air.append([x, y, z])

    print(surface(data) - surface(air))


part_one()
part_two()
