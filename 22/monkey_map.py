with open("data.txt") as f:
    file = [line.rstrip() for line in f.readlines()]


def make_tile(x, y, is_wall, region="map"):
    return {
        'x': x,
        'y': y,
        'is_wall': is_wall,
        'n': None,
        'o': None,
        's': None,
        'w': None,
        'region': region,
        'direction': None
    }


def rotation(region_from, region_to, default):
    match [region_from, region_to]:
        case ["front", "top"]:
            return 0
        case ["front", "left"]:
            return 0
        case ["right", "back"]:
            return 2
        case ["right", "bottom"]:
            return 2
        case ["back", "right"]:
            return 2
        case ["back", "top"]:
            return 2
        case ["left", "bottom"]:
            return 0
        case ["left", "front"]:
            return 0
        case ["top", "back"]:
            return 3
        case ["top", "front"]:
            return 1
        case ["bottom", "right"]:
            return 3
        case ["bottom", "left"]:
            return 1

    return default


def to_string(map):
    for line in map:
        for tile in line:
            if tile is None: print(" ", end="")
            elif tile['is_wall']: print("#", end="")
            elif tile['direction'] is not None:
                match tile['direction']:
                    case "o": print(">", end="")
                    case "s": print("v", end="")
                    case "w": print("<", end="")
                    case "n": print("^", end="")
            else: print(".", end="")
        print()


map = []
for i, line in enumerate(file):
    if line == "": break

    curr = []
    for j, tile in enumerate(line):
        if tile == ".":
            curr.append(make_tile(i, j, False))
        elif tile == "#":
            curr.append(make_tile(i, j, True))
        else:
            curr.append(None)
    map.append(curr)

