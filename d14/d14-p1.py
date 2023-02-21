class Rock:
    def __init__(self, path):
        self.path = path
        
    def get_xlim(self):
        path_sorted_by_x = sorted(self.path)
        return (path_sorted_by_x[0][0], path_sorted_by_x[-1][0])

    def get_ylim(self):
        path_sorted_by_y = sorted(self.path, key=lambda a: a[1])
        return (path_sorted_by_y[0][1], path_sorted_by_y[-1][1])
        

all_rocks = []
with open("./input.txt", "r") as f:
    while True:
        line = f.readline() 
        if not line:
            break
        rock_path_str = line.replace('-', '').replace('>', '').replace('\n', '')
        path = []
        for coordinate in rock_path_str.split():
            x_str, y_str = coordinate.split(',')
            path.append((int(x_str), int(y_str)))
        all_rocks.append(Rock(path))


class Grid:
    def __init__(self, rocks):
        self.xlim, self.ylim = self.get_lims(rocks)
        self.grid = [ ['.' for _ in range(self.xlim[1]-self.xlim[0]+1)] for _ in range(self.ylim[1]+1)]
        self.origin = (500, 0)
        self.grid[self.origin[1]][self.origin[0] - self.xlim[0]] = '+'
        for rock in rocks:
            self._construct_rock_path(rock)
        self.y_abyss = self.ylim[1]
        self.y_lowest_sand = 0

    def get_lims(self, rocks):
        all_xlim = [rock.get_xlim() for rock in rocks]
        all_ylim = [rock.get_ylim() for rock in rocks]
        all_xlim_sorted_by_xmin = sorted(all_xlim)
        all_xlim_sorted_by_xmax = sorted(all_xlim, key=lambda a: a[1])
        grid_xlim = (all_xlim_sorted_by_xmin[0][0] - 2, all_xlim_sorted_by_xmax[-1][1] + 2)
        all_ylim_sorted_by_ymax = sorted(all_ylim, key=lambda a: a[1])
        grid_ylim = (0, all_ylim_sorted_by_ymax[-1][1] + 1)
        return grid_xlim, grid_ylim

    def _construct_rock_path(self, rock: Rock):
        
        def _construct_rock_line(from_pos, to_pos):
            # vertical line
            if from_pos[0] == to_pos[0]:
                x_line = from_pos[0]
                y_from = min(from_pos[1], to_pos[1])
                y_to = max(from_pos[1], to_pos[1])
                for y in range(y_from, y_to+1):
                    self.grid[y][x_line - self.xlim[0]] = '#'
            # horizontal line
            else:
                y_line = from_pos[1]
                x_from = min(from_pos[0], to_pos[0])
                x_to = max(from_pos[0], to_pos[0])
                for x in range(x_from, x_to+1):
                    self.grid[y_line][x-self.xlim[0]] = '#'

        for i in range(len(rock.path) - 1):
            from_pos = rock.path[i]
            to_pos = rock.path[i+1]
            _construct_rock_line(from_pos, to_pos)
    
    def drop_sand(self):
        (x_curr, y_curr) = self.origin
        while True:
            if y_curr > self.y_lowest_sand:
                self.y_lowest_sand = y_curr
            if y_curr >= self.y_abyss:
                self.grid[y_curr][x_curr-self.xlim[0]] = 'o'
                break

            if self.grid[y_curr+1][x_curr-self.xlim[0]] == '.':
                y_curr += 1
                continue
            elif self.grid[y_curr+1][x_curr-self.xlim[0]-1] == '.':
                y_curr += 1
                x_curr -= 1
                continue
            elif self.grid[y_curr+1][x_curr-self.xlim[0]+1] == '.':
                y_curr += 1
                x_curr += 1
                continue
            self.grid[y_curr][x_curr-self.xlim[0]] = 'o'
            
            break


    def print(self):
        for i in range(len(self.grid)):
            line = self.grid[i]
            for j in range(len(line)):
                print(self.grid[i][j], end='')
            print()
        print()

grid = Grid(all_rocks)
# grid.print()
units_of_sand = 0
while grid.y_lowest_sand < grid.y_abyss:
    grid.drop_sand()
    units_of_sand += 1
    # grid.print()

print(units_of_sand-1)