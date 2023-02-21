import math

all_monkey_notes = []
with open("./input.txt", "r") as f:
    monkey_notes = []
    while True:
        line = f.readline()
        if line != '\n':
            monkey_notes.append(line.replace(',', '').split())
        else:
            all_monkey_notes.append(monkey_notes)
            monkey_notes = []
        if not line:
            break

# print(all_monkey_notes)

class Monkey:
    def __init__(self, notes):
        self.items = []
        self.inspec_items_count = 0
        self.operation = dict.fromkeys(['operator', 'value'])
        self.test =  dict.fromkeys(['div', 'if_true', 'if_false'])

        starting_items = notes[1]
        for i in range(2, len(starting_items)):
            self.items.append(int(starting_items[i]))

        operation = notes[2]
        self.operation['operator'] = operation[4]
        if operation[5] == 'old':
            self.operation['value'] = 'old'
        else:
            self.operation['value'] = int(operation[5])

        self.test['div'] = int(notes[3][3])
        self.test['if_true'] = int(notes[4][5])
        self.test['if_false'] = int(notes[5][5])

    def inspect_and_throw(self):
        item = self.items.pop(0)
        monkey_to = None
        if self.operation['operator'] == '*':
            if self.operation['value'] == 'old':
                item *= item
            else:
                item *= self.operation['value']
            
        elif self.operation['operator'] == '+':
            if self.operation['value'] == 'old':
                item += item
            else:
                item += self.operation['value']
        else:
            print("unrecognized operator")
        
        self.inspec_items_count += 1

        was_true = False
        if item % self.test['div'] == 0:
            monkey_to = self.test['if_true']
            was_true = True
        else:
            monkey_to = self.test['if_false']
            
        return item, monkey_to, was_true


monkeys = [Monkey(notes) for notes in all_monkey_notes]

product_of_tests = 1
for monkey in monkeys:
    product_of_tests *= monkey.test['div']

for r in range(10000):
    for m in range(len(monkeys)):
        monkey = monkeys[m]
        while monkey.items:
            item, monkey_to, was_true = monkey.inspect_and_throw()
            monkeys[monkey_to].items.append(item % product_of_tests)
        
    
    if r+1 == 1 or r+1 == 20 or (r+1) % 1000 == 0:
        print(f'== After round {r+1} ==')
        for m in range(len(monkeys)):
            print(f'Monkey {m} inspected items {monkeys[m].inspec_items_count} times')
        print()

inspec_count_list = []
for m in range(len(monkeys)):
    # print(f'Monkey {m} inspected items {monkeys[m].inspec_items_count} times')
    inspec_count_list.append(monkeys[m].inspec_items_count)

inspec_count_list.sort(reverse=True)
monkey_business = inspec_count_list[0] * inspec_count_list[1]

print(monkey_business)