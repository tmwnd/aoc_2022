import copy

with open("data.txt") as f:
    jets = [-1 if c == "<" else 1 for c in f.readline()]


def to_string(data):
    for line in data:
        for c in line:
            print("." if c == 0 else "#", end="")
        print()


rocks = [
    [[1, 1, 1, 1]],
    [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
    [[0, 0, 1], [0, 0, 1], [1, 1, 1]],
    [[1], [1], [1], [1]],
    [[1, 1], [1, 1]]
]


def get_estimator(dh):
    for i in range(1, len(dh))[::-1]:
        dh[i] -= dh[i-1]

    for l in range(25, len(dh)//2):
        cycle = dh[-l:]

        if cycle == dh[-2*l:-l]:
            return [dh[:len(dh) % l], cycle]


def simulate_n_rocks(n, estimate=False, estimate_n=0):
    data = [[0 for _ in range(7)] for _ in range(3)]

    def is_invalid(lines, rock, x, dx=0):
        for i, line in enumerate(rock[::-1]):
            for j, c in enumerate(line):
                lines[-i-1][x+dx+j] += c

        return any([any([c > 1 for c in line]) for line in lines])

    def get_f(f=0):
        for line in data:
            if any([c == 1 for c in line]):
                break
            f += 1
        return f

    jet_ptr = 0
    dh = []
    for t in range(n):
        rock = rocks[t % len(rocks)]

        x = 2
        y = len(rock) - 1

        f = get_f(f=-3)

        for _ in range(f - len(rock)):
            data.pop(0)
        for _ in range(len(rock) - f):
            data.insert(0, [0 for _ in range(7)])

        while y < len(data):
            if is_invalid(copy.deepcopy(data[y-len(rock)+1:y+1]), rock, x):
                break

            jet = jets[jet_ptr % len(jets)]
            jet_ptr += 1

            if x + len(rock[0]) + jet <= len(data[0]) and x + jet >= 0:
                if not is_invalid(copy.deepcopy(data[y-len(rock)+1:y+1]), rock, x, dx=jet):
                    x += jet

            y += 1

        for i, line in enumerate(rock[::-1]):
            for j, c in enumerate(line):
                data[y-i-1][x+j] += c

        if estimate:
            dh.append(len(data) - get_f())

    if estimate:
        base, cycle = get_estimator(dh)
        estimate_n -= len(base)
        return sum(base) + sum(cycle) * (estimate_n // len(cycle)) + sum(cycle[:estimate_n % len(cycle)])
    else:
        return len(data) - get_f()


def part_one():
    print("--- part one ---")
    print(simulate_n_rocks(2022))


def part_two():
    print("--- part two ---")
    print(simulate_n_rocks(10000, estimate=True, estimate_n=1000000000000))


part_one()
part_two()