instructions = file[i + 1].replace("R", ",R,").replace("L", ",L,").split(",")
for i in range(len(instructions) // 2 + 1):
    instructions[i * 2] = int(instructions[i * 2])

for i, line in enumerate(map):
    for j, tile in enumerate(line):
        if tile is None or tile['is_wall']: continue

        di = 0
        while True:
            di += 1
            x = i - di
            if j > len(map[x]) - 1 or map[x][j] is None: continue
            if map[x][j]['is_wall']: break

            tile['n'] = map[x][j]
            break

        dj = 0
        while True:
            dj += 1
            y = (j + dj) % len(line)
            if map[i][y] is None: continue
            if map[i][y]['is_wall']: break

            tile['o'] = map[i][y]
            break

        di = 0
        while True:
            di += 1
            x = (i + di) % len(map)
            if j > len(map[x]) - 1 or map[x][j] is None: continue
            if map[x][j]['is_wall']: break

            tile['s'] = map[x][j]
            break

        dj = 0
        while True:
            dj += 1
            y = j - dj
            if map[i][y] is None: continue
            if map[i][y]['is_wall']: break

            tile['w'] = map[i][y]
            break

cube_size = 50

front = []
for line in map[0:cube_size]:
    curr = []
    for tile in line[cube_size:2 * cube_size]:
        curr.append(make_tile(tile['x'], tile['y'], tile['is_wall'], "front"))
    front.append(curr)

right = []
for line in map[0:cube_size]:
    curr = []
    for tile in line[2 * cube_size:3 * cube_size]:
        curr.append(make_tile(tile['x'], tile['y'], tile['is_wall'], "right"))
    right.append(curr)

back = []
for line in map[2 * cube_size:3 * cube_size]:
    curr = []
    for tile in line[cube_size:2 * cube_size]:
        curr.append(make_tile(tile['x'], tile['y'], tile['is_wall'], "back"))
    back.append(curr)

left = []
for line in map[2 * cube_size:3 * cube_size]:
    curr = []
    for tile in line[0:cube_size]:
        curr.append(make_tile(tile['x'], tile['y'], tile['is_wall'], "left"))
    left.append(curr)

top = []
for line in map[3 * cube_size:4 * cube_size]:
    curr = []
    for tile in line[0:cube_size]:
        curr.append(make_tile(tile['x'], tile['y'], tile['is_wall'], "top"))
    top.append(curr)

bottom = []
for line in map[cube_size:2 * cube_size]:
    curr = []
    for tile in line[cube_size:2 * cube_size]:
        curr.append(make_tile(tile['x'], tile['y'], tile['is_wall'], "bottom"))
    bottom.append(curr)

for i, line in enumerate(front):
    for j, tile in enumerate(line):
        if tile is None or tile['is_wall']: continue

        if i > 0: tile['n'] = front[i - 1][j]
        else: tile['n'] = top[j][0]

        if j < cube_size - 1: tile['o'] = line[j + 1]
        else: tile['o'] = right[i][0]

        if i < cube_size - 1: tile['s'] = front[i + 1][j]
        else: tile['s'] = bottom[0][j]

        if j > 0: tile['w'] = line[j - 1]
        else: tile['w'] = left[-i - 1][0]

for i, line in enumerate(right):
    for j, tile in enumerate(line):
        if tile is None or tile['is_wall']: continue

        if i > 0: tile['n'] = right[i - 1][j]
        else: tile['n'] = top[-1][j]

        if j < cube_size - 1: tile['o'] = line[j + 1]
        else: tile['o'] = back[-i - 1][-1]

        if i < cube_size - 1: tile['s'] = right[i + 1][j]
        else: tile['s'] = bottom[j][-1]

        if j > 0: tile['w'] = line[j - 1]
        else: tile['w'] = front[i][-1]

for i, line in enumerate(back):
    for j, tile in enumerate(line):
        if tile is None or tile['is_wall']: continue

        if i > 0: tile['n'] = back[i - 1][j]
        else: tile['n'] = bottom[-1][j]

        if j < cube_size - 1: tile['o'] = line[j + 1]
        else: tile['o'] = right[-i - 1][-1]

        if i < cube_size - 1: tile['s'] = back[i + 1][j]
        else: tile['s'] = top[j][-1]

        if j > 0: tile['w'] = line[j - 1]
        else: tile['w'] = left[i][-1]

for i, line in enumerate(left):
    for j, tile in enumerate(line):
        if tile is None or tile['is_wall']: continue

        if i > 0: tile['n'] = left[i - 1][j]
        else: tile['n'] = bottom[j][0]

        if j < cube_size - 1: tile['o'] = line[j + 1]
        else: tile['o'] = back[i][0]

        if i < cube_size - 1: tile['s'] = left[i + 1][j]
        else: tile['s'] = top[0][j]

        if j > 0: tile['w'] = line[j - 1]
        else: tile['w'] = front[-i - 1][0]

for i, line in enumerate(top):
    for j, tile in enumerate(line):
        if tile is None or tile['is_wall']: continue

        if i > 0: tile['n'] = top[i - 1][j]
        else: tile['n'] = left[-1][j]

        if j < cube_size - 1: tile['o'] = line[j + 1]
        else: tile['o'] = back[-1][i]

        if i < cube_size - 1: tile['s'] = top[i + 1][j]
        else: tile['s'] = right[0][j]

        if j > 0: tile['w'] = line[j - 1]
        else: tile['w'] = front[0][i]

for i, line in enumerate(bottom):
    for j, tile in enumerate(line):
        if tile is None or tile['is_wall']: continue

        if i > 0: tile['n'] = bottom[i - 1][j]
        else: tile['n'] = front[-1][j]

        if j < cube_size - 1: tile['o'] = line[j + 1]
        else: tile['o'] = right[-1][i]

        if i < cube_size - 1: tile['s'] = bottom[i + 1][j]
        else: tile['s'] = back[0][j]

        if j > 0: tile['w'] = line[j - 1]
        else: tile['w'] = left[0][i]

full_map = []
for i in range(cube_size):
    curr = []
    for _ in range(cube_size): curr.append(None)
    curr.extend(front[i])
    curr.extend(right[i])
    full_map.append(curr)
for i in range(cube_size):
    curr = []
    for _ in range(cube_size): curr.append(None)
    curr.extend(bottom[i])
    for _ in range(cube_size): curr.append(None)
    full_map.append(curr)
for i in range(cube_size):
    curr = []
    curr.extend(left[i])
    curr.extend(back[i])
    for _ in range(cube_size): curr.append(None)
    full_map.append(curr)
for i in range(cube_size):
    curr = []
    curr.extend(top[i])
    for _ in range(cube_size): curr.append(None)
    for _ in range(cube_size): curr.append(None)
    full_map.append(curr)


def move(ptr):
    facing_directions = {
        0: "o",
        1: "s",
        2: "w",
        3: "n",
    }

    facing = 0
    ptr['player'] = True

    for i, instruction in enumerate(instructions):

        if i % 2 == 0:
            for _ in range(instruction):
                direction = facing_directions[facing]

                ptr['direction'] = direction
                if ptr[direction] is None or ptr[direction]['is_wall']: break

                region_from = ptr['region']
                ptr = ptr[direction]
                region_to = ptr['region']

                facing = rotation(region_from, region_to, facing)
        else:
            match instruction:
                case "L": facing = facing - 1 if facing > 0 else len(facing_directions) - 1
                case "R": facing = (facing + 1) % len(facing_directions)

    # to_string(full_map)
    return (ptr['x'] + 1) * 1000 + (ptr['y'] + 1) * 4 + facing


def part_one():
    print("--- part one ---")

    for tile in map[0]:
        if tile is not None and not tile['is_wall']:
            print(move(tile))
            break


def part_two():
    print("--- part two ---")

    for tile in front[0]:
        if tile is not None and not tile['is_wall']:
            print(move(tile))
            break


part_one()
part_two()
