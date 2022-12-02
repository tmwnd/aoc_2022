import numpy as np

points = [[1, 2, 0], [0, 1, 2], [2, 0, 1]]

def calc_points_1(shapes):
    score = ord(shapes[1])-87
    outcome = points[ord(shapes[0])-65][ord(shapes[1])-88]

    return score + outcome*3

def calc_points_2(shapes):
    outcome = ord(shapes[1])-88
    i = ord(shapes[0])-65
    if outcome == 0:
        score = np.argmin(points[i])
    elif outcome == 1:
        score = np.argmax(np.array(points[i]) % 2)
    elif outcome == 2:
        score = np.argmax(points[i])
    
    return score+1 + outcome*3


with open("data.txt") as f:
    data = f.readlines()
data = [l.strip().split(" ") for l in data]

def part_one():
    print("--- part one ---")
    print(np.sum([calc_points_1(shapes) for shapes in data]))

def part_two():
    print("--- part two ---")
    print(np.sum([calc_points_2(shapes) for shapes in data]))

part_one()
part_two()