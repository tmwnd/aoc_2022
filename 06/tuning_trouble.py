with open("data.txt") as f:
    data = f.readline()

def find_first_n_unique(s, n):
    for i in range(len(data)-n):
        for j in range(n-1):
            if data[i+j] in data[i+j+1:i+n]:
                break
            if j == n-2:
                return i+n

def part_one():
    print("--- part one ---")
    print(find_first_n_unique(data, 4))

def part_two():
    print("--- part two ---")
    print(find_first_n_unique(data, 14))

part_one()
part_two()