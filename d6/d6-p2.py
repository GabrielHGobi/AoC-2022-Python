with open("input.txt", "r") as f: 
    message = f.readline()

start_of_message = None
i = 0
while i + 3 < len(message):
    marker = message[i:i+14]

    next = None
    for j in range(13):
        for k in range(j+1, 14):
            if marker[j] == marker[k]:
                next = j
        
    if next is None:
        start_of_message = i
        break

    i += 1 + next 

print(f'{start_of_message+14}, {message[start_of_message:start_of_message+14]}')
