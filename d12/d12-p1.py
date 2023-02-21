with open("./input.txt", "r") as f:
    N = len(f.readline().replace('\n', ''))
with open("./input.txt", "r") as f: 
    M = len(f.readlines())
  
grid = [ [None for _ in range(N)] for _ in range(M)]
size = (M, N)
(Si, Sj) = (None, None)
(Ei, Ej) = (None, None)

with open("./input.txt", "r") as f:
    for i in range(M):
        line = f.readline().replace('\n', '')
        for j in range(N):
            if line[j] == 'S':
                grid[i][j] = 'a'
                (Si, Sj) = (i, j)
            elif line[j] == 'E':
                grid[i][j] = 'z'
                (Ei, Ej) = (i, j)
            else:
                grid[i][j] = line[j]

def is_inside(pos, grid_size):
    if 0 <= pos[0] and pos[0] < grid_size[0]:
        if 0 <= pos[1] and pos[1] < grid_size[1]:
            return True
    return False 

def BFS(grid, grid_size, start, end):
    queue = []
    queue.append(start)
    directions = [(+1, 0), (-1, 0), (0, +1), (0, -1)]
    visited = [ [False for _ in range(grid_size[1])] for _ in range(grid_size[0])]
    costs = [ [0 for _ in range(grid_size[1])] for _ in range(grid_size[0])]
    costs[start[0]][start[1]] = 1

    while queue:
        pos = queue.pop(0)
        (i, j) = pos
        if visited[i][j]:
            continue
        visited[i][j] = True
        if pos == end:
            break

        for (di, dj) in directions:
            next = (i + di, j + dj)
            if is_inside(next, grid_size):
                (ni, nj) = next
                if ord(grid[ni][nj]) <= ord(grid[i][j]) + 1:
                    if not visited[ni][nj]:
                        queue.append(next)
                        costs[ni][nj] = costs[i][j] + 1
    
    return costs[end[0]][end[1]] - 1

print(BFS(grid, size, (Si, Sj), (Ei, Ej)))