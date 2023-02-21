# HARDCODED TO WORK JUST FOR PART 2 INPUT

with open("./input.txt", "r") as f:
    lines = f.readlines()

board_map = lines[:-2]
path = lines[-1].replace('\n', '')


EMPTY_TILE =  ' '
OPEN_TYLE = '.'
SOLID_WALL = '#'


class Position:
    def __init__(self, row: int, column: int, facing: chr, face_num: int) -> None:
        if not facing == 'v' and not facing == '^' and not facing == '>' and not facing == '<':
            raise Exception("Invalid facing direction")
        self.row = row
        self.column = column
        self.facing = facing
        self.face_num = face_num
        self.f_row = (row - 1) % 50 + 1
        self.f_column = (column - 1) % 50 + 1
    
    def __repr__(self) -> str:
        return f'({self.row}, {self.column}), {self.facing}'

    def move(self, board) -> None: 
        if self.facing == '>':
            next_column = 1 + self.column % board.M
            if board.map[self.row][next_column][0] == EMPTY_TILE:
                warp_map = {2: 5, 3: 2, 5: 2, 6: 5}
                self.warp_to(board, warp_map[self.face_num])
            elif board.map[self.row][next_column][0] == OPEN_TYLE:
                self.column = next_column
                self.f_column = 1 + self.f_column % 50
                self.face_num = board.map[self.row][next_column][1]
            elif board.map[self.row][next_column][0] == SOLID_WALL:
                return

        elif self.facing == '<':
            next_column = (self.column - 2) % board.M + 1
            if board.map[self.row][next_column][0] == EMPTY_TILE:
                warp_map = {1: 4, 3: 4, 4: 1, 6: 1}
                self.warp_to(board, warp_map[self.face_num])  
            elif board.map[self.row][next_column][0] == OPEN_TYLE:
                self.column = next_column
                self.f_column = (self.f_column - 2) % 50 + 1
                self.face_num = board.map[self.row][next_column][1]
            elif board.map[self.row][next_column][0] == SOLID_WALL:
                return

        elif self.facing == 'v':
            next_row = 1 + self.row % board.N
            if board.map[next_row][self.column][0] == EMPTY_TILE:
                warp_map = {2: 3, 5: 6, 6: 2}
                self.warp_to(board, warp_map[self.face_num])  
            elif board.map[next_row][self.column][0] == OPEN_TYLE:
                self.row = next_row
                self.f_row = 1 + self.f_row % 50
                self.face_num = board.map[next_row][self.column][1]
            elif board.map[next_row][self.column][0] == SOLID_WALL:
                return

        else:
            next_row = (self.row - 2) % board.N + 1
            if board.map[next_row][self.column][0] == EMPTY_TILE:
                warp_map = {1: 6, 2: 6, 4: 3}
                self.warp_to(board, warp_map[self.face_num])  
            elif board.map[next_row][self.column][0] == OPEN_TYLE:
                self.row = next_row
                self.f_row = (self.f_row - 2) % 50 + 1
                self.face_num = board.map[next_row][self.column][1]
            elif board.map[next_row][self.column][0] == SOLID_WALL:
                return

    def rotate(self, dir: chr) -> None:
        if not dir == 'R' and not dir == 'L':
            raise Exception("Invalid rotation direction")
        if dir == 'R':
            clockwise_order = {'>': 'v', 'v': '<', '<': '^', '^': '>'}
            self.facing = clockwise_order[self.facing]
        else:
            counterclockwise_order = {'>': '^', 'v': '>', '<': 'v', '^': '<'}
            self.facing = counterclockwise_order[self.facing]

    def warp_to(self, board, to_face: int) -> None:
        if self.face_num == 1:
            if to_face == 6:
                next_f_row = self.f_column
                next_f_column = 1
                next_facing = '>'
            elif to_face == 4:
                next_f_row = 51 - self.f_row
                next_f_column = 1
                next_facing = '>'
        elif self.face_num == 2:
            if to_face == 6:
                next_f_column = self.f_column
                next_f_row = 50
                next_facing = '^'
            elif to_face == 5:
                next_f_row = 51 - self.f_row
                next_f_column = 50
                next_facing = '<'
            elif to_face == 3:
                next_f_row = self.f_column
                next_f_column = 50
                next_facing = '<'
        elif self.face_num == 3:
            if to_face == 2:
                next_f_column = self.f_row
                next_f_row = 50
                next_facing = '^'
            elif to_face == 4:
                next_f_row = 1
                next_f_column = self.f_row
                next_facing = 'v'
        elif self.face_num == 4:
            if to_face == 1:
                next_f_column = 1
                next_f_row = 51 - self.f_row
                next_facing = '>'
            elif to_face == 3:
                next_f_row = self.f_column
                next_f_column = 1
                next_facing = '>'
        elif self.face_num == 5:
            if to_face == 2:
                next_f_column = 50
                next_f_row = 51 - self.f_row
                next_facing = '<'
            elif to_face == 6:
                next_f_row = self.f_column
                next_f_column = 50
                next_facing = '<'
        elif self.face_num == 6:
            if to_face == 5:
                next_f_column = self.f_row
                next_f_row = 50
                next_facing = '^'
            elif to_face == 2:
                next_f_row = 1 
                next_f_column = self.f_column 
                next_facing = 'v'
            elif to_face == 1:
                next_f_row = 1
                next_f_column = self.f_row
                next_facing = 'v'

        face_origin = {1: (0, 50), 2: (0, 100), 3: (50, 50), 4: (100, 0), 5: (100, 50), 6: (150, 0)}
        next_row = face_origin[to_face][0] + next_f_row
        next_column = face_origin[to_face][1] + next_f_column

        if board.map[next_row][next_column][0] == SOLID_WALL:
            return
        else:
            self.row = next_row
            self.column = next_column
            self.facing = next_facing
            self.face_num = to_face
            self.f_row = next_f_row
            self.f_column = next_f_column


    def move_through_path(self, path: str, board) -> None:
        path = path.replace('R', ',R,').replace('L', ',L,')
        path_commands = path.split(',')
        for command in path_commands:
            if command == 'L' or command == 'R':
                dir = command
                self.rotate(dir)
            else:
                steps = int(command)
                for _ in range(steps):
                    self.move(board)

    def get_final_password(self) -> int:
        facing_score_table = {'>': 0, 'v': 1, '<': 2, '^': 3}
        return 1000 * self.row + 4 * self.column + facing_score_table[self.facing]

    


