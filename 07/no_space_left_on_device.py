import numpy as np

with open("data.txt") as f:
    out = f.readlines()

def make_dir(name, size=0):
    return {
        'name': name,
        'size': size,  
        'subdirs' : []
    }

# def get_ptr(root, name):
#     for subdir in root['subdirs']:
#         ptr = get_ptr(subdir, name)
#         if ptr is not None:
#             return ptr
#     if root['name'] == name:
#         return root
#     return None

def get_ptr(root, name):
    for subdir in root['subdirs']:
        if subdir['name'] == name:
            return subdir

root = make_dir("/")

ptr = root
stack = []

for line in out:
    line = line.strip()

    if "$" in line:
        match line[2:].split(" "):
            case ["cd", "/"]:
                ptr = root
                stack = []
            case ["cd", ".."]:
                ptr = stack.pop()
            case ["cd", dir_name]:
                stack.append(ptr)
                ptr = get_ptr(ptr, dir_name)
    else:
        match line.split(" "):
            case ["dir", dir_name]:
                ptr['subdirs'].append(make_dir(dir_name))
            case [size, file_name]:
                size = int(size)

                ptr['size'] += size
                for dir in stack:
                    dir['size'] += size

                ptr['subdirs'].append(make_dir(file_name, size))

def to_string(root, depth=0):
    print(f"{' '*(depth*2)}- {root['name']} ({'file' if len(root['subdirs']) == 0 else 'dir'}, {root['size']})")
    for subdir in root['subdirs']:
        to_string(subdir, depth+1)
# to_string(root)

def sum_size_under_n(root, n):
    if len(root['subdirs']) == 0:
        return 0
    return root['size'] * int(root['size'] <= n) + sum([sum_size_under_n(subdir, n) for subdir in root['subdirs']])

def find_smallest_over_n(root, n):
    if root['size'] < n or len(root['subdirs']) == 0:
        return 0
    arr = [find_smallest_over_n(subdir, n) for subdir in root['subdirs']]
    arr.append(root['size'])
    arr = np.array(arr)
    return min(arr[arr != 0])

def part_one():
    print("--- part one ---")
    print(sum_size_under_n(root, 100000))

def part_two():
    print("--- part two ---")
    print(find_smallest_over_n(root, 30000000 - (70000000 - root['size'])))

part_one()
part_two()