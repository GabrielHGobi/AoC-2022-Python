EMPTY = '.'

with open("./input.txt", "r") as f:
    scan_map = f.readlines()

class Elf:
    def __init__(self, i: int, j: int) -> None:
        self.i = i
        self.j = j
        self.proposed_dest = None
    
    def can_move(self, map):
        lookup_directions = [(1,0), (1,+1), (1,-1), (0,+1), (0,-1), (-1,0), (-1,+1), (-1,-1)]
        for (di, dj) in lookup_directions:
            if map[self.i + di][self.j + dj] != EMPTY:
                return True
        return False
    
    def propose(self, dir_list: list, map):
        for direction_try in dir_list:
            (direction, adjacent_positions) = list(direction_try.items())[0]
            found_dir = True
            for (di, dj) in adjacent_positions:
                if map[self.i + di][self.j + dj] != EMPTY:
                    found_dir = False
            if found_dir: 
                break
        
        if not found_dir:
            return None

        if direction == 'N':
            self.proposed_dest = (self.i - 1, self.j)
        elif direction == 'S':
            self.proposed_dest = (self.i + 1, self.j)
        elif direction == 'W':
            self.proposed_dest = (self.i, self.j - 1)
        elif direction == 'E':
            self.proposed_dest = (self.i, self.j + 1)

        return self.proposed_dest

    def move(self):
        self.i = self.proposed_dest[0]
        self.j = self.proposed_dest[1]
        self.proposed_dest = None
    
    def __repr__(self) -> str:
        return f'Elf at ({self.i}, {self.j})'

class Grove:
    def __init__(self, scan_map) -> None:
        self.N = len(scan_map)
        self.M = len(scan_map[0].replace('\n', ''))
        self.elves = []
        self.dir_list = [{'N': [(-1, 0), (-1, -1), (-1, +1)]},
                         {'S': [(+1, 0), (+1, +1), (+1, -1)]},
                         {'W': [(0, -1), (-1, -1), (+1, -1)]},
                         {'E': [(0, +1), (-1, +1), (+1, +1)]}]
        self.map = self._construct_map(scan_map)
    
    def do_one_search_round(self) -> bool:
        some_elf_try_to_move = False
        
        proposed_destinations = []
        for elf in self.elves:
            if elf.can_move(self.map):
                some_elf_try_to_move = True
                proposed_dest = elf.propose(self.dir_list, self.map)
                if not proposed_dest is None:
                    proposed_destinations.append((proposed_dest, elf))

        proposed_destinations.sort(key= lambda a: a[0])

        k = 0
        while k < len(proposed_destinations):
            if k < len(proposed_destinations) - 1 and proposed_destinations[k][0] == proposed_destinations[k+1][0]:
                while k < len(proposed_destinations) - 1 and proposed_destinations[k][0] == proposed_destinations[k+1][0]:
                    k = k + 1
            else:
                dest = proposed_destinations[k][0]
                elf = proposed_destinations[k][1]
                next_i = dest[0]
                next_j = dest[1]
                self.map[next_i][next_j] = self.map[elf.i][elf.j]
                self.map[elf.i][elf.j] = EMPTY
                elf.move()
            k = k + 1

        self._update_dir_list()
        self._update_map_size()

        return some_elf_try_to_move

    def do_many_search_rounds(self, rounds: int) -> None:
        print('== Initial State ==')
        print(self, end='\n\n')

        for r in range(rounds):
            if not self.do_one_search_round():
                break
            print(f'== End of Round {r+1} ==')
            print(self, end='\n\n')

    def get_search_rounds_until_stop(self) -> int:
        round_count = 0
        while True:
            round_count += 1
            if not self.do_one_search_round():
                break
        return round_count

    def get_empty_grounds(self) -> int:
        min_i, min_j = 99999999, 99999999
        max_i, max_j = -1, -1
        for i in range(self.N + 2):
            for j in range(self.M + 2):
                if self.map[i][j] != EMPTY:
                    min_i = min(i, min_i)
                    min_j = min(j, min_j)
                    max_i = max(i, max_i)
                    max_j = max(j, max_j)
        
        count = 0
        for i in range(min_i, max_i+1):
            for j in range(min_j, max_j+1):
                if self.map[i][j] == EMPTY:
                    count += 1
        return count

    def _update_dir_list(self) -> None:
        first_dir = self.dir_list.pop(0)
        self.dir_list.append(first_dir)

    def _update_map_size(self) -> None:
        # update on north
        for j in range(self.M + 2):
            if self.map[0][j] != EMPTY:
                self.map.insert(0, [EMPTY for _ in range(self.M + 2)])
                self.N += 1
                for elf in self.elves:
                    elf.i += 1
                break

        # update on south
        for j in range(self.M + 2):
            if self.map[-1][j] != EMPTY:
                self.map.append([EMPTY for _ in range(self.M + 2)])
                self.N += 1
                break
        
        # update on east
        for i in range(self.N + 2):
            if self.map[i][-1] != EMPTY:
                for line in self.map:
                    line.append(EMPTY)
                self.M += 1
                break
        
        # update on west
        for i in range(self.N + 2):
            if self.map[i][0] != EMPTY:
                for line in self.map:
                    line.insert(0, EMPTY)
                self.M += 1
                for elf in self.elves:
                    elf.j += 1
                break

    def _construct_map(self, scan_map):
        map = [ [EMPTY for _ in range(self.M + 2)] for _ in range(self.N + 2)]
        for i in range(self.N):
            line = scan_map[i].replace('\n', '')
            for j in range(self.M):
                if line[j] == '#':
                    elf = Elf(i+1, j+1)
                    map[i+1][j+1] = elf
                    self.elves.append(elf)
                else:
                    map[i+1][j+1] = EMPTY
        return map
    
    def __repr__(self) -> str:
        map_str = ''
        for i in range(self.N + 2):
            for j in range(self.M + 2):
                if self.map[i][j] == EMPTY:
                    map_str += '.'
                else:
                    map_str += '#'
            map_str += '\n'
        return map_str
    
grove = Grove(scan_map)

print(grove.get_search_rounds_until_stop())


