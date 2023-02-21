with open("input.txt", "r") as f:
    lines = f.readlines()

rucksacks = []
for line in lines:
    rucksacks.append(line[:-1])

def letter_binnary_search(char, sorted_list, end, start=0):
    if start > end:
        return False
    else:
        middle = (end + start) // 2
        if char == sorted_list[middle]:
            return True
        elif ord(char) > ord(sorted_list[middle]):
            return letter_binnary_search(char, sorted_list, end, middle+1)
        else:
            return letter_binnary_search(char, sorted_list, middle-1, start)

total_priority = 0
for i in range(len(rucksacks)//3):
    sack_1 = rucksacks[3*i]
    sack_2 = rucksacks[3*i+1]
    sack_3 = rucksacks[3*i+2]
    
    sack_2_sorted = sorted(sack_2)
    sack_3_sorted = sorted(sack_3)
    for i in range(len(sack_1)):
        item_1 = sack_1[i]
        if letter_binnary_search(item_1, sack_2_sorted, len(sack_2_sorted)-1):
            if letter_binnary_search(item_1, sack_3_sorted, len(sack_3_sorted)-1):
                common_item = item_1
                break
        
    if common_item.isupper():
        priority = ord(common_item) - ord('A') + 27
    else: 
        priority = ord(common_item) - ord('a') + 1
    total_priority += priority

print(total_priority)            
    
