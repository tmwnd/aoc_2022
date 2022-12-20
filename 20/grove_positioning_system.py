import numpy as np

with open("data.txt") as f:
    data = [{
        'value': int(line.strip()),
        'index': i
    } for i, line in enumerate(f.readlines())]


def sort_n_times(data, n=1):
    sorted = data.copy()
    for _ in range(n):
        for i, x in enumerate(data):
            j = sorted.index(x)
            sorted.remove(x)
            sorted.insert((j + x['value']) % len(sorted), x)

    for i in range(len(sorted)):
        if sorted[i]['value'] == 0:
            index_of_zero = i
            break

    return (sum([sorted[i % len(sorted)]['value'] for i in [index_of_zero + i * 1000 for i in range(1, 4)]]))


def part_one():
    print("--- part one ---")
    print(sort_n_times(data))


def part_two():
    print("--- part two ---")

    decrypted_data = [{
        'value': x['value'] * 811589153,
        'index': x['index']
    } for x in data]
    print(sort_n_times(decrypted_data, n=10))


part_one()
part_two()
