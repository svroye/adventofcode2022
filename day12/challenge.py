'''
--- Day 12: Hill Climbing Algorithm ---
You try contacting the Elves using your handheld device, but the river you're following must be too low to get a
decent signal.

You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area from
above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where a is
the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

Also included on the heightmap are marks for your current position (S) and the location that should get the best signal
(E). Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.

You'd like to reach E, but to save energy, you should do it in as few steps as possible. During each step, you can move
exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of the
destination square can be at most one higher than the elevation of your current square; that is, if your current
elevation is m, you could step to elevation n, but not to elevation o. (This also means that the elevation of the
destination square can be much lower than the elevation of your current square.)

For example:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi

Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right, but
eventually you'll need to head toward the e at the bottom. From there, you can spiral around to the goal:

v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^

In the above diagram, the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or
right (>). The location that should get the best signal is still E, and . marks unvisited squares.

This path reaches the goal in 31 steps, the fewest possible.

What is the fewest steps required to move from your current position to the location that should get the best signal?

'''
from collections import deque


def create_grid(file_name):
    with open(file_name, 'r') as f:
        data = [[ord(j) for j in i.strip()] for i in f.readlines()]
    rows = len(data)
    columns = len(data[0]) if rows > 0 else 0

    start = None
    end = None
    for i in range(rows):
        for j in range(columns):
            if data[i][j] == ord("S"):
                start = (i, j)
            elif data[i][j] == ord("E"):
                end = (i, j)

    data[start[0]][start[1]] = ord('a')
    data[end[0]][end[1]] = ord('z')
    return data, rows, columns, start, end


def bfs(data, rows, columns, start, end):
    children_map = create_children_map(data, rows, columns)
    queue = deque()
    visited = set()
    queue.append((start, []))

    while queue:
        node, path = queue.popleft()
        visited.add(node)
        if node == end:
            return path + [node]

        for child in children_map[node]:
            if child in visited:
                continue
            queue.append((child, path + [node]))
            visited.add(child)

    return None


def create_children_map(data, rows, columns):
    children = {}
    for i in range(rows):
        for j in range(columns):
            children[(i, j)] = [c for c in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
                                if (0 <= c[0] <= rows - 1) and (0 <= c[1] <= columns - 1)
                                and data[c[0]][c[1]] - data[i][j] <= 1]
    return children


data, rows, columns, start, end = create_grid('input.txt')
print(len(bfs(data, rows, columns, start, end)))

'''
--- Part Two ---
As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail. The beginning isn't 
very scenic, though; perhaps you can find a better starting point.

To maximize exercise while hiking, the trail should start as low as possible: elevation a. The goal is still the square 
marked E. However, the trail should still be direct, taking the fewest steps to reach its goal. So, you'll need to 
find the shortest path from any square at elevation a to the square marked E.

Again consider the example from above:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi

Now, there are six choices for starting position (five marked a, plus the square marked S that counts as being at 
elevation a). If you start at the bottom-left square, you can reach the goal most quickly:

...v<<<<
...vv<<^
...v>E^^
.>v>>>^^
>^>>>>>^

This path reaches the goal in only 29 steps, the fewest possible.

What is the fewest steps required to move starting from any square with elevation a to the location that should get the 
best signal?
'''

data, rows, columns, _, end = create_grid('input.txt')

start_positions = []
for i in range(rows):
    for j in range(columns):
        if data[i][j] == ord("a"):
            start_positions.append((i, j))

steps = []
for position in start_positions:
    result = bfs(data, rows, columns, position, end)
    if result:
        steps.append(len(result))

print(min(steps))