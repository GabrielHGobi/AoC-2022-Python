with open("./input.txt", "r") as f:
    lines = f.readlines()

board_map = lines[:-2]
path = lines[-1].replace('\n', '')


EMPTY_TILE =  ' '
OPEN_TYLE = '.'
SOLID_WALL = '#'


class Position:
    def __init__(self, row: int, column: int, facing: chr) -> None:
        if not facing == 'v' and not facing == '^' and not facing == '>' and not facing == '<':
            raise Exception("Invalid facing direction")
        self.row = row
        self.column = column
        self.facing = facing
    
    def __repr__(self) -> str:
        return f'({self.row}, {self.column}), {self.facing}'

    def move(self, board) -> None: 
        if self.facing == '>':
            next_column = 1 + self.column % board.M
            while board.map[self.row][next_column] == EMPTY_TILE:
                next_column = 1 + next_column % board.M
            if board.map[self.row][next_column] == OPEN_TYLE:
                self.column = next_column
            elif board.map[self.row][next_column] == SOLID_WALL:
                return

        elif self.facing == '<':
            next_column = (self.column - 2) % board.M + 1
            while board.map[self.row][next_column] == EMPTY_TILE:
                next_column = (next_column - 2) % board.M + 1    
            if board.map[self.row][next_column] == OPEN_TYLE:
                self.column = next_column
            elif board.map[self.row][next_column] == SOLID_WALL:
                return

        elif self.facing == 'v':
            next_row = 1 + self.row % board.N
            while board.map[next_row][self.column] == EMPTY_TILE:
                next_row = 1 + next_row % board.N
            if board.map[next_row][self.column] == OPEN_TYLE:
                self.row = next_row
            elif board.map[next_row][self.column] == SOLID_WALL:
                return

        else:
            next_row = (self.row - 2) % board.N + 1
            while board.map[next_row][self.column] == EMPTY_TILE:
                next_row = (next_row - 2) % board.N + 1
            if board.map[next_row][self.column] == OPEN_TYLE:
                self.row = next_row
            elif board.map[next_row][self.column] == SOLID_WALL:
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
        for line in board_map:
            self.M = max(self.M, len(line.replace('\n', '')))
        self.map = [ [EMPTY_TILE for _ in range(self.M + 1)] for _ in range(self.N + 1)]
        self._construct_board(board_map)

    def _construct_board(self, board_map) -> None:
        for i in range(1, self.N + 1):
            line = board_map[i-1].replace('\n', '')
            for j in range(1, len(line) + 1):
                self.map[i][j] = line[j-1]

    def __repr__(self) -> str:
        board_str = ''
        for i in range(1, self.N + 1):
            for j in range(1, self.M + 1):
                board_str += self.map[i][j]
            board_str += '\n'
        return board_str
    
    def get_initial_pos(self) -> Position:
        for j in range(1, self.M + 1):
            if self.map[1][j] == OPEN_TYLE:
                return Position(1, j, '>')
    
board = Board(board_map)

my_pos = board.get_initial_pos()

my_pos.move_through_path(path, board)

print(my_pos.get_final_password())