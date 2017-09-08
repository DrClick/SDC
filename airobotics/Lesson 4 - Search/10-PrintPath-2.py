# -----------
# User Instructions:
#
# Modify the the search function so that it returns
# a shortest path as follows:
#
# [['>', 'v', ' ', ' ', ' ', ' '],
#  [' ', '>', '>', '>', '>', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', '*']]
#
# Where '>', '<', '^', and 'v' refer to right, left,
# up, and down motions. Note that the 'v' should be
# lowercase. '*' should mark the goal cell.
#
# You may assume that all test cases for this function
# will have a path from init to goal.
# ----------

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0]]
init = [0, 0]
goal = [len(grid) - 1, len(grid[0]) - 1]
cost = 1

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>', '']


def search(grid, init, goal, cost):
    # ----------------------------------------
    # modify code below
    # ----------------------------------------
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[init[0]][init[1]] = 1

    x = init[0]
    y = init[1]
    g = 0

    open = [[g, x, y, []]]

    found = False  # flag that is set when search is complete
    resign = False  # flag set if we can't find expand

    shortest_path = None

    while not found and not resign:
        if len(open) == 0:
            resign = True
            return 'fail'
        else:

            # take the smallest g value cell to explore
            open.sort(reverse=True)
            next = open.pop()

            g, x, y, path = next



            if x == goal[0] and y == goal[1]:
                found = True
                shortest_path = next
            else:
                for delta_index in range(len(delta)):

                    # look at each new
                    #  position using the moves in delta
                    x2 = x + delta[delta_index][0]
                    y2 = y + delta[delta_index][1]

                    # determine if the new position is legally on the board
                    if 0 <= x2 < len(grid) and 0 <= y2 < len(grid[0]):

                        # determine if the position has not been explored already
                        # and that its not wall
                        if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                            # incrament the step
                            g2 = g + cost

                            # add it to the open cells to explore
                            new_path = path + [(x, y, delta_name[delta_index])]
                            open.append([g2, x2, y2, new_path])

                            closed[x2][y2] = 1


    # format the shortest_path
    expand = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    for entry in shortest_path[3]:
        x, y, d = entry
        expand[x][y] = d

    expand[goal[0]][goal[1]] = '*'
    return expand  # make sure you return the shortest path


result = search(grid, init, goal, cost)

for row in result:
    print row
