class Monkey:
    def __init__(self, name, yell_type) -> None:
        if yell_type != 'math_op' and yell_type != 'number':
            raise Exception(f'Invalid yell type for monkey {name}')   
        self.name = name
        self.yell_type = yell_type
    
    def yell(self, monkey_dict) -> int:
        return NotImplementedError()

    def depends_of(self) -> list:
        return []


class NumberMonkey(Monkey):
    def __init__(self, name, number) -> None:
        super().__init__(name, "number")
        if not isinstance(number, int):
            raise Exception(f'NumberMonkey {name} has to yell a int number if is its job')
        self.num = number
    
    def yell(self, monkey_dict) -> int:
        return self.num


class MathOpMonkey(Monkey):
    def __init__(self, name, left_monkey_name, op, right_monkey_name) -> None:
        super().__init__(name, "math_op")
        self.num = None
        self.left_monkey_name = left_monkey_name
        self.op = op
        self.right_monkey_name = right_monkey_name
    
    def yell(self, monkey_dict) -> int:
        if not self.num is None:
            return self.num
        else:
            left_value = monkey_dict[self.left_monkey_name].yell(monkey_dict)
            right_value = monkey_dict[self.right_monkey_name].yell(monkey_dict)
            if self.op == '+':
                self.num = left_value + right_value
            if self.op == '-':
                self.num = left_value - right_value
            if self.op == '*':
                self.num = left_value * right_value
            if self.op == '/':
                self.num = left_value / right_value
            return int(self.num)
        
    def depends_of(self) -> list:
        return [self.left_monkey_name, self.right_monkey_name]


class Graph:
    def __init__(self) -> None:
        self.g = {}

    def add_monkey(self, name, yell) -> None:
        yell_list = yell.split()
        if len(yell.split()) == 1:
            self.g[name] = NumberMonkey(name, int(yell_list[0]))
        else:
            self.g[name] = MathOpMonkey(name, yell_list[0], yell_list[1], yell_list[2])

    def make_monkey_yell(self, name):
        return self.g[name].yell(self.g)

    def answer_riddle(self) -> int:
        left_side, right_side = self.g["root"].depends_of()

        def DFS(start_name, end_name):
            stack = []
            
            def recursive_DFS(start_name, end_name):
                stack.append(start_name)
                if start_name == end_name:
                    return True
                found = False
                for monkey in self.g[start_name].depends_of():
                    found = recursive_DFS(monkey, end_name) or found
                    if found:
                        return True
                stack.pop()
                return False
            
            if recursive_DFS(start_name, end_name):
                return stack
            else:
                return None
        
        order = DFS(left_side, "humn")
        if order:
            humn_side = left_side
            other_side = right_side
        else: 
            humn_side = right_side
            other_side = left_side
            order = DFS(left_side, "humn")

        new_monkeys = dict.fromkeys(order, None)
        inverse_op = {'+': '-', '-': '+', '*': '/', '/': '*'}

        for m in range(len(order) - 1):

            curr_name = order[m]
            curr_monkey = self.g[curr_name]
            left_monkey, right_monkey = curr_monkey.depends_of()

            next_name = order[m+1]

            if left_monkey == next_name:
                other_monkey = right_monkey
            else:
                other_monkey = left_monkey

            if curr_monkey.op == '/' or curr_monkey.op == '-':
                if left_monkey == next_name:
                    new_monkeys[next_name] = MathOpMonkey(next_name, curr_name, inverse_op[curr_monkey.op], right_monkey)
                elif right_monkey == next_name:
                    new_monkeys[next_name] = MathOpMonkey(next_name, left_monkey, curr_monkey.op, curr_name)
            else:
                new_monkeys[next_name] = MathOpMonkey(next_name, curr_name, inverse_op[curr_monkey.op], other_monkey)

        other_side_value = self.make_monkey_yell(other_side)
        new_monkeys[humn_side] = NumberMonkey(humn_side, other_side_value)

        for name, monkey_obj in new_monkeys.items():
            self.g[name] = monkey_obj

        return self.make_monkey_yell("humn")


monkey_graph = Graph()
with open("./input.txt", "r") as f:
    while True:
        line = f.readline()
        if not line:
            break
        name, yell = line.split(':')
        yell = yell.strip()
        monkey_graph.add_monkey(name, yell)

print(monkey_graph.answer_riddle())