with open("./input.txt", "r") as f:
    lines = f.readlines()

class CPU:
    def __init__(self):
        self.x = 1
        self.history = []

    def noop(self):
        self.history.append(self.x)
    
    def addx(self, value):
        self.history.append(self.x)
        self.x += value
        self.history.append(self.x)

    def signal_strength_during(self, clock_cycle):
        return self.history[clock_cycle-2] * clock_cycle

cpu = CPU()
for line in lines:
    command = line.split()
    if command[0] == 'noop':
        cpu.noop()
    else:
        cpu.addx(int(command[1]))

print("At 20th:", cpu.signal_strength_during(20))
print("At 60th:", cpu.signal_strength_during(60))
print("At 100th:", cpu.signal_strength_during(100))
print("At 140th:", cpu.signal_strength_during(140))
print("At 180th:", cpu.signal_strength_during(180))
print("At 220th:", cpu.signal_strength_during(220))

sum = 0
for cycle in range(20, 221, 40):
    sum += cpu.signal_strength_during(cycle)
print("\nSum:", sum)


