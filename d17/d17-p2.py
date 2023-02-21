with open("input.txt", "r") as f:
    movements = f.readline().replace('\n', '')

class Rock:
    def __init__(self) -> None:
        self.shape = None
        self.curr_pos = None
        self.landed = False

    def spawn(self, chamber):
        self.curr_pos = (chamber.top + 4, 3)
        self.landed = False
    
    def get_rock_positions(self):
        pass

    def fall(self, chamber):
        can_move = True
        for position in self.get_rock_positions():
            (i, j) = position
            if not chamber.is_valid_to_move(i - 1 , j):
                can_move = False
                break
        if can_move:
            self.curr_pos = (self.curr_pos[0] - 1, self.curr_pos[1])
        else:
            self.land(chamber)

    def move_left_by_gas_jet(self, chamber):
        can_move = True
        for position in self.get_rock_positions():
            (i, j) = position
            if not chamber.is_valid_to_move(i , j - 1):
                can_move = False
                break
        if can_move:
            self.curr_pos = (self.curr_pos[0], self.curr_pos[1] - 1)

    def move_right_by_gas_jet(self, chamber):
        can_move = True
        for position in self.get_rock_positions():
            (i, j) = position
            if not chamber.is_valid_to_move(i , j + 1):
                can_move = False
                break
        if can_move:
            self.curr_pos = (self.curr_pos[0], self.curr_pos[1] + 1)

    def land(self, chamber):
        max_i = -1
        for position in self.get_rock_positions():
            (i, j) = position
            chamber.grid[i][j] = '#'
            max_i = max(i, max_i)
        self.landed = True
        chamber.top = max(chamber.top, max_i)

class HBarRock(Rock):
    def __init__(self) -> None:
        super().__init__()
        self.shape = ['#', '#', '#', '#']

    def get_rock_positions(self):
        (i0, j0) = self.curr_pos
        return [(i0, j0), (i0, j0+1), (i0, j0+2), (i0, j0+3)]

class StarRock(Rock):
    def __init__(self) -> None:
        super().__init__()
        self.shape = [['.', '#', '.'],
                      ['#', '#', '#'],
                      ['.', '#', '.']]

    def get_rock_positions(self):
        (i0, j0) = self.curr_pos
        return [(i0+1, j0), (i0, j0+1), (i0+1, j0+1), (i0+2, j0+1), (i0+1, j0+2)]
    

class LRock(Rock):
    def __init__(self) -> None:
        super().__init__()
        self.shape = [['.', '.', '#'],
                      ['.', '.', '#'],
                      ['#', '#', '#']]
    
    def get_rock_positions(self):
        (i0, j0) = self.curr_pos
        return [(i0, j0), (i0, j0+1), (i0, j0+2), (i0+1, j0+2), (i0+2, j0+2)]
    

class VBarRock(Rock):
    def __init__(self) -> None:
        super().__init__()
        self.shape = [['#'],
                      ['#'],
                      ['#'],
                      ['#']]

    def get_rock_positions(self):
        (i0, j0) = self.curr_pos
        return [(i0, j0), (i0+1, j0), (i0+2, j0), (i0+3, j0)]
    

class SquareRock(Rock):
    def __init__(self) -> None:
        super().__init__()
        self.shape = [['#', '#'],
                      ['#', '#']]

    def get_rock_positions(self):
        (i0, j0) = self.curr_pos
        return [(i0, j0), (i0+1, j0), (i0, j0+1), (i0+1, j0+1)]


class Chamber:
    def __init__(self) -> None:
        self.grid = [ ['.' for _ in range(9)] for _ in range(8) ]
        self.top = 0
        self._construct_ground_and_walls()

    def _construct_ground_and_walls(self):
        self.grid[0][0] = '+'
        self.grid[0][8] = '+'
        for j in range(1, 8):
            self.grid[0][j] = '-'
        for i in range(1, 8):
            self.grid[i][0] = '|'
            self.grid[i][8] = '|'
    
    def is_valid_to_move(self, i, j):
        if i > 0 and i <= self.top + 7 and j > 0 and j < 8:
            if self.grid[i][j] == '.':
                return True
            else:
                return False
    
    def clean(self):
        self.grid = [ ['.' for _ in range(9)] for _ in range(8) ]
        self.top = 0
        self._construct_ground_and_walls()

    def update(self):
        if self.top + 7 >= len(self.grid):
            for _ in range(self.top + 8 - len(self.grid)):
                self.grid.append(['|', '.', '.', '.', '.', '.', '.', '.', '|'])

    def print(self, falling_rock):
        rock_positions = falling_rock.get_rock_positions()
        for i in range(self.top + 7, -1, -1):
            for j in range(9):
                if (i, j) in rock_positions:
                    print('@', end='')
                else:
                    print(self.grid[i][j], end='')
            print()
        print()
    
    


rocks = [HBarRock(), StarRock(), LRock(), VBarRock(), SquareRock()]
chamber = Chamber()

def find_sequence_loop() -> dict:

    sequence = {"before_start": None, "delta_r": None, "delta_h": None}
    rock_0_mov_idx_list = []
    last_rock_0_mov_idx_list = [1]
    r_start = 0
    last_h = 0

    mov_i = 0
    for r in range(100000):
        rock_n = r % 5    
        rock = rocks[rock_n]
        rock.spawn(chamber)

        if rock_n == 0:
            if mov_i == last_rock_0_mov_idx_list[0]:
                sequence['before_start'] = r_start
                sequence['delta_r'] = r - r_start
                sequence['delta_h'] = chamber.top - last_h
                return sequence
            if len(rock_0_mov_idx_list) == 0:
                rock_0_mov_idx_list.append(mov_i)
            else:
                if mov_i < rock_0_mov_idx_list[-1]:
                    last_rock_0_mov_idx_list = rock_0_mov_idx_list
                    rock_0_mov_idx_list = [mov_i]
                    r_start = r
                    last_h = chamber.top
                else:
                    rock_0_mov_idx_list.append(mov_i)

        while not rock.landed:
            if movements[mov_i] == '>':
                rock.move_right_by_gas_jet(chamber)
            elif movements[mov_i] == '<':
                rock.move_left_by_gas_jet(chamber)
            mov_i = (mov_i + 1) % len(movements)
            rock.fall(chamber)

        chamber.update()

sequence = find_sequence_loop()
print(sequence)
total_rocks = 1_000_000_000_000
rocks_after_start_loop = total_rocks - sequence["before_start"]
total_loops = rocks_after_start_loop // sequence["delta_r"]
print(total_loops)
remaining_rocks = rocks_after_start_loop % sequence["delta_r"]


chamber.clean()
mov_i = 0
for r in range(sequence["before_start"] + remaining_rocks):
    rock_n = r % 5    
    rock = rocks[rock_n]
    rock.spawn(chamber)

    while not rock.landed:
        if movements[mov_i] == '>':
            rock.move_right_by_gas_jet(chamber)
        elif movements[mov_i] == '<':
            rock.move_left_by_gas_jet(chamber)
        mov_i = (mov_i + 1) % len(movements)
        rock.fall(chamber)

    chamber.update()
print(chamber.top)

final_h = (total_loops) * sequence["delta_h"] + chamber.top
print(final_h)
