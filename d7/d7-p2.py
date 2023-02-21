with open("./input.txt", "r") as f:
    lines = f.readlines()

# parsing the input
terminal_lines = []
for line in lines:
    if line[0] == '$':
        terminal_lines.append(('command', line.replace('\n', '').split()))
    else:
        terminal_lines.append(('content', line.replace('\n', '').split())) 

# utility classes for the filesystem
class Dir:
    def __init__(self, name, parent_dir):
        self.name = name
        self.size = 0
        self.content = []
        self.parent_dir = parent_dir

    def cd_in(self, dir_name):
        for item in self.content:
            if item.name == dir_name and isinstance(item, Dir):
                return item

    def cd_out(self):
        return self.parent_dir

    def add_file(self, name, size):
        self.content.append(File(name, size))
    
    def add_subdir(self, name):
        self.content.append(Dir(name, self))
    

class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size


class FileSystem:
    def __init__(self):
        self.root = Dir("/", None)

    def calculate_file_storage(self):
        
        def sum_total_file_size(dir):
            total_file_size = 0
            for item in dir.content:
                # print(item.name)
                total_file_size += item.size
            dir.size = total_file_size

        def post_order_traverse(dir):
            for item in dir.content:
                if isinstance(item, Dir):
                    post_order_traverse(item)
                    sum_total_file_size(item)
                    # print(item.name, item.size)

        post_order_traverse(self.root)
        sum_total_file_size(self.root)


fs = FileSystem()
current_dir = None
for i in range(len(terminal_lines)):
    line = terminal_lines[i]
    if line[0] == 'command':
        cm = line[1]
        if cm[1] == 'cd':
            if cm[2] == '/':
                current_dir = fs.root
            elif cm[2] == '..':
                current_dir = current_dir.cd_out()
            else:
                current_dir = current_dir.cd_in(cm[2])
        elif cm[1] == 'ls':
            continue
    else:
        item = line[1]
        if item[0] == 'dir':
            current_dir.add_subdir(item[1])
        else:
            current_dir.add_file(item[1], int(item[0]))

fs.calculate_file_storage()

total_storage = 70_000_000
space_left = total_storage - fs.root.size

update_size = 30_000_000
space_needed = update_size - space_left

def find_dir_with_at_least(dir, at_least_size):
    dir_list = []
    for item in dir.content:
        if isinstance(item, Dir):
            if item.size >= at_least_size:
                dir_list.append(item)
            dir_list += find_dir_with_at_least(item, at_least_size)
    return dir_list

dir_list = find_dir_with_at_least(fs.root, space_needed)
if fs.root.size >= space_needed:
    dir_list.append(fs.root)

smallest_dir_size = total_storage
for dir in dir_list:
    if dir.size < smallest_dir_size:
        smallest_dir_size = dir.size

print(smallest_dir_size)