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
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
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
            explored[i].append(-1)



    # set bounds
    # REMEMBER grid is grid[y,x]
    max_x = len(grid[0]) - 1
    max_y = len(grid) - 1

    g_value_heap = []
    found = init == goal
    heappush(g_value_heap, (0, init))
    explored[0][0] = 0
    current_expansion_step = 1

    # lets go explore
    while not found:
        # check we have not exhausted the search
        if len(g_value_heap) == 0:
            print 'fail'
            print explored
            return explored

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
                    explored[neighbor[0]][neighbor[1]] = current_expansion_step

                    # walk back the shortest path
                    return shortestPath(explored, goal, init)

                # otherwise add it to the heap if it has not already been explored and is not a wall
                explored_cell = explored[neighbor[0]][neighbor[1]]
                map_cell = grid[neighbor[0]][neighbor[1]]

                if explored_cell < 0 and map_cell != 1:
                    heappush(g_value_heap, (g_value, neighbor))
                    explored[neighbor[0]][neighbor[1]] = current_expansion_step
                    current_expansion_step += 1


def shortestPath(grid, goal, init):
    # track where we have been
    path = []
    for i in range(len(grid)):
        path.append([])
        for j in range(len(grid[i])):
            path[i].append(' ')

    delta = [[-1, 0],  # go up
             [0, -1],  # go left
             [1, 0],  # go down
             [0, 1]]  # go right
    # REMEMBER grid is grid[y,x]
    max_x = len(grid[0]) - 1
    max_y = len(grid) - 1

    delta_name = ['^', '<', 'v', '>']
    current_pos = goal
    path[goal[0]][goal[1]] = '*'


    complete = False

    while not complete:

        # look at each neighbor and if a valid neighbor, determine if its the smallest neighbor
        # and record its value
        lowest_neighbor_value = grid[goal[0]][goal[1]]
        lowest_neighbor = goal
        lowest_neighbor_delta = 0
        neighbors = [[current_pos[0] + x[0], current_pos[1] + x[1]] for x in delta]

        for ii in range(len(neighbors)):
            neighbor = neighbors[ii]
            if neighbor[0] <= max_y and neighbor[0] >= 0 and neighbor[1] <= max_x and neighbor[1] >= 0 and grid[neighbor[0]][neighbor[1]] != -1:

                # see if we are there yet
                if neighbor == init:
                    complete = True
                    path[neighbor[0]][neighbor[1]] = delta_name[ii + 2]
                    return path

                # otherwise add it to the heap if it has not already been explored and is not a wall
                grid_cell = grid[neighbor[0]][neighbor[1]]

                if grid_cell < lowest_neighbor_value:
                    lowest_neighbor_value = grid_cell
                    lowest_neighbor = neighbor
                    lowest_neighbor_delta = ii

        # mark the direction
        path[lowest_neighbor[0]][lowest_neighbor[1]] = delta_name[(lowest_neighbor_delta + 2) % 4]
        current_pos = lowest_neighbor

print search(grid, init, goal, cost)