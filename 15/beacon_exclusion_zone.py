import numpy as np

with open("data.txt") as f:
    file = [line.strip() for line in f.readlines()]

def dist(x, y, dx, dy):
    return np.abs(x-dx) + np.abs(y-dy)

def make_sensor(x, y, d):
    return {
        'x': x,
        'y': y,
        'd': d
    }

def to_string(sensors, beacons):
    x0 = np.min([sensor['x'] - sensor['d'] for sensor in sensors])
    xn = np.max([sensor['x'] + sensor['d'] for sensor in sensors])
    y0 = np.min([sensor['y'] - sensor['d'] for sensor in sensors])
    yn = np.max([sensor['y'] + sensor['d'] for sensor in sensors])

    for y in range(y0, yn+1):
        for x in range(x0, xn+1):
            for sensor in sensors:
                if dist(sensor['x'], sensor['y'], x, y) == 0:
                    print("S", end="")
                    x = x0-1
                    break
            if x >= x0:
                for beacon in beacons:
                    if dist(*beacon, x, y) == 0:
                        print("B", end="")
                        x = x0-1
                        break
            if x >= x0:
                for sensor in sensors:
                    if dist(sensor['x'], sensor['y'], x, y) <= sensor['d']:
                        print("#", end="")
                        x = x0-1
                        break
            if x >= x0:
                print(".", end="")
        print()

sensors = []
beacons = set()
for line in file:
    points = [int(x) for x in line.replace("Sensor at x=", ", ").replace(", y=", ", ").replace(": closest beacon is at x=", ", ").split(", ")[1:]]
    sensors.append(make_sensor(*points[:2], dist(*points)))
    beacons.add(tuple(points[2:]))

# to_string(sensors, beacons)
def get_blocked(sensors, y):
    blocked = []

    for sensor in sensors:
        dy = np.abs(sensor['y'] - y)
        if dy < sensor['d']:
            dx = sensor['d'] - dy
            blocked.append([sensor['x'] - dx, sensor['x'] + dx])

    # print(blocked)
    
    return blocked

def len_blocked(sensors, beacons, y):
    blocked = get_blocked(sensors, y)

    x0 = np.min([b[0] for b in blocked])
    xn = np.max([b[1] for b in blocked])

    sum = 0
    x = x0
    while x <= xn:
        for b in blocked:
            if b[0] <= x <= b[1]:
                sum += b[1] - x + 1
                x = b[1]
                break
        x += 1
    return sum - np.sum([beacon[1] == y for beacon in beacons])

def get_tuning_frequency(sensors, beacons, y, x0, xn):
    blocked = get_blocked(sensors, y)

    x = x0
    while x <= xn:
        is_blocked = False
        for b in blocked:
            if b[0] <= x <= b[1]:
                x = b[1]
                is_blocked = True
                break
        if not is_blocked:
            return str(x*4//10) + str((x%10)*4000000 + y)
        x += 1
    return ""
        

def part_one():
    print("--- part one ---")
    
    print(len_blocked(sensors, beacons, 2000000))
    

def part_two():
    print("--- part two ---")

    for y in range(0, 4000001)[::-1]:
        tuning_frequency = get_tuning_frequency(sensors, beacons, y, 0, 4000000)
        if tuning_frequency != "":
            print(tuning_frequency)
            break

part_one()
part_two()