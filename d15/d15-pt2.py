import functools

class Obj:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class Beacon(Obj):
    def __init__(self, x, y):
        super().__init__(x, y)

class Sensor(Obj):
    def __init__(self, id, x, y, xb, yb):
        super().__init__(x, y)
        self.id = id
        self.beacon = Beacon(xb, yb)
        self.coverage = self.manhattan_dist(xb, yb)
    
    def manhattan_dist(self, x, y):
        return abs(self.x - x) + abs(self.y - y)


all_sensors = []
with open("./input.txt", "r") as f:
    id = 0
    while True:
        line = f.readline()
        if not line:
            break
        line = line.split()
        x_sensor = int(line[2].split('=')[1].split(',')[0])
        y_sensor = int(line[3].split('=')[1].split(':')[0])
        x_beacon = int(line[8].split('=')[1].split(',')[0])
        y_beacon = int(line[9].split('=')[1])
        all_sensors.append(Sensor(id, x_sensor, y_sensor, x_beacon, y_beacon))
        id += 1
all_beacons = [sensor.beacon for sensor in all_sensors]


class PointOfSegment:
    def __init__(self, x, type, id):
        self.x = x
        self.type = type
        self.id = id
    
    def __repr__(self) -> str:
        return self.x.__repr__()

def compare(a: PointOfSegment, b:PointOfSegment):
    if a.x < b.x:
        return -1
    if a.x > b.x:
        return 1
    if a.x == b.x:
        if a.type == 's':
            return -1
        if b.type == 's':
            return 1
        return 0

def interval_covered_by_sensor_at_row(sensor: Sensor, row: int, xlim: tuple):
    if sensor.manhattan_dist(sensor.x, row) > sensor.coverage:
        return None
    horizontal_dist = sensor.coverage - sensor.manhattan_dist(sensor.x, row)
    x_min = max(xlim[0], sensor.x - horizontal_dist)
    x_max = min(xlim[1], sensor.x + horizontal_dist)
    return [PointOfSegment(x_min, 's', sensor.id), PointOfSegment(x_max, 'e', sensor.id)]

def interval_covered_by_all_sensor_at_row(all_sensors: list, row: int, xlim: tuple):
    intervals_covered_by_S = []
    for sensor in all_sensors:
        seg = interval_covered_by_sensor_at_row(sensor, row, xlim) 
        if not seg is None:
            intervals_covered_by_S.append(seg)

    all_points = []
    for seg in intervals_covered_by_S:
        all_points.append(seg[0])
        all_points.append(seg[1])

    all_points.sort(key=functools.cmp_to_key(compare))

    union_of_segments = []
    segments_together = []
    xmin = None
    for i in range(len(all_points)):
        point = all_points[i]
        
        if point.type == 's':
            if not segments_together:
                xmin = point.x
            segments_together.append(point.id)
        
        if point.type == 'e':
            segments_together.remove(point.id)
            if not segments_together:
                union_of_segments.append([xmin, point.x])

    return union_of_segments

for row in range(4_000_000):
    interval_covered = interval_covered_by_all_sensor_at_row(all_sensors, row, (0, 4_000_000))
    if len(interval_covered) > 1:
        y = row
        x = interval_covered[0][1] + 1
        print(f'Tuning frequency: {x * 4_000_000 + y}')

