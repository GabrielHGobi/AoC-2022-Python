from queue import Queue

LAVA_DROPLET = 1
EMPTY = 0

class Cube:
    def __init__(self, x, y, z, is_lava_droplet = False) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.is_lava_droplet = is_lava_droplet
        self.adj_cubes_coords = []

    def is_adjacent(self, other):
        if self.x == other.x and self.z == other.z and abs(self.y - other.y) == 1:
            return True 
        if self.x == other.x and self.y == other.y and abs(self.z - other.z) == 1:
            return True
        if self.y == other.y and self.z == other.z and abs(self.x - other.x) == 1:
            return True
        return False

    def group(self, other):
        self.adj_cubes_coords.append((other.x, other.y, other.z))

    def get_possible_trapped_cubes_coords(self):
        possible_trapped_cubes_coords = []
        for (dx, dy, dz) in [(+1, 0, 0), (-1, 0, 0), (0, +1, 0), (0, -1, 0), (0, 0, +1), (0, 0, -1)]:
            possible_adj_coord = (self.x + dx, self.y + dy, self.z + dz)
            if not possible_adj_coord in self.adj_cubes_coords:
                possible_trapped_cubes_coords.append(possible_adj_coord)
        return possible_trapped_cubes_coords

    def get_surface_area(self):
        return 6 - len(self.adj_cubes_coords)


class Lava:
    def __init__(self) -> None:
        self.lava_droplets = []
        
    def add_lava_cube_droplet(self, cube_droplet):
        self.lava_droplets.append(cube_droplet)

    def _get_convex_hull_grid(self):
        self.lava_droplets.sort(key= lambda a: a.x)
        min_x, max_x = self.lava_droplets[0].x, self.lava_droplets[-1].x
        Lx = max_x - min_x + 1
        self.lava_droplets.sort(key= lambda a: a.y)
        min_y, max_y = self.lava_droplets[0].y, self.lava_droplets[-1].y
        Ly = max_y - min_y + 1
        self.lava_droplets.sort(key= lambda a: a.z)
        min_z, max_z = self.lava_droplets[0].z, self.lava_droplets[-1].z
        Lz = max_z - min_z + 1

        cube_droplets_coords = [(cube.x, cube.y, cube.z) for cube in self.lava_droplets]
        hull_grid = [ [ [None for _ in range(Lz)] for _ in range(Ly) ] for _ in range(Lx) ]
        for x in range(Lx):
            for y in range(Ly):
                for z in range(Lz):
                    if (min_x + x, min_y + y, min_z + z) in cube_droplets_coords:
                        hull_grid[x][y][z] = LAVA_DROPLET
                    else:
                        hull_grid[x][y][z] = EMPTY   
        return hull_grid
    
    def _get_trapped_blobs(self):
        trapped_blobs = []
        hull_grid = self._get_convex_hull_grid()
        Lx = len(hull_grid)
        Ly = len(hull_grid[0])
        Lz = len(hull_grid[0][0])
        visited = [ [ [False for _ in range(Lz)] for _ in range(Ly) ] for _ in range(Lx) ]
        
        def BFS(start):
            blob = []
            q = Queue()
            q.put(start)
            while not q.empty():
                (x, y, z) = q.get()
                if not visited[x][y][z]:
                    visited[x][y][z] = True
                    blob.append(Cube(x, y, z))
                    for (dx, dy, dz) in [(+1, 0, 0), (-1, 0, 0), (0, +1, 0), (0, -1, 0), (0, 0, +1), (0, 0, -1)]:
                        if x + dx >= 0 and  x + dx < Lx and y + dy >= 0 and y + dy < Ly and z + dz >= 0 and z + dz < Lz:
                            if not visited[x+dx][y+dy][z+dz] and hull_grid[x+dx][y+dy][z+dz] == EMPTY:
                                q.put((x+dx, y+dy, z+dz))
            return blob
        
        for x in range(Lx):
            for y in range(Ly):
                for z in range(Lz):
                    if not visited[x][y][z] and hull_grid[x][y][z] == EMPTY:
                        empty_blob = BFS((x, y, z))
                        is_trapped = True
                        for cube in empty_blob:
                            if cube.x == 0 or cube.x == Lx-1 or cube.y == 0 or cube.y == Ly-1 or cube.z == 0 or cube.z == Lz-1:
                                is_trapped = False
                        if is_trapped:
                            trapped_blobs.append(empty_blob)

        return trapped_blobs


    def get_interior_surface_area(self):
        interior_surface_area = 0
        for empty_blob in self._get_trapped_blobs():
            interior_surface_area += self.get_total_surface_area(empty_blob)
        return interior_surface_area
    
    def get_total_surface_area(self, cubes):
        for cube in cubes:
            for other_cube in cubes:
                if cube != other_cube and cube.is_adjacent(other_cube):
                    cube.group(other_cube)

        total_surface_area = 0
        for cube in cubes:
            total_surface_area += cube.get_surface_area()
        return total_surface_area
    
    def get_exterior_surface_area(self):
        lava_droplets_surface_area = self.get_total_surface_area(self.lava_droplets)
        trapped_cubes_surface_area = self.get_interior_surface_area() 
        return lava_droplets_surface_area - trapped_cubes_surface_area

lava = Lava()

with open("./input.txt", "r") as f:
    while True:
        line = f.readline().replace('\n', '')
        if not line:
            break
        coord = line.split(',')
        lava.add_lava_cube_droplet(Cube(int(coord[0]), int(coord[1]), int(coord[2]), True))

print(lava.get_exterior_surface_area())

# PART 1
# for cube in cubes:
#     for other_cube in cubes:
#         if cube != other_cube and cube.is_adjacent(other_cube):
#             cube.group(other_cube)

# total_surface_area = 0
# for cube in cubes:
#     total_surface_area += cube.get_surface_area()


# PROBLEM: adjacent trapped cubes
# possible_trapped_cubes_coords_counter = {}

# for cube in cubes:
#     possible_trapped_cubes_coords = cube.get_possible_trapped_cubes_coords()
#     for possible_trapped_cube_coord in possible_trapped_cubes_coords:
#         if not possible_trapped_cube_coord in possible_trapped_cubes_coords_counter.keys():
#             possible_trapped_cubes_coords_counter[possible_trapped_cube_coord] = 1
#         else:
#             possible_trapped_cubes_coords_counter[possible_trapped_cube_coord] += 1

# trapped_cubes = []
# for key, freq in possible_trapped_cubes_coords_counter.items():
#     print(key, freq)
#     if freq == 6:
#         trapped_cubes.append()

# print(total_surface_area - 6 * trapped_cubes)


