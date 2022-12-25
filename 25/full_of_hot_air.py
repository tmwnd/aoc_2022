with open("data.txt") as f:
    file = [line.strip() for line in f.readlines()]


def SNAFU_to_int(s):
    dict = {
        '=': -2,
        '-': -1,
        '0': 0,
        '1': 1,
        '2': 2
    }

    return sum([5**i * dict[x] for i, x in enumerate(s[::-1])])


def int_to_SNAFU(i):
    dict = {
        -2: "=",
        -1: "-",
        0: "0",
        1: "1",
        2: "2"
    }

    s = []
    while i > 0:
        s.insert(0, i % 5)
        i = i // 5

    for i in range(1, len(s))[::-1]:
        if s[i] >= 3:
            s[i] = -5 + s[i]
            s[i - 1] += 1

    ret = ""
    for x in s:
        ret += dict[x]
    return ret


def part_one():
    print("--- part one ---")
    print(int_to_SNAFU(sum([SNAFU_to_int(s) for s in file])))


part_one()
