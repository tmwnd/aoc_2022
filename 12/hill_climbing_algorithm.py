with open("data.txt") as f:
    data = [[ord(c)-97 for c in line.strip()] for line in f.readlines()]

def f(node):
    g = node['g']
    f = 25 - node['val']
    return g + f

def make_node(v):
    return {
        'val': v if v >= 0 else 0 if v == -14 else 25,
        'g': 0,
        'state': 0,
        'is_start': v == -14,
        'is_target': v == -28,
        'neighbors': []
    }

nodes = []
for line in data:
    curr = []
    for v in line:
        curr.append(make_node(v))
    nodes.append(curr)

queue = []
for i in range(len(nodes)):
    for j, node in enumerate(nodes[i]):
        if node['is_start']:
            queue.append(node)

        for di, dj in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
            if 0 <= i+di < len(nodes) and 0 <= j+dj < len(nodes[i+di]):
                if -1 <= nodes[i+di][j+dj]['val'] - nodes[i][j]['val'] <= 1:
                    node['neighbors'].append(nodes[i+di][j+dj])

print(queue[-1]['val'])

def part_one():
    print("--- part one ---")


def part_two():
    print("--- part two ---")     

part_one()
part_two()