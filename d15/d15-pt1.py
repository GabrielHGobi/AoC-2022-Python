import math

class Obj:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class Beacon(Obj):
    def __init__(self, x, y):
        super().__init__(x, y)

class Sensor(Obj):
    def __init__(self, x, y, xb, yb):
        super().__init__(x, y)
        self.beacon = Beacon(xb, yb)
        self.coverage = self.manhattan_dist(xb, yb)
    
    def manhattan_dist(self, x, y):
        return abs(self.x - x) + abs(self.y - y)


all_sensors = []
with open("./input.txt", "r") as f:
    while True:
        line = f.readline()
        if not line:
            break
        line = line.split()
        x_sensor = int(line[2].split('=')[1].split(',')[0])
        y_sensor = int(line[3].split('=')[1].split(':')[0])
        x_beacon = int(line[8].split('=')[1].split(',')[0])
        y_beacon = int(line[9].split('=')[1])
        all_sensors.append(Sensor(x_sensor, y_sensor, x_beacon, y_beacon))
all_beacons = [sensor.beacon for sensor in all_sensors]

min_x_possible_to_detect = math.inf
max_x_possible_to_detect = -math.inf

for sensor in all_sensors:
    if sensor.x + sensor.coverage - 1 > max_x_possible_to_detect:
        max_x_possible_to_detect = sensor.x + sensor.coverage - 1
    if sensor.x - sensor.coverage + 1 < min_x_possible_to_detect:
        min_x_possible_to_detect = sensor.x - sensor.coverage + 1

count = 0
row_to_check = 2_000_000
found = False
there_is_a_beacon = False
for x in range(min_x_possible_to_detect, max_x_possible_to_detect+1):
    for sensor in all_sensors:
        if sensor.manhattan_dist(x, row_to_check) <= sensor.coverage:
            there_is_a_beacon = False
            for beacon in all_beacons:
                if beacon.x == x and beacon.y == row_to_check: 
                    there_is_a_beacon = True
            if not there_is_a_beacon:
                count += 1
                found = True
                break
    if found:
        found = False
        continue

print(count) # it consumes a lot of time :( 
# Need to improve for part 2

