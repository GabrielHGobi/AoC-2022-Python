with open("input.txt", "r") as f:
    lines = f.readlines()

rounds = []

for line in lines:
    rounds.append(line.split())

total_score = 0
shape_score = {'A': 1, 'B': 2, 'C': 3}

def get_round_score(other_player, me):
    # is a draw?
    if other_player == me:
        return 3

    # who wins?    
    elif other_player == 'A': # rock
        if me == 'B': # paper
            return 6
        else:
            return 0
    elif other_player == 'B': # paper
        if me == 'C': # scissors
            return 6
        else:
            return 0
    elif other_player == 'C': # scissors
        if me == 'A': # rock
            return 6
        else:
            return 0

for round in rounds:
    # getting shape score and encrypting back to A, B, C notation
    if round[1] == 'X':
        round[1] = 'A'
    if round[1] == 'Y':
        round[1] = 'B'
    if round[1] == 'Z':
        round[1] = 'C'

    total_score += shape_score[round[1]]
    total_score += get_round_score(*round)

print(total_score)