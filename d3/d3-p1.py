with open("input.txt", "r") as f:
    lines = f.readlines()

rucksacks = []
for line in lines:
    all_items_in_rucksack = line[:-1]
    compartment_size = int(len(all_items_in_rucksack)/2)
    rucksacks.append([all_items_in_rucksack[0:compartment_size], all_items_in_rucksack[compartment_size:]])

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
for [c1, c2] in rucksacks:
    c_size = len(c1)
    c2_sorted = sorted(c2)
    for i in range(c_size):
        if letter_binnary_search(c1[i], c2_sorted, c_size-1):
            common_item = c1[i]
    if common_item.isupper():
        priority = ord(common_item) - ord('A') + 27
    else: 
        priority = ord(common_item) - ord('a') + 1
    total_priority += priority

print(total_priority)            
    
