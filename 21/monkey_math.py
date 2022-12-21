with open("data.txt") as f:
    file = [line.strip() for line in f.readlines()]

data = {}
for line in file:
    key, value = line.split(": ")
    match value.split(" "):
        case [a, "+", b]:
            def f(a=a, b=b): return data[a]['f']() + data[b]['f']()
            def d(next, target, a=a, b=b): return target - data[a]['f']() if next == b else target - data[b]['f']()
        case [a, "-", b]:
            def f(a=a, b=b): return data[a]['f']() - data[b]['f']()
            def d(next, target, a=a, b=b): return data[a]['f']() - target if next == b else target + data[b]['f']()
        case [a, "*", b]:
            def f(a=a, b=b): return data[a]['f']() * data[b]['f']()
            def d(next, target, a=a, b=b): return target // data[a]['f']() if next == b else target // data[b]['f']()
        case [a, "/", b]:
            def f(a=a, b=b): return data[a]['f']() // data[b]['f']()
            def d(next, target, a=a, b=b): return data[a]['f']() // target if next == b else target * data[b]['f']()
        case n:
            a = b = d = None
            f = lambda n=int(n[0]): n

    data[key] = {
        'left': a,
        'right': b,
        'f': f,
        'd': d
    }


def find_path_to_humn(ptr, stack=[]):
    stack = stack.copy()
    stack.append(ptr)

    if ptr == 'humn': return stack

    monkey = data[ptr]
    for child in ['left', 'right']:
        if monkey[child] is not None:
            path = find_path_to_humn(monkey[child], stack)
            if len(path) > 0: return path

    return []


def part_one():
    print("--- part one ---")
    print(data['root']['f']())


def part_two():
    print("--- part two ---")

    root = data['root']
    root['d'] = lambda next, _, a=root['left'], b=root['right']: data[a]['f']() if next == b else data[b]['f']()

    path = find_path_to_humn('root')
    target = 0
    for i in range(len(path) - 1):
        target = data[path[i]]['d'](path[i + 1], target)
    print(target)


part_one()
part_two()
