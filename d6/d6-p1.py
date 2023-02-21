with open("input.txt", "r") as f: 
    message = f.readline()

start_of_packet = None
i = 0
while i + 3 < len(message):
    marker = message[i:i+4]

    next = None
    for j in range(3):
        for k in range(j+1, 4):
            if marker[j] == marker[k]:
                next = j
        
    if next is None:
        start_of_packet = i
        break

    i += 1 + next 

print(f'{start_of_packet+4}, {message[start_of_packet:start_of_packet+4]}')
