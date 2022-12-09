import numpy as np

with open("data.txt") as f:
    data = [line.strip().split(" ") for line in f.readlines()]

def print_state(H, T, visited, show_rope=True, show_visited=False):
    # print(f"H: {H}")
    # print(f"T: {T}")

    def label(x, y):
        if show_rope:
            if H[0] == x and H[1] == y:
                return "H"
            for i, t in enumerate(T):
                if t[0] == x and t[1] == y:
                    if len(T) == 1:
                        return "T"
                    return i+1
            if x == 0 and y == 0 and len(T) > 1:
                return "s"
        if show_visited:
            for pos in visited:
                if pos[0] == x and pos[1] == y:
                    return "#"
        return "."

    pos = np.array([H, *T, *visited])
    ranges = np.vstack((np.min(pos, axis=0, initial=0).astype(int), np.max(pos, axis=0).astype(int))) + [[0, 0], [1, 1]]

    for y in range(*ranges[:,1])[::-1]:
        for x in range(*ranges[:,0]):
            print(label(x, y), end="")
        print()

def make_head_with_n_tails_and_move(n, instructions):
    H = np.array([0, 0])
    T = np.zeros(n*2).reshape(-1, 2)
    visited = [T[-1].copy()]

    def add_visit(T):
        for pos in visited:
            if pos[0] == T[0] and pos[1] == T[1]:
                return
        visited.append(T.copy())

    def move(H, T, dh, n):
        for _ in range(n):
            H += dh
            
            for i, t in enumerate(T):
                a = (T[i-1] if i > 0 else H) - t
                
                dt = [0, 0]
                if np.any(a!=0):
                    if np.max(np.abs(a)) == 2:
                        dt = np.sign(a) * [1, 1]
                elif np.max(np.abs(a)) == 2:
                    dt = a//2
                
                if np.any(dt != 0):
                    t += dt

            if np.any(dt != 0):
                add_visit(t)

    for instruction in instructions:
        match instruction:
            case ["U", n]:
                move(H, T, [0, 1], int(n))
            case ["D", n]:
                move(H, T, [0, -1], int(n))
            case ["L", n]:
                move(H, T, [-1, 0], int(n))
            case ["R", n]:
                move(H, T, [1, 0], int(n))

    # print_state(H, T, visited, show_rope=True, show_visited=True)
    print(len(visited))

def part_one():
    print("--- part one ---")
    make_head_with_n_tails_and_move(1, data)  

def part_two():
    print("--- part two ---")
    make_head_with_n_tails_and_move(9, data)        

part_one()
part_two()