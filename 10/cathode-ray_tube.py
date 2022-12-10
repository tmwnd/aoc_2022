import numpy as np

with open("data.txt") as f:
    instructions = [line.strip().split(" ") for line in f.readlines()]
with open("alphabet.txt") as f:
    alphabet = [line.strip() for line in f.readlines()]

X = [1]
stack = []

for instruction in instructions[:-1]:
    match instruction:
        case ["noop"]:
            stack.append(lambda x: x)
        case ["addx", v]:
            stack.append(lambda x: x)
            stack.append(lambda x, v=v: x + int(v))

    X.append(stack.pop(0)(X[-1]))
for cycle in stack:
    X.append(cycle(X[-1]))


def part_one():
    print("--- part one ---")

    sum = 0
    for i, x in enumerate(X):
        if (i - 19) % 40 == 0:
            sum += (i+1) * x
    print(sum)


def part_two():
    print("--- part two ---")

    display = []
    for i, x in enumerate(X):
        if np.abs((i % 40) - x) <= 1:
            display.append("#")
        else:
            display.append(".")

    for i, pixel in enumerate(display):
        if i > 0 and i % 40 == 0:
            print()
        print(pixel, end="")
    print()

    letters = []
    for x in range(8):
        letter = ""
        for y in range(6):
            for c in display[x*5+y*40:x*5+y*40+4]:
                letter += c
        letters.append(letter)
    for letter in letters:
        for i, c in enumerate(alphabet):
            if letter == c:
                print(chr(i+65), end="")
    print()


part_one()
part_two()
