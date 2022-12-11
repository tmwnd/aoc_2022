import numpy as np

with open("data.txt") as f:
    file = f.readlines()


def get_data():
    data = []
    for i in range(len(file)//7+1):
        i *= 7

        curr = {}
        curr['count'] = 0

        curr['items'] = [int(item) for item in file[i +
                                                    1].strip().replace("Starting items: ", "").split(", ")]

        match file[i+2].strip().replace("Operation: new = old ", "").split(" "):
            case ["+", "old"]: curr['operation'] = lambda x: 2 * x
            case ["*", "old"]: curr['operation'] = lambda x: x**2
            case ["+", n]: curr['operation'] = lambda x, n=n: x + int(n)
            case ["*", n]: curr['operation'] = lambda x, n=n: x * int(n)

        n = int(file[i+3].strip().replace("Test: divisible by ", ""))
        curr['split'] = n
        curr['test'] = lambda x, n=n: x % n == 0

        curr['true'] = int(
            file[i+4].strip().replace("If true: throw to monkey ", ""))
        curr['false'] = int(
            file[i+5].strip().replace("If false: throw to monkey ", ""))

        data.append(curr)
    return data


def part_one():
    print("--- part one ---")

    data = get_data()
    for _ in range(20):
        for monkey in data:
            for _ in range(len(monkey['items'])):
                monkey['count'] += 1
                x = monkey['operation'](monkey['items'].pop(0)) // 3
                data[monkey['true'] if monkey['test'](
                    x) else monkey['false']]['items'].append(x)
    counts = [monkey['count'] for monkey in data]
    counts.sort()
    print(counts[-2] * counts[-1])


def part_two():
    print("--- part two ---")

    data = get_data()

    mod = int(np.prod([monkey['split'] for monkey in data]))
    for i in range(10000):
        for monkey in data:
            for _ in range(len(monkey['items'])):
                monkey['count'] += 1
                x = monkey['operation'](monkey['items'].pop(0)) % mod
                data[monkey['true'] if monkey['test'](
                    x) else monkey['false']]['items'].append(x)
    counts = [monkey['count'] for monkey in data]
    counts.sort()
    print(counts[-2] * counts[-1])


part_one()
part_two()
