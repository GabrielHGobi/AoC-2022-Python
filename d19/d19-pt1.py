from dataclasses import dataclass

@dataclass
class Resource:
    ore: int
    clay: int
    obsidian: int
    geode: int

    def __sub__(self, other):
        return Resource(self.ore - other.ore, self.clay - other.clay, self.obsidian - other.obsidian, self.geode - other.geode)
    
    def __add__(self, other):
        return Resource(self.ore + other.ore, self.clay + other.clay, self.obsidian + other.obsidian, self.geode + other.geode)
    
    def __ge__(self, other):
        difference = self - other
        if difference.ore >= 0  and difference.clay >= 0 and difference.obsidian >= 0 and difference.geode >= 0:
            return True
        return False

class Robots(Resource):
    def __init__(self, ore, clay, obsidian, geode):
        super().__init__(ore, clay, obsidian, geode)

class Blueprint:
    def __init__(self, id: int, ore_robot_cost: Resource, clay_robot_cost: Resource, obsidian_robot_cost: Resource, geode_robot_cost: Resource):
        self.id = id
        self.ore_robot_cost = ore_robot_cost
        self.clay_robot_cost = clay_robot_cost
        self.obsidian_robot_cost = obsidian_robot_cost
        self.geode_robot_cost = geode_robot_cost

    def get_max_number_of_geodes_that_can_be_opened(self, time) -> int:
        
        def backtracking_search(time, initial_sack: Resource, initial_robots: Robots) -> int:
            return recursive_backtracking_search(time, initial_sack, initial_robots)
        
        def recursive_backtracking_search(time, sack: Resource, robots: Robots) -> int:
            if time == 0:
                return sack.geode
            else:
                # produce new robots, if possible, or dont
                make_geode_robot_result = -1
                if sack >= self.geode_robot_cost and not sack - robots >= self.geode_robot_cost:
                    new_sack = sack - self.geode_robot_cost
                    new_sack += robots
                    make_geode_robot_result = recursive_backtracking_search(time - 1, new_sack, robots + Robots(0, 0, 0, 1))
                    return make_geode_robot_result
                
                make_obsidian_robot_result = -1
                if sack >= self.obsidian_robot_cost and robots.obsidian < self.geode_robot_cost.obsidian and not sack - robots >= self.obsidian_robot_cost:
                    new_sack = sack - self.obsidian_robot_cost
                    new_sack += robots
                    make_obsidian_robot_result = recursive_backtracking_search(time - 1, new_sack, robots + Robots(0, 0, 1, 0))
                
                make_clay_robot_result = -1
                if sack >= self.clay_robot_cost and robots.clay < self.obsidian_robot_cost.clay and not sack - robots >= self.clay_robot_cost:
                    new_sack = sack - self.clay_robot_cost
                    new_sack += robots
                    make_clay_robot_result = recursive_backtracking_search(time - 1, new_sack, robots + Robots(0, 1, 0, 0))
                
                make_ore_robot_result = -1
                if sack >= self.ore_robot_cost and not sack - robots >= self.ore_robot_cost:
                    new_sack = sack - self.ore_robot_cost
                    new_sack += robots
                    make_ore_robot_result = recursive_backtracking_search(time - 1, new_sack , robots + Robots(1, 0, 0, 0))

                dont_purchase_robot_result = recursive_backtracking_search(time -1, sack + robots, robots)
            
                return max(make_obsidian_robot_result, make_clay_robot_result, make_ore_robot_result, dont_purchase_robot_result)

        initial_sack = Resource(0, 0, 0, 0)
        initial_robots = Robots(1, 0, 0, 0)

        return backtracking_search(time, initial_sack, initial_robots)

    def get_quality_level(self, time):
        return self.id * self.get_max_number_of_geodes_that_can_be_opened(time)

blueprints = []
with open("./input.txt", "r") as f:
    while True:
        line = f.readline().replace('\n', '')
        if not line:
            break

        blueprint_id, receipt_list = line.split(':')
        
        id = int(blueprint_id.split()[1])
        receipts = [receipt.strip() for receipt in receipt_list.split('.')[:-1]]
        ore_robot_receipt = receipts[0].split()
        ore_robot_cost = Resource(int(ore_robot_receipt[4]), 0, 0, 0)

        clay_robot_receipt = receipts[1].split()
        clay_robot_cost = Resource(int(clay_robot_receipt[4]), 0, 0, 0)

        obsidian_robot_receipt = receipts[2].split()
        obsidian_robot_cost = Resource(int(obsidian_robot_receipt[4]), int(obsidian_robot_receipt[7]), 0, 0)

        geode_robot_receipt = receipts[3].split()
        geode_robot_cost = Resource(int(geode_robot_receipt[4]), 0, int(geode_robot_receipt[7]), 0)

        blueprints.append(Blueprint(id, ore_robot_cost, clay_robot_cost, obsidian_robot_cost, geode_robot_cost))

sum = 0
for blueprint in blueprints:
    a =  blueprint.get_quality_level(24)
    print(f'For Blueprint {blueprint.id}, the QL = {a}')
    sum += a
print(sum)


    