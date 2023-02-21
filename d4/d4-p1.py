with open("./input.txt", "r") as f:
    lines = f.readlines()

counter = 0
for line in lines:
    # Getting the pairs
    p1_str, p2_str = line[:-1].split(",")
    p1 = [int(i) for i in p1_str.split("-")]
    p2 = [int(i) for i in p2_str.split("-")]
    
    if p1[0] < p2[0]: # p1 starts firts
        if p1[1] >= p2[1]: # p1 finishes after or together with p2
            counter += 1
    elif p2[0] < p1[0]: # p2 starts firts
        if p2[1] >= p1[1]: # p2 finishes after or together with p1
            counter += 1
    else: # p1 and p2 starts together
        counter +=1

print(counter)

    


