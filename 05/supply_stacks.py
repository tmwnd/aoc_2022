with open("data.txt") as f:
    file = f.readlines()

i = file.index("\n")

procedures = file[i+1:]
procedures = [[int(p)-1 for p in procedure.replace("move ", "").replace(" from ", ",").replace(" to ", ",").strip().split(',')] for procedure in procedures]

def get_stacks(i, file):
    stacks = [[] for _ in range(int(file[i-1].strip().split(" ")[-1]))]
    for line in file[:i-1][::-1]:
        for i, stack in enumerate(stacks):
            crate = line[1+i*4]
            
            if crate != " ":
                stack.append(crate)
    return stacks

def part_one():
    print("--- part one ---")

    stacks = get_stacks(i, file)

    for procedure in procedures:
        for _ in range(procedure[0]+1):
            stacks[procedure[2]].append(stacks[procedure[1]].pop())
    
    for stack in stacks:
        print(stack[-1], end="")
    print()

def part_two():
    print("--- part two ---")

    stacks = get_stacks(i, file)

    for procedure in procedures:
        for j in range(procedure[0]+1)[::-1]:
            stacks[procedure[2]].append(stacks[procedure[1]].pop(-j-1))
    
    for stack in stacks:
        print(stack[-1], end="")
    print()

part_one()
part_two()