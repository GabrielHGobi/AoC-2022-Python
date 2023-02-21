class Pair:
    def __init__(self, left, right):
        self.left = MyList(left)
        print(self.left.l)
        self.right = MyList(right)
        print(self.right.l)
        self.is_correct = self.left < self.right
        if self.is_correct:
            print("Correct!")
        else:
            print("No :(")
        print()

class MyList:
    def __init__(self, list_str: str):
        tokens = self._parse_str(list_str)
        def new_list(tok_i):
            l = []
            tok_i += 1
            tok = tokens[tok_i]
            while tok != ']':
                if tok == '[':
                    l_inside, tok_i = new_list(tok_i)
                    l.append(l_inside)
                else:
                    l.append(int(tok))
                tok_i += 1
                tok = tokens[tok_i]
            return l, tok_i

        self.l = new_list(0)[0]
        
    def _parse_str(self, list_str:str):
        tokens = list_str.replace('[', '[,').replace(']', ',]').replace(' ', '').split(',')
        while True:
            try:
                tokens.remove('')
            except ValueError:
                break
        return tokens

    def __lt__(self, other):
        other_l = None
        
        if isinstance(other, MyList):
            other_l = other.l
        elif isinstance(other, list):
            other_l = other

        if isinstance(other_l, list):
            for i in range(len(self.l)):
                
                if i >= len(other_l):
                    return False

                # print(self.l[i], other_l[i])    

                if isinstance(other_l[i], list):
                    if MyList(str(other_l[i])) < self.l[i]:
                        return False

                elif isinstance(other_l[i], int):
                    if isinstance(self.l[i], int):
                        if self.l[i] > other_l[i]:
                            return False
                        elif self.l[i] < other_l[i]:
                            return True
                    elif isinstance(self.l[i], list):
                        if not MyList(str(self.l[i])) < other_l[i]:
                            return False
                        elif MyList(str(self.l[i])) < other_l[i]:
                            return True
            
            if len(self.l) < len(other_l):
                return True

            return False
        
        if isinstance(other, int):
            return self < MyList(str([other]))


with open("./input.txt", "r") as f:
    all_pairs = []
    while True:
        line = f.readline()
        if not line:
            break
        if line == '\n':
            continue
        left = line.replace('\n', '')
        right = f.readline().replace('\n', '')
        all_pairs.append(Pair(left, right))


sum = 0
for i in range(len(all_pairs)):
    pair = all_pairs[i]
    if pair.is_correct:
        sum += i+1
print(sum)
