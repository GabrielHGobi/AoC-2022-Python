class Monkey:
    def __init__(self, name, yell_type) -> None:
        if yell_type != 'math_op' and yell_type != 'number':
            raise Exception(f'Invalid yell type for monkey {name}')   
        self.name = name
        self.yell_type = yell_type
    
    def yell(self, monkey_dict) -> int:
        return NotImplementedError()


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

monkey_graph = Graph()
with open("./input.txt", "r") as f:
    while True:
        line = f.readline()
        if not line:
            break
        name, yell = line.split(':')
        yell = yell.strip()
        monkey_graph.add_monkey(name, yell)

print(monkey_graph.make_monkey_yell("root"))