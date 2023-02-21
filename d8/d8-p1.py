with open("./input.txt", "r") as f:
    map_lines = f.readlines()

class Forest:
    def __init__(self, lines):
        self.n = len(lines)
        self.map = [ [ None for _ in range(self.n) ] for _ in range(self.n) ]
        self._generate_map(lines)
        self._find_tallest_trees_in_rows_and_columns()
        self._update_all_tree_visibility()

    def _generate_map(self, lines):
        for i in range(self.n):
            for j in range(self.n):
                self.map[i][j] = Tree(int(lines[i][j]))
    
    def _find_tallest_trees_in_rows_and_columns(self):
        # rows
        for i in range(self.n):
            
            # W -> E
            for j in range(1, self.n):
                self.map[i][j].tallest_W = max([self.map[i][j-1].h, self.map[i][j-1].tallest_W])

            # W <- E
            for j in range(self.n-2, -1, -1):
                self.map[i][j].tallest_E = max([self.map[i][j+1].h, self.map[i][j+1].tallest_E])

        # columns
        for j in range(self.n):
            
            # N -> S
            for i in range(1, self.n):
                self.map[i][j].tallest_N = max([self.map[i-1][j].h, self.map[i-1][j].tallest_N])

            # N <- S
            for i in range(self.n-2, -1, -1):
                self.map[i][j].tallest_S = max([self.map[i+1][j].h, self.map[i+1][j].tallest_S])

    def _update_all_tree_visibility(self):
        for i in range(self.n):
            for j in range(self.n):
                self.map[i][j].set_visibility()

    def get_visible_trees(self):
        count = 0
        for i in range(self.n):
            for j in range(self.n):
                if self.map[i][j].visible:
                    count += 1
        return count

    def print_visibility(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.map[i][j].visible:
                    print('1', end=' ')
                else:
                    print('0', end=' ')
            print()

    def print_heigths(self):
        for i in range(self.n):
            for j in range(self.n):
                print(self.map[i][j].h, end=' ')
            print()


class Tree:
    def __init__(self, height):
        self.h = height
        self.tallest_N = -1
        self.tallest_S = -1
        self.tallest_W = -1
        self.tallest_E = -1
        self.visible = False
    
    def set_visibility(self):
        if self.tallest_N == -1 or \
        self.tallest_S == -1 or \
        self.tallest_W == -1 or \
        self.tallest_E == -1:
            self.visible = True
            pass

        if self.h > self.tallest_N or \
        self.h > self.tallest_S or \
        self.h > self.tallest_W or \
        self.h > self.tallest_E:
            self.visible = True
            pass


f = Forest(map_lines)
print(f.get_visible_trees())


        
