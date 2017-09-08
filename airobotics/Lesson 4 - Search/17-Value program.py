# ----------
# User Instructions:
#
# Create a function compute_value which returns
# a grid of values. The value of a cell is the minimum
# number of moves required to get from the cell to the goal.
#
# If a cell is a wall or it is impossible to reach the goal from a cell,
# assign that cell a value of 99.
# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0]]

goal = [len(grid) - 1, len(grid[0]) - 1]
cost = 1  # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go rightundefined

delta_name = ['^', '<', 'v', '>']


def explore(nodes, current_value, grid, value, cost):
    # get the neighbors of this cell
    neighbors = []
    grid_height = len(grid)
    grid_width = len(grid[0])

    # find all valid neighbors
    for node in nodes:
        neighbors.extend([(node[0] + x[0], node[1] + x[1]) for x in delta])

    valid_neighbors = set([x for x in neighbors if
                        0 <= x[0] < grid_height and
                        0 <= x[1] < grid_width and
                        grid[x[0]][x[1]] == 0 and
                        value[x[0]][x[1]] == 99
                       ])

    # set the value for all valid neighbors
    new_value = current_value + cost
    for neighbor in valid_neighbors:
        x, y = neighbor
        if value[x][y] > new_value:
            value[x][y] = new_value

    # recursively explore this set of neighbors
    if valid_neighbors:
        explore(valid_neighbors, new_value, grid, value, cost)
    else:
        return


def compute_value(grid, goal, cost):
    # ----------------------------------------
    # insert code below
    # ----------------------------------------

    # make sure your function returns a grid of values as
    # demonstrated in the previous video.

    # set up the value grid
    value = [[99 for _ in row] for row in grid]
    value[goal[0]][goal[1]] = 0

    # recursively explore the grid
    explore([goal], 0, grid, value, cost)

    return value


result = compute_value(grid, goal, cost)
for r in result:
    print [str(x).rjust(2) for x in r]

print result


