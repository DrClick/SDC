from heapq import heappush, heappop
# ----------
# User Instructions:
#
# Define a function, search() that returns a list
# in the form of [optimal path length, x, y]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
# 0 = Navigable space
# 1 = Occupied space



grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid) - 1, len(grid[0]) - 1]
cost = 1

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']


def search(grid, init, goal, cost):
    # ----------------------------------------
    # insert code here
    # ----------------------------------------

    # track where we have been
    explored = []
    for i in range(len(grid)):
        explored.append([])
        for j in range(len(grid[i])):
            explored[i].append(0)



    # set bounds
    # REMEMBER grid is grid[y,x]
    max_x = len(grid[0]) - 1
    max_y = len(grid) - 1

    g_value_heap = []
    found = init == goal
    heappush(g_value_heap, (0, init))

    # lets go explore
    while not found:
        # check we have not exhausted the search
        if len(g_value_heap) == 0:
            print 'fail'
            print explored
            return 'fail'


        current_cell = heappop(g_value_heap)
        g_value = current_cell[0] + 1
        current_pos = current_cell[1]

        neighbors = [[current_pos[0] + x[0], current_pos[1] + x[1]] for x in delta]
        # look at each neighbor and if a valid neighbor, determine if we have been there and if not
        # add it to the explore heap
        for ii in range(len(neighbors)):
            neighbor = neighbors[ii]
            if neighbor[0] <= max_y and neighbor[0] >= 0 and neighbor[1] <= max_x and neighbor[1] >= 0:

                # see if we are there yet
                if neighbor == goal:
                    found = True
                    print [g_value, neighbor[0], neighbor[1]]
                    return [g_value, neighbor[0], neighbor[1]]

                #otherwise add it to the heap if it has not already been explored and is not a wall
                explored_cell = explored[neighbor[0]][neighbor[1]]
                map_cell = grid[neighbor[0]][neighbor[1]]

                if not explored_cell and map_cell != 1:
                    heappush(g_value_heap, (g_value, neighbor))

                explored[neighbor[0]][neighbor[1]] = True


search(grid, init, goal, cost)