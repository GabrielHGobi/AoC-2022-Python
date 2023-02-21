with open("./input.txt", "r") as f:
    map_lines = f.readlines()

class Forest:
    def __init__(self, lines):
        self.n = len(lines)
        self.map = [ [ None for _ in range(self.n) ] for _ in range(self.n) ]
        self._generate_map(lines)

    def _generate_map(self, lines):
        for i in range(self.n):
            for j in range(self.n):
                self.map[i][j] = Tree(i, j, self.n, int(lines[i][j]))
    

    def calculate_scenic_score(self, t_i, t_j):
        h = self.map[t_i][t_j].h
        
        view_distance_N = 0
        if t_i != 0:
            for i in range(t_i - 1, -1, -1):
                if self.map[i][t_j].h < h:
                    view_distance_N += 1
                elif self.map[i][t_j].h >= h:
                    view_distance_N += 1
                    break
            
        view_distance_S = 0
        if t_i != self.n - 1:
            for i in range(t_i + 1, self.n):
                if self.map[i][t_j].h < h:
                    view_distance_S += 1
                elif self.map[i][t_j].h >= h:
                    view_distance_S += 1
                    break

        view_distance_E = 0
        if t_j != self.n - 1:
            for j in range(t_j + 1, self.n):
                if self.map[t_i][j].h < h:
                    view_distance_E += 1
                elif self.map[t_i][j].h >= h:
                    view_distance_E += 1
                    break

        view_distance_W = 0
        if t_j != 0:
            for j in range(t_j - 1, -1, -1):
                if self.map[t_i][j].h < h:
                    view_distance_W += 1
                elif self.map[t_i][j].h >= h:
                    view_distance_W += 1
                    break

        scenic_score = view_distance_N * view_distance_E * view_distance_S * view_distance_W
        return scenic_score

    def get_highest_scenic_score(self):
        highest = 0
        for i in range(self.n):
            for j in range(self.n):
                scenic_score_i_j = self.calculate_scenic_score(i, j)
                if scenic_score_i_j > highest:
                    highest = scenic_score_i_j
        return highest

    def print_heigths(self):
        for i in range(self.n):
            for j in range(self.n):
                print(self.map[i][j].h, end=' ')
            print()


class Tree:
    def __init__(self, i, j, n, height):
        self.i = i
        self.j = j
        self.n = n
        self.h = height

        


f = Forest(map_lines)
print(f.get_highest_scenic_score())
# f.print_heigths()
        
