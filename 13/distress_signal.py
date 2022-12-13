with open("data.txt") as f:
    file = [line.strip() for line in f.readlines()]

def make_packet(s):
    if "[" not in s:
        return int(s)
    if s == "[]":
        return []

    s = s[1:-1]
    packet = []

    depth = 0
    i = 0
    for di, c in enumerate(s):
        depth += int(c == "[") - int(c == "]")
        if depth == 0 and c == ",":
            packet.append(make_packet(s[i:di]))
            i = di+1
    packet.append(make_packet(s[i:di+1]))

    return packet

data = []
for signal in file:
    if signal != "":
        data.append(make_packet(signal))

def compare_signals(left, right):
    def type_value(obj):
        if type(obj) == int: return 0
        if type(obj) == list: return 1

    type_values = [type_value(left), type_value(right)]
    match type_values:
        case [0, 0]:
            return left - right
        case [1, 0]:
            return compare_signals(left, [right])
        case [0, 1]:
            return compare_signals([left], right)
        case [1, 1]:
            for i in range(max(len(left), len(right))):
                if i >= len(left): return -1
                if i >= len(right): return 1

                y = compare_signals(left[i], right[i])
                if y != 0: return y
            return 0

def part_one():
    print("--- part one ---")
    print(sum([(i+1) * int((compare_signals(data[2*i], data[2*i+1]) <= 0)) for i in range(len(data)//2)]))

def part_two():
    print("--- part two ---")
    data.append([[2]])
    data.append([[6]])
    print(sorted(data, cpr=compare_signals))

part_one()
part_two()