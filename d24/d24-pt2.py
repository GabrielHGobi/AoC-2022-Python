from queue import PriorityQueue
from copy import deepcopy

with open("./input.txt", "r") as f:
    map_scan = f.readlines()

WALL = '#'
EMPTY = 0

class Blizzard:
    def __init__(self, i, j, dir) -> None:
        if dir != '>' and dir != '<' and dir != '^' and dir != 'v':
            raise Exception(f"Invalid dir: {dir}")      
        self.i = i
        self.j = j
        self.dir = dir
    
    def move(self, map):
        map[self.i][self.j] -= 1

        if self.dir == '>':
            if map[self.i][self.j+1] == WALL:
                self.j = 1
                map[self.i][1] += 1
            else:
                map[self.i][self.j + 1] += 1
                self.j += 1

        elif self.dir == '<':
            if map[self.i][self.j-1] == WALL:
                self.j = len(map[self.i]) - 2
                map[self.i][-2] += 1
            else:
                map[self.i][self.j - 1] += 1
                self.j -= 1

        elif self.dir == '^':
            if map[self.i-1][self.j] == WALL:
                self.i = len(map) - 2
                map[-2][self.j] += 1
            else:
                map[self.i - 1][self.j] += 1
                self.i -= 1

        elif self.dir == 'v':
            if map[self.i+1][self.j] == WALL:
                self.i = 1
                map[1][self.j] += 1
            else:
                map[self.i + 1][self.j] += 1
                self.i += 1

        return map

    def get_pos(self):
        return (self.i, self.j)
    

class Agent:
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j

    def get_pos(self):
        return (self.i, self.j)
    
    def get_valid_positions_to_go(self, map):
        N, M = len(map), len(map[0])
        valid_pos_to_go = []
        valid_dir = [(+1, 0), (-1, 0), (0, +1), (0, -1)]
        for (di, dj) in valid_dir:
            next_i = self.i + di
            next_j = self.j + dj
            if next_i >= 0 and next_j >= 0 and next_i < N and next_j < M and map[next_i][next_j] == EMPTY:
                valid_pos_to_go.append(Agent(next_i, next_j))
        return valid_pos_to_go
    
    def can_wait(self, map) -> bool:
        if map[self.i][self.j] != EMPTY:
            return False
        return True
    
    def wait(self):
        return Agent(self.i, self.j)


class MapState:
    def __init__(self, blizzards: list, map) -> None:
        self._all_map_states = dict()
        self._all_map_states[0] = (map, blizzards)
    
    def update_blizzards(self, current_time):
        if not current_time + 1 in self._all_map_states.keys():
            (old_map, old_blizzards) = self._all_map_states[current_time]
            new_map = deepcopy(old_map)
            new_blizzards = deepcopy(old_blizzards)
            for blizzard in new_blizzards:
                new_map = blizzard.move(new_map)

            self._all_map_states[current_time + 1] = (new_map, new_blizzards)
        else:
            (new_map, new_blizzards) = self._all_map_states[current_time + 1]
        return new_map, new_blizzards
            

class State:
    def __init__(self, agent) -> None:
        self.agent = agent

    def __lt__(self, other):
        return 0


class Valley:
    def __init__(self, map_scan) -> None:
        self.start_pos = (0, 1)
        map, blizzards, self.end_pos = self._construct_map(map_scan)
        self.map_state = MapState(blizzards, map)

    def _construct_map(self, map_scan):
        blizzards = []
        map = [ [EMPTY for _ in range(len(map_scan[0].replace('\n', '')))] for _ in range(len(map_scan))]
        for i in range(len(map_scan)):
            line = map_scan[i]
            for j in range(len(line.replace('\n', ''))):
                if line[j] == WALL:
                    map[i][j] = WALL
                elif line[j] == '.':
                    continue
                else:
                    map[i][j] += 1
                    blizzards.append(Blizzard(i, j, line[j]))
        end_pos = (len(map) - 1, len(map[0]) - 2)
        return map, blizzards, end_pos
    
    def fastest_path_time(self, initial_time, start_pos, end_pos) -> int:
        
        print(f'Going from {start_pos} to {end_pos}')

        def get_manhattan_dist(pos1, pos2):
            return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

        agent = Agent(start_pos[0], start_pos[1])
        initial_state = State(agent)

        pq = PriorityQueue()
        visited = dict()
        pq.put(((initial_time, get_manhattan_dist(start_pos, end_pos)), initial_state))

        while not pq.empty():
            ((time, dist), state) = pq.get()
            
            if not (time, state.agent.get_pos()) in visited.keys():
                visited[(time, state.agent.get_pos())] = True
            else: 
                continue
            
            if state.agent.get_pos() == end_pos:
                return time

            next_map, _ = self.map_state.update_blizzards(time)
            for next_agent in state.agent.get_valid_positions_to_go(next_map):
                new_dist_to_end = get_manhattan_dist(next_agent.get_pos(), end_pos)

                if not (time + 1, next_agent.get_pos()) in visited.keys():
                    pq.put(((time + 1, new_dist_to_end), State(next_agent)))
            
            if state.agent.can_wait(next_map):
                next_agent = state.agent.wait()
                if not (time + 1, next_agent.get_pos()) in visited.keys():
                    pq.put(((time + 1, dist), State(next_agent)))





snow_valley = Valley(map_scan)
first_time = snow_valley.fastest_path_time(0, snow_valley.start_pos, snow_valley.end_pos)
print(first_time)
second_time = snow_valley.fastest_path_time(first_time, snow_valley.end_pos, snow_valley.start_pos)
print(second_time)
third_time = snow_valley.fastest_path_time(second_time, snow_valley.start_pos, snow_valley.end_pos)
print(third_time)
