import numpy as np

with open('data.txt') as f:
    file = f.readlines()
file = [line.strip() for line in file]

index = [-1]
index.extend([i for i, x in enumerate(file) if x == ""])
index.append(len(file))

data = []
for i in range(len(index)-1):
    data.append(np.sum([int(val) for val in file[index[i]+1:index[i+1]]]))

def part_one():
    print("--- part one ---")
    print(np.max(data))

def part_two():
    print("--- part two ---")
    data.sort()
    print(np.sum(data[-3:]))

part_one()
part_two()