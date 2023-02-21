with open("./input.txt", "r") as f:
    lines = f.readlines()

class MovingObject:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.pos_hist = set()
        self.pos_hist.add((self.x, self.y))
    
    def move(self, direction):
        if direction == 'R':
            self.x += 1
        elif direction == 'U':
            self.y += 1
        elif direction == 'D':
            self.y -= 1
        elif direction == 'L':
            self.x -= 1
    
    def is_together(self, other):
        if abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1:
            return True
        return False 
    

    def go_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        if self._manhattan_dist(other) == 2:
            if dx > 0:
                self.x = other.x - 1
            elif dx < 0:
                self.x = other.x + 1
            
            if dy > 0:
                self.y = other.y - 1
            elif dy < 0:
                self.y = other.y + 1
        else:
            if dx > 0:
                if dy > 0:
                    self.x += 1
                    self.y += 1
                else:
                    self.x += 1
                    self.y -= 1
            else:
                if dy > 0:
                    self.x -= 1
                    self.y += 1
                else:
                    self.x -= 1
                    self.y -= 1
            
            

    def _manhattan_dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


rope = [MovingObject() for _ in range(10)]

for line in lines:
    dir, n = line.split()
    for i in range(int(n)):
        rope[0].move(dir)
        for i in range(1, 10):
            if not rope[i].is_together(rope[i-1]):
                rope[i].go_to(rope[i-1])
        rope[9].pos_hist.add((rope[9].x, rope[9].y))
        
print(len(rope[9].pos_hist))


