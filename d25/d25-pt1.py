with open("./input.txt", "r") as f:
    lines = f.readlines()

def get_decimal(number_list):
    decimal = 0
    for j in range(max_len):
        power = max_len - 1 - j
        decimal += number_list[j] * pow(5, power)
    return decimal

max_len = -1
for line in lines:
    line = line.replace('\n', '')
    max_len = max(max_len, len(line))
max_len += 1

numbers = [ [0 for _ in range(max_len)] for _ in range(len(lines) + 1)]

for i in range(len(lines)):
    line = lines[i].replace('\n', '')
    for j in range(len(line)):
        if line[j] == '-':
            numbers[i][max_len - len(line) + j] = -1
        elif line[j] == '=':
            numbers[i][max_len - len(line) + j] = -2
        else:
            numbers[i][max_len - len(line) + j] = int(line[j])

for j in range(max_len):
    sum = 0
    for i in range(len(lines)):
        sum += numbers[i][j]
    numbers[len(lines)][j] = sum

result = numbers[len(lines)]

for i in range(len(result) - 1, -1, -1):
    digit = result[i]
    result[i-1] += digit // 5

    if digit % 5 <= 2:
        result[i] = digit % 5 
    else:
        result[i-1] += 1
        if digit % 5 == 3:
            result[i] = '='
        else:
            result[i] = '-'


for i in range(1, len(result)):
    print(result[i], end='')
print()