class Board:
    def __init__(self, board_map) -> None:
        self.N = len(board_map)
        self.M = -1
        self.cube_size = 50
        for line in board_map:
            self.M = max(self.M, len(line.replace('\n', '')))
        self.map = [ [[EMPTY_TILE, ' '] for _ in range(self.M + 2)] for _ in range(self.N + 2)]
        self._construct_board(board_map)
        self._mark_face_numbers()

    def _construct_board(self, board_map) -> None:
        for i in range(1, self.N + 1):
            line = board_map[i-1].replace('\n', '')
            for j in range(1, len(line) + 1):
                if line[j-1] != EMPTY_TILE:
                    self.map[i][j] = [line[j-1], 0]

    def _mark_face_numbers(self):
        face_number = 1
        for i in range(1, self.N + 1):
            for j in range(1, self.M + 1):
                if self.map[i][j][1] == 0:

                    for k in range(i, i+self.cube_size):
                        for l in range(j, j+self.cube_size):
                            self.map[k][l][1] = face_number
                    face_number += 1

    def __repr__(self) -> str:
        board_str = ''
        for i in range(1, self.N + 1):
            for j in range(1, self.M + 1):
                board_str += self.map[i][j][0]
            board_str += '\n'
        board_str += '\n'
        for i in range(1, self.N + 1):
            for j in range(1, self.M + 1):
                board_str += f'{self.map[i][j][1]}'
            board_str += '\n'
        return board_str
    
    def get_initial_pos(self) -> Position:
        for j in range(1, self.M + 1):
            if self.map[1][j][0] == OPEN_TYLE:
                return Position(1, j, '>', self.map[1][j][1])
    
board = Board(board_map)

my_pos = board.get_initial_pos()

my_pos.move_through_path(path, board)

print(my_pos.get_final_password())