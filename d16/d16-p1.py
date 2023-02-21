from queue import PriorityQueue
from dataclasses import dataclass

INF = 9999999999
UNDEF = -1

with open("./input.txt", "r") as f:
    lines = f.readlines()

class Valve:
    def __init__(self, name, fr, to_list):
        self.name = name
        self.fr = fr
        self._to_valves = to_list
        self.is_open = False
        self.dist_table = {}
    
    def get_neighboors(self):
        return self._to_valves
    
class Network:
    def __init__(self):
        self.valves = {}
        self.pressure_realesed = 0
    
    def add_valve(self, name, fr, to_list):
        self.valves[name] = Valve(name, fr, to_list)
        
    def open_valve(self, name):
        self.valves[name].is_open = True

    def get_valve(self, name):
        return self.valves[name]

    def construct_djkistra_dist_table(self):
        for valve_name in self.valves.keys():

            start = self.get_valve(valve_name)
            costs = dict.fromkeys(self.valves.keys(), INF)
            visited = dict.fromkeys(self.valves.keys(), False)
            pq = PriorityQueue()
            pq.put((0, start.name))

            while not pq.empty():
                (cost, curr_valve) = pq.get()
                if not visited[curr_valve]:
                    visited[curr_valve] = True
                    costs[curr_valve] = cost
                for neighbor in self.valves[curr_valve].get_neighboors():
                    if not visited[neighbor]:
                        if cost + 1 < costs[neighbor]:
                            pq.put((cost+1, neighbor))

            start.dist_table = costs.copy()


net = Network()
for line in lines:
    line = line.replace('\n', '')
    valve_name_and_fr, tunnels_map = line.split(';')
    name = valve_name_and_fr.split()[1]
    fr = int(valve_name_and_fr.split()[-1].split('=')[-1])
    to_list = tunnels_map.replace(',', '').split()[4:]
    net.add_valve(name, fr, to_list)

net.construct_djkistra_dist_table()

@dataclass
class TableItem:
    pr: int # pressure released
    fr: int # flow rate
    v_open: set # valves_opened

def dynamic_programming_strategy(network: Network, start: str, time: int):
    # initializing table
    N_valves = len(network.valves.keys())
    valves_names_list = list(network.valves.keys())
    i_to_valve_n_map = {}
    for i in range(len(valves_names_list)):
        i_to_valve_n_map[i] = valves_names_list[i]
    valve_n_to_i_map = dict((v, k) for k, v in i_to_valve_n_map.items())

    table = [ [TableItem(UNDEF, 0, set()) for _ in range(time+1)] for _ in range(N_valves)]
   
    # start value
    for i in range(len(valves_names_list)):
        if valves_names_list[i] == start:
            table[i][0].pr = 0
    
    for t in range(time+1):
        for i in range(len(valves_names_list)):
            valve_n = i_to_valve_n_map[i]
            
            if table[i][t].pr != UNDEF:

                curr_fr = table[i][t].fr
                curr_pr = table[i][t].pr
                valve = network.get_valve(valve_n)
                for next_v_n in valve.dist_table.keys():
                    d = valve.dist_table[next_v_n]
                    next_v = network.get_valve(next_v_n)
                    next_i = valve_n_to_i_map[next_v_n]
                    if not next_v_n in table[i][t].v_open:
                        if t + d + 1 <= time:
                            if curr_pr + next_v.fr * (time - t - d - 1) > table[next_i][t+d+1].pr:
                                table[next_i][t+d+1].pr = curr_pr + next_v.fr * (time - t - d - 1)
                                table[next_i][t+d+1].fr = curr_fr + next_v.fr
                                table[next_i][t+d+1].v_open = table[i][t].v_open.copy()
                                table[next_i][t+d+1].v_open.add(next_v_n)

    all_pr = [ [UNDEF for _ in range(time+1)] for _ in range(N_valves)]
    for i in range(len(valves_names_list)):
        for t in range(time+1): 
            all_pr[i][t] = table[i][t].pr

    return max(map(max, all_pr))  

print(dynamic_programming_strategy(net, 'AA', 30))

        





