with open("input.txt", "r") as f: 
    inital_stack_lines = []
    initial_stack_ended = False
    moves_lines = []
    while True:
        line = f.readline()
        if not line:
            break
        
        if line == '\n':
            initial_stack_ended = True
            continue
        
        if not initial_stack_ended:
            inital_stack_lines.append(line.replace('\n', ''))
        else:
            moves_lines.append(line.replace('\n', '').split())

n_stacks = len(inital_stack_lines[-1].split())

# creating an utility class for the stacks 
class Stack:
    def __init__(self):
        self.s = []
    
    def top(self):
        if not self.is_empty():
            return self.s[-1]
    
    def is_empty(self):
        if not self.s:
            return True
        return False

    def pop(self):
        if not self.is_empty():
            del self.s[-1]

    def push(self, el):
        self.s.append(el)

# filling the stacks with the initial crates
stacks = [Stack() for i in range(n_stacks)]
for i in range(len(inital_stack_lines) - 2, -1, -1):
    line = inital_stack_lines[i]
    for s in range(n_stacks):
        if line[1 + s * 4] != ' ':
            stacks[s].push(line[1 + s * 4])

for line in moves_lines:
    from_s = int(line[3]) - 1
    to_s = int(line[5]) - 1
    crates_to_move = int(line[1])

    for crate in range(crates_to_move):
        el = stacks[from_s].top()
        stacks[to_s].push(el)
        stacks[from_s].pop()

for s in stacks:
    print(s.top(), end='')
print()


