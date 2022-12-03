def halve(list):
    return [list[:len(list)//2], list[len(list)//2:]]


with open('data.txt') as f:
    data = f.readlines()
data = [halve(rucksack.strip()) for rucksack in data]


def part_one():
    print("--- part one ---")

    sum = 0
    for rucksack in data:
        for item in rucksack[0]:
            if item in rucksack[1]:
                sum += ord(item)-38 if item.isupper() else ord(item)-96
                break

    print(sum)


def part_two():
    print("--- part two ---")

    sum = 0
    for i in range(len(data)//3):
        i *= 3
        for item in data[i][0] + data[i][1]:
            if item in data[i+1][0] + data[i+1][1] and item in data[i+2][0] + data[i+2][1]:
                sum += ord(item)-38 if item.isupper() else ord(item)-96
                break

    print(sum)


part_one()
part_two()
