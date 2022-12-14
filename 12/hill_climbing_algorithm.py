import numpy as np
import copy

with open("data.txt") as f:
    data = [[ord(c)-97 for c in line.strip()] for line in f.readlines()]


for i in range(len(data)):
    for j, v in enumerate(data[i]):
        if v == -14:
            start = np.array([i, j])
        elif v == -28:
            target = np.array([i, j])


def f(node):
    return node['g'] + node['h']


def h(v, pos):
    return np.sum(np.abs(target-pos)) - v**3


def make_node(v, pos):
    is_start = v == -14
    is_target = v == -28
    v = 0 if is_start else 25 if is_target else v
    return {
        'value': v,
        'g': 0,
        'h': h(v, pos),
        'is_in_queue': False,
        'is_complete': False,
        'is_start': is_start,
        'is_target': is_target,
        'neighbors': []
    }


def to_string(nodes, check='is_complete'):
    for i in range(len(nodes)):
        for node in nodes[i]:
            if node['is_start']:
                print("S", end="")
            elif node['is_target']:
                print("E", end="")
            elif node[check]:
                print("#", end="")
            else:
                print(".", end="")
        print()


def a(start=start):
    nodes = []
    for i in range(len(data)):
        curr = []
        for j, v in enumerate(data[i]):
            curr.append(make_node(v, [i, j]))
        nodes.append(curr)

    for i in range(len(nodes)):
        for j, node in enumerate(nodes[i]):
            for di, dj in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
                if 0 <= i+di < len(nodes) and 0 <= j+dj < len(nodes[i+di]):
                    if nodes[i+di][j+dj]['value'] - nodes[i][j]['value'] <= 1:
                        node['neighbors'].append(nodes[i+di][j+dj])

    queue = [nodes[start[0]][start[1]]]
    queue[0]['is_in_queue'] = True

    while len(queue) > 0:
        i = np.argmin([f(node) for node in queue])
        ptr = queue.pop(i)

        ptr['is_complete'] = True
        for node in ptr['neighbors']:
            if node['is_complete']:
                continue

            if node['is_in_queue']:
                if ptr['g'] + 1 < node['g']:
                    node['g'] = ptr['g'] + 1
                continue

            node['is_in_queue'] = True
            node['g'] = ptr['g'] + 1

            if node['is_target']:
                to_string(nodes)
                return node

            queue.append(node)


def part_one():
    print("--- part one ---")
    print(a()['g'])


def part_two():
    print("--- part two ---")
    print(np.min([a([i, 0])['g'] for i in range(len(data))]))


part_one()
part_two()
