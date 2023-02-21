import math

class Node:
    def __init__(self, value) -> None:
        self.v = value
        self.next = None
        self.prev = None

    def move_in_the_circular_list(self, value, dir: str):
        if dir != "forward" and dir != "backward":
            raise Exception("dir not allowed")
        
        p = self
        q = self.prev
        q.next = p.next
        q = p.next
        q.prev = p.prev

        if dir == "forward":
            for _ in range(value):
                p = p.next
            q = p.next
            p.next = self
            self.prev = p
            q.prev = self
            self.next = q
        elif dir == "backward":
            for _ in range(value):
                p = p.prev
            q = p.prev
            p.prev = self
            self.next = p
            q.next = self
            self.prev = q

    def get_value_after(self, value, dir):
        if dir != "forward" and dir != "backward":
            raise Exception("dir not allowed")
        
        p = self
        if dir == "forward":
            for _ in range(value):
                p = p.next
        elif dir == "backward":
            for _ in range(value):
                p = p.prev
        return p.v

nodes = []
zero_idx = None
with open("./input.txt", "r") as f:
    while True:
        line = f.readline().replace('\n', '')
        if not line:
            break
        value = int(line)
        nodes.append(Node(value))
        if value == 0:
            zero_idx = len(nodes) - 1

N = len(nodes)
nodes[0].prev = nodes[N-1]
nodes[0].next = nodes[1]
nodes[N-1].prev = nodes[N-2]
nodes[N-1].next = nodes[0]
for i in range(1, N-1):
    nodes[i].prev = nodes[i-1]
    nodes[i].next = nodes[i+1]

for i in range(N):
    value = nodes[i].v

    if value > 0:
        nodes[i].move_in_the_circular_list(value, "forward")

    elif value < 0:
        nodes[i].move_in_the_circular_list(abs(value), "backward")

sum = 0
for value in [1000, 2000, 3000]:
    number = None
    value = value % N
    number = nodes[zero_idx].get_value_after(value, "forward")
    sum += number
print(sum)


