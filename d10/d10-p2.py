with open("./input.txt", "r") as f:
    lines = f.readlines()

class CPU:
    def __init__(self):
        self.x = 1
        self.history = [1, 1]

    def noop(self):
        self.history.append(self.x)
    
    def addx(self, value):
        self.history.append(self.x)
        self.x += value
        self.history.append(self.x)

    def X_during(self, clock_cycle):
        return self.history[clock_cycle]

class CRT:
    def __init__(self):
        self.clock = 0
        self.pos_at_row = -1
    
    def tick(self):
        self.clock += 1
        self.pos_at_row = (self.pos_at_row + 1) % 40
    
    def draw(self, cpu):
        self.tick()
        X_middle = cpu.X_during(self.clock)
        if X_middle -1 <= self.pos_at_row and self.pos_at_row <= X_middle + 1:
            print('#', end='')
        else:
            print('.', end='')
        if self.pos_at_row == 39:
            print() 

cpu = CPU()
crt = CRT()
for line in lines:
    command = line.split()
    if command[0] == 'noop':
        cpu.noop()
    else:
        cpu.addx(int(command[1]))

for cycle in range(1, 241):
    crt.draw(cpu)




