import numpy as np
from multiprocessing import Pool
from functools import partial

with open("data.txt") as f:
    file = [line.strip() for line in f.readlines()]

ORES = {
    "ore": 0,
    "clay": 1,
    "obsidian": 2,
    "geode": 3
}


def make_blueprint(id, ore, clay, obsidian, geode):
    return {
        "id": id,
        "ore": ore,
        "clay": clay,
        "obsidian": obsidian,
        "geode": geode
    }


def make_state(robots, building_robots=[0, 0, 0, 0], ores=np.array([0, 0, 0, 0])):
    return {
        "robots": robots,
        "building_robots": building_robots,
        "ores": ores.copy()
    }


def get_state_options(state, blueprint, max_robots):
    ores = state['ores']
    robots = state['robots']

    ores += robots
    robots = robots + state['building_robots']

    if any(robots > max_robots): return []
    if all(ores - blueprint["geode"] >= 0): return [make_state(robots, [0, 0, 0, 1], ores - blueprint["geode"])]

    options = []
    for i, ore in enumerate(ORES):
        if ore == "geode": continue

        if all(ores - blueprint[ore] >= 0):
            options.append(make_state(robots, [int(i == j) for j in range(len(robots))], ores - blueprint[ore]))

    if len(options) <= len(ORES) - 1:
        options.append(make_state(robots, ores=ores))

    return options


def sort_robots_key(state):
    return (state['robots'] + state['building_robots']) @ [100**i for i in range(len(ORES))]


def get_n_sorted_querry_options(queue_options, n=10000):
    queue_options.sort(key=sort_robots_key)

    ret = []
    options = []
    key = -1
    for option in queue_options[::-1]:
        if sort_robots_key(option) != key:
            for i, state in enumerate(options):
                if any([all(state['ores'] <= x['ores']) and any(state['ores'] < x['ores']) for x in options[:i]]): continue
                if any([all(state['ores'] <= x['ores']) and any(state['ores'] < x['ores']) for x in options[i + 1:]]): continue
                ret.append(state)

            if len(ret) >= n:
                return ret[:n + 1]

            options = [option]
            key = sort_robots_key(option)
        else:
            options.append(option)
    ret.extend(options)

    return ret[:n + 1]


data = []
for line in file:
    id, line = line.split(": ")
    id = int(id.replace("Blueprint ", ""))
    costs = []
    for robot in line[:len(line) - 1].split(". "):
        ores = [0, 0, 0, 0]
        for price in robot.split("costs ")[1].split(" and "):
            for key in ORES:
                if key in price:
                    ores[ORES[key]] = int(price.replace(f" {key}", ""))
        costs.append(ores)
    data.append(make_blueprint(id, *costs))


def simulate_blueprint(blueprint, T=24, DEBUG=False):
    if DEBUG: print(f"started blueprint {blueprint['id']}. simulate for {T} minutes")

    max_robots = [[np.inf if ore == "geode" else 0 for ore in ORES]]
    max_robots.extend([blueprint[ore] for ore in ORES])
    max_robots = np.max(max_robots, axis=0)

    queue_options = [make_state(np.array([1, 0, 0, 0]))]
    for _ in range(T):
        queue = get_n_sorted_querry_options(queue_options)
        queue_options = []
        while len(queue) > 0:
            queue_options.extend(get_state_options(queue.pop(), blueprint, max_robots))

    quality_level = sorted(queue_options, key=lambda state: state['ores'][3])[-1]['ores'][3] * blueprint['id']
    if DEBUG: print(f"finished blueprint {blueprint['id']} with quality level {quality_level}")
    return quality_level


def part_one():
    print("--- part one ---")

    with Pool(6) as p:
        quality_levels = p.map(simulate_blueprint, data)
    print(sum(quality_levels))


def part_two():
    print("--- part two ---")

    with Pool(3) as p:
        quality_levels = p.map(partial(simulate_blueprint, T=32), data[:3])
    print(np.prod(quality_levels) // np.math.factorial(3))


if __name__ == '__main__':
    part_one()
    part_two()
