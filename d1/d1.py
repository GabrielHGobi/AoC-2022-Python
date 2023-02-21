with open("./input.txt", "r") as f:
    lines = f.readlines()
    
elves_calories = []
calories_list = []

for line in lines:
    if line == '\n':
        elves_calories.append(sum(calories_list))
        calories_list = []
    else:
        calories_list.append(int(line))

elves_calories.sort(reverse=True)
three_most_calories = elves_calories[0] + elves_calories[1] + elves_calories[2]

print(f'{elves_calories[0]} + {elves_calories[1]} + {elves_calories[2]} = {three_most_calories}')