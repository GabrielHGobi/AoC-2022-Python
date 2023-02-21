import functools

class Packet:
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
        # print(self, other)
        other_l = None
        if isinstance(other, Packet):
            other_l = other.l
        elif isinstance(other, list):
            other_l = other
        elif isinstance(other, int):
            # print('convert')
            return self < Packet(str([other]))

        for i in range(len(self.l)):
            

            # acabou a lista da direita primeiro? Então ela é menor
            if i >= len(other_l):
                return 1 # not right order

            # print(self.l[i], other_l[i])
            
            # int vs int -> resolução
            if isinstance(self.l[i], int) and isinstance(other_l[i], int):
                if self.l[i] < other_l[i]:
                    return -1 # right order
                elif self.l[i] > other_l[i]:
                    return 1 # not right order

            # list vs list -> recursão
            elif isinstance(self.l[i], list) and isinstance(other_l[i], list):
                comp = Packet(str(self.l[i])) < Packet(str(other_l[i]))
                if comp != 0: # comparision makes a decision
                    return comp
                else: # if not, continue the comparision
                    continue
            
            else: # exactly one value is an integer
                # print("convert!")
                if isinstance(self.l[i], int):
                    comp = Packet(str([self.l[i]])) < other_l[i]
                    if comp != 0:
                        return comp
                    else:
                        continue
                elif isinstance(other_l[i], int):
                    comp = Packet(str(self.l[i])) < Packet(str([other_l[i]]))
                    if comp != 0:
                        return comp
                    else:
                        continue
        
        # acabou a lista?
        if len(self.l) < len(other_l):
            return -1 # right order
        else:
            return 0 # same len        
    
    def __repr__(self):
        return self.l.__repr__()


with open("./input.txt", "r") as f:
    all_packets = []
    while True:
        line = f.readline()
        if not line:
            break
        if line == '\n':
            continue
        packet_str = line.replace('\n', '')
        all_packets.append(Packet(packet_str))

all_packets.append(Packet('[[2]]'))
all_packets.append(Packet('[[6]]'))

def compare(packet_x, packet_y):
    return packet_x < packet_y
    
all_packets.sort(key=functools.cmp_to_key(compare))


divider_packet_2_idx = 0
divider_packet_6_idx = 0

for p in range(len(all_packets)):
    packet = all_packets[p]
    # print(packet)
    if str(packet.l) == str([[2]]):
        divider_packet_2_idx = p + 1
    if str(packet.l) == str([[6]]):
        divider_packet_6_idx = p + 1

decoder_key = divider_packet_2_idx * divider_packet_6_idx
print(decoder_key)

