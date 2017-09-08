# ----------
# User Instructions:
#
# Write a function optimum_policy that returns
# a grid which shows the optimum policy for robot
# motion. This means there should be an optimum
# direction associated with each navigable cell from
# which the goal can be reached.
#
# Unnavigable cells as well as cells from which
# the goal cannot be reached should have a string
# containing a single space (' '), as shown in the
# previous video. The goal cell should have '*'.
# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 1, 0, 1, 1, 0]]

init = [0, 0]
goal = [len(grid) - 1, len(grid[0]) - 1]
cost = 1  # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']


def explore(nodes, current_value, grid, value, cost, policy):
    # get the neighbors of this cell
    neighbors = []
    grid_height = len(grid)
    grid_width = len(grid[0])

    # find all valid neighbors
    for node in nodes:
        neighbors.extend([(node[0] + x[0], node[1] + x[1], delta_index) for
                          delta_index, x in enumerate(delta)])

    valid_neighbors = set([x for x in neighbors if
                           0 <= x[0] < grid_height and
                           0 <= x[1] < grid_width and
                           grid[x[0]][x[1]] == 0 and
                           value[x[0]][x[1]] == 99
                           ])

    # set the value for all valid neighbors
    new_value = current_value + cost
    for neighbor in valid_neighbors:
        x, y, di = neighbor
        value[x][y] = new_value
        policy[x][y] = delta_name[di -2]

    # recursively explore this set of neighbors
    if valid_neighbors:
        explore(valid_neighbors, new_value, grid, value, cost, policy)
    else:
        return


def optimum_policy(grid, goal, cost):
    # ----------------------------------------
    # insert code below
    # ----------------------------------------

    # make sure your function returns a grid of values as
    # demonstrated in the previous video.

    # set up the value grid
    value = [[99 for _ in row] for row in grid]
    policy = [[' ' for _ in row] for row in grid]
    value[goal[0]][goal[1]] = 0
    policy[goal[0]][goal[1]] = '*'

    # recursively explore the grid
    explore([goal], 0, grid, value, cost, policy)

    return policy


result = optimum_policy(grid, goal, cost)
for r in result:
    print r

