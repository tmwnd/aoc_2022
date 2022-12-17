import numpy as np

with open("data.txt") as f:
    file = [line.strip().replace("Valve ", "").replace(" has flow rate=", ", ").replace(
        "; tunnels lead to valves ", ", ").replace("; tunnel leads to valve ", ", ").split(", ") for line in f.readlines()]


def make_valve(name, pressure, index):
    return {
        'name': name,
        'index': i,
        'open': False,
        'pressure': int(pressure),
        'neighbors': []
    }


valves = []
for i, line in enumerate(file):
    valves.append(make_valve(*line[:2], i))

for i, line in enumerate(file):
    for valve in valves:
        if valve['name'] in line[2:]:
            valves[i]['neighbors'].append(valve)


pipes = []
for i, valve in enumerate(valves):
    pipes.append([0 if i == j else 1 if p in valve['neighbors']
                  else np.inf for j, p in enumerate(valves)])

for i in range(len(pipes)):
    for j in range(len(pipes)):
        for k in range(len(pipes)):
            pipes[j][k] = np.min([pipes[j][k], pipes[j][i] + pipes[i][k]])

for i in range(len(pipes)):
    pipes[i] = [int(p) for p in pipes[i]]


def max_pressure(ptr, t):
    if t <= 1:
        return 0

    ptr['open'] = True
    pressures = [ptr['pressure'] * t]

    for valve in valves:
        if valve['open'] or valve['pressure'] == 0:
            continue

        pressures.append(
            pressures[0] + max_pressure(valve, t-1-pipes[ptr['index']][valve['index']]))

    ptr['open'] = False

    return np.max(pressures)


def get_options():
    return [valve for valve in valves if not valve['open'] and valve['pressure'] > 0]


def get_permutation(list):
    a = []
    b = []
    for s in range(2**(len(list)+1)):
        s = [bool(s & (1 << n)) for n in range(len(list))[::-1]]
        if np.sum(s) == len(list) // 2:
            a.append([list[i] for i in range(len(list)) if s[i]])
            b.append([list[i] for i in range(len(list)) if not s[i]])
    return [a, b]


def max_pressure_with_stupid_elephant(ptr, ptr_moves, elephant, elephant_moves, pressure, t):
    #     if all(valve['open'] or valve['pressure'] == 0 for valve in valves):
    #         return t * pressure + (t-1-ptr_moves) * ptr['pressure'] + (t-1-elephant_moves) * elephant['pressure']

    #     if t <= 0:
    #         return 0

    #     new_ptr = ptr_moves == -1
    #     new_elephant = elephant_moves == -1

    #     if not new_ptr and not new_elephant:
    #         skip = np.min([ptr_moves, elephant_moves, t-1])+1
    #         return pressure*skip + max_pressure_with_stupid_elephant(ptr, ptr_moves-skip, elephant, elephant_moves-skip, pressure, t-skip)

    #     if new_ptr:
    #         pressure += ptr['pressure']
    #     if new_elephant:
    #         pressure += elephant['pressure']

    #     max = [0]
    #     for ptr_option in get_options() if new_ptr else [ptr]:
    #         for elephant_option in get_options() if new_elephant else [elephant]:
    #             if ptr_option == elephant_option:
    #                 continue

    #             ptr_option['open'] = True
    #             elephant_option['open'] = True

    #             if new_ptr:
    #                 ptr_moves = pipes[ptr['index']][ptr_option['index']]
    #             if new_elephant:
    #                 elephant_moves = pipes[elephant['index']
    #                                        ][elephant_option['index']]

    #             max.append(max_pressure_with_stupid_elephant(
    #                 ptr_option, ptr_moves-1, elephant_option, elephant_moves-1, pressure, t-1))

    #             ptr_option['open'] = False
    #             elephant_option['open'] = False

    #     return pressure + np.max(max)

    a, b = get_permutation([valve['index'] for valve in get_options()])

    pressures = []
    for i in range(len(a)):
        curr = 0
        for j in a[i]:
            valves[j]['open'] = True
        curr += max_pressure(ptr, t)
        for j in a[i]:
            valves[j]['open'] = False

        for j in b[i]:
            valves[j]['open'] = True
        curr += max_pressure(ptr, t)
        for j in b[i]:
            valves[j]['open'] = False

        pressures.append(curr)
    return np.max(pressures)


def part_one():
    print("--- part one ---")

    for valve in valves:
        if valve['name'] == 'AA':
            print(max_pressure(valve, 30))


def part_two():
    print("--- part two ---")

    for valve in valves:
        if valve['name'] == 'AA':
            print(max_pressure_with_stupid_elephant(
                valve, -1, valve, -1, 0, 26))


part_one()
part_two()
