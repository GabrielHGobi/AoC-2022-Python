with open("input.txt", "r") as f:
    lines = f.readlines()

rounds = []

for line in lines:
    rounds.append(line.split())

total_score = 0
shape_score = {'A': 1, 'B': 2, 'C': 3}
to_win = {'A': 'B', 'B': 'C', 'C': 'A'}
to_lose = {'A': 'C', 'B': 'A', 'C': 'B'}

for round in rounds:
    my_play = 'A'
    if round[1] == 'X': # loss
        total_score += 0
        my_play = to_lose[round[0]]
    if round[1] == 'Y': # draw
        total_score += 3
        my_play = round[0]
    if round[1] == 'Z': # win
        total_score += 6
        my_play = to_win[round[0]]

    total_score += shape_score[my_play]

print(total_score)