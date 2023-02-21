class Cube:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.adj_cubes = []

    def is_adjacent(self, other):
        if self.x == other.x and self.z == other.z and abs(self.y - other.y) == 1:
            return True 
        if self.x == other.x and self.y == other.y and abs(self.z - other.z) == 1:
            return True
        if self.y == other.y and self.z == other.z and abs(self.x - other.x) == 1:
            return True
        return False

    def group(self, other):
        self.adj_cubes.append(other)

    def get_surface_area(self):
        return 6 - len(self.adj_cubes)


cubes = []
with open("./input.txt", "r") as f:
    while True:
        line = f.readline().replace('\n', '')
        if not line:
            break
        coord = line.split(',')
        cubes.append(Cube(int(coord[0]), int(coord[1]), int(coord[2])))

for cube in cubes:
    for other_cube in cubes:
        if cube != other_cube and cube.is_adjacent(other_cube):
            cube.group(other_cube)

total_surface_area = 0
for cube in cubes:
    total_surface_area += cube.get_surface_area()

print(total_surface_area)


