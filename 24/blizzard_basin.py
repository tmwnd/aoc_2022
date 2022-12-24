with open("data.txt") as f:
    file = [line.strip() for line in f.readlines()]

XMIN = 0
XMAX = len(file) - 2
YMIN = 0
YMAX = len(file[0]) - 2

blizzards = []
blizzard_movings = []

for i, line in enumerate(file[1:-1]):
    for j, c in enumerate(line[1:-1]):
        if c == ".": continue

        blizzards.append((i, j))
        match c:
            case '^': blizzard_movings.append((-1, 0))
            case 'v': blizzard_movings.append((1, 0))
            case '<': blizzard_movings.append((0, -1))
            case '>': blizzard_movings.append((0, 1))


def op_add(a, b):
    return tuple([a[i] + b[i] for i in range(len(a))])


def op_add_inplace(a, b, min=[XMIN, YMIN], max=[XMAX, YMAX]):
    def scale_to_min_max_interval(value, j):
        if value >= max[j]: return 0
        if value < min[j]: return max[j] - 1
        return value

    for i in range(len(a)): a[i] = tuple([scale_to_min_max_interval(a[i][j] + b[i][j], j) for j in range(len(a[i]))])


def to_string(blizzards, blizzard_movings, player=(-1, 1)):
    def hline(space=-1):
        for y in range(YMIN, YMAX + 2):
            print("#" if y != space else "E" if player == (-1, y) else ".", end="")
        print()

    hline(1)
    for x in range(XMIN, XMAX):
        print("#", end="")
        for y in range(YMIN, YMAX):
            cnt = 0
            if player == (x, y):
                print("E", end="")
                continue
            for i, blizzard in enumerate(blizzards):
                if (x, y) == blizzard:
                    match blizzard_movings[i]:
                        case (-1, 0): c = '^'
                        case (1, 0): c = 'v'
                        case (0, -1): c = '<'
                        case (0, 1): c = '>'
                    cnt += 1
            if cnt == 0: print(".", end="")
            elif cnt == 1: print(c, end="")
            else: print(cnt, end="")
        print("#")
    hline(YMAX)


def simulate_blizzards(blizzards, blizzard_movings, start=(-1, 0), target=(XMAX, YMAX - 1)):
    minute = 0

    queue = {start}
    while True:
        op_add_inplace(blizzards, blizzard_movings)

        queue_options = set()
        for q in queue:
            for d in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
                option = op_add(q, d)
                if option == target: return minute + 1
                if XMIN <= option[0] < XMAX and YMIN <= option[1] < YMAX and option not in blizzards or option == start:
                    queue_options.add(option)
        queue = queue_options

        # to_string(blizzards, blizzard_movings)

        if len(queue) == 0:
            break
        minute += 1


def part_one():
    global ONE
    print("--- part one ---")

    ONE = simulate_blizzards(blizzards, blizzard_movings)
    print(ONE)


def part_two():
    print("--- part two ---")

    print(ONE + simulate_blizzards(blizzards, blizzard_movings, start=(XMAX, YMAX - 1), target=(-1, 0)) + simulate_blizzards(blizzards, blizzard_movings))


part_one()
part_two()
