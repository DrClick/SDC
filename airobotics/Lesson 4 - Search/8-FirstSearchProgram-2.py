# ----------
# User Instructions:
#
# Define a function, search() that returns a list
# in the form of [optimal path length, row, col]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

delta_name = ['^', '<', 'v', '>']

def search(grid,init,goal,cost, verbose=False):
    # ----------------------------------------
    # insert code here
    # ----------------------------------------

    open = []
    explored = {}

    y_bounds = (0, len(grid) - 1)
    x_bounds = (0, len(grid[0]) - 1)

    path = None
    g_value = 0

    open.append((g_value, init[0], init[1]))
    explored['{}-{}'.format(init[0], init[1])] = True

    while len(open):
        path = open.pop()
        if verbose:
            print path

        #incrament g-value
        g_value = path[0] + cost

        # check to see if at goal
        if path[1] == goal[0] and path[2] == goal[1]:
            if verbose:
                print 'SUCCESS'

            return list(path)

        neighbors = [(g_value, path[1] - x[0], path[2] - x[1]) for x in delta]

        # filter valid neighbors that are on the grid and not
        # explored and navigable
        valid_neighbors = [(g, y, x) for (g, y, x) in neighbors
                           if y_bounds[0] <= y <= y_bounds[1] and
                           x_bounds[0] <= x <= x_bounds[1] and
                           not '{}-{}'.format(y, x) in explored and
                           grid[y][x] == 0]

        # mark valid neighbors as explored
        for neighbor in valid_neighbors:
            g, y, x = neighbor
            explored['{}-{}'.format(y, x)] = True

        # add valid neighbors to open
        open.extend(valid_neighbors)

        #sort in reverse order so the smallest G-value can be popped off
        open = sorted(open, reverse=True)

        if verbose:
            print 'OPEN LIST -------------'
            print open
            print '-----------------------'

    # if we reached here, the goal was not found
    if verbose:
        print('FAILED')

    return 'fail'


print search(grid, init, goal, cost, verbose=True)