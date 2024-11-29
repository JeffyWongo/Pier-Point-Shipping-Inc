"""
Purpose of class Load:
    1. Run load / unload operation with A*
"""

import queue

# for testing
class Container:
    def __init__(self, name = "UNUSED", weight = 0):
        self.name = name
        self.weight = weight

# cannot do Container == Container right now programatically

class Load:
    # function called by main program
    @staticmethod
    def run(ship_layout, unload_list, load_list):
        for item in load_list:
            item += item + (8,0)

        Load.a_star(ship_layout, unload_list, load_list)

    
    # a star algorithm for moves to do
    @staticmethod
    def a_star(ship_layout, full_unload_list, full_load_list):
        # ASSUMPTION: unload_list and load_list stores a pair (container (name needed) and its location)

        # initialize frontier, explored, and solution
        frontier = queue.PriorityQueue()
        explored = {}
        solution_map = {}
        
        # pair stores (f, g, h, state)
        # f = g (cost) + h (heuristic)
        initial_h = Load.calc_heuristic(ship_layout, full_unload_list, full_load_list)
        frontier.put((initial_h, 0, initial_h, ship_layout.copy(), full_unload_list, full_load_list))

        # loops for each state in queue
        while not frontier.empty():
            _, current_cost, current_h, current_layout, unload_list, load_list = frontier.get()
            hashable_layout = tuple(tuple(row) for row in current_layout)

            # check goal state
            if(Load.check_goal_state(current_layout, unload_list, load_list)):
                return Load.reconstruct_path(solution_map, current_layout)

            # check if state is already explored
            if(explored[hashable_layout]==True):
                continue

            # note that current state is explored (map / dictionary)
            explored[hashable_layout] = True

            # TODO: add all possible moves to the frontier
            # TODO: don't load already explored states into frontier (when frontier implemented)
            # TODO: update load and unload list for each state
            # TODO: keep track of previous states
            top_containers = Load.find_top_empty_containers(current_layout)
            frontier.put()
            
    # find highest empty slot in each column
    @staticmethod
    def find_top_empty_containers(current_layout):
        top_containers = []
        transposed_layout = zip(*current_layout)
        for col, column in enumerate(transposed_layout): # iterate through columns
            for row, item in enumerate(column):
                if(item.name == "UNUSED"):
                    top_containers.append((row, col))
                    break
        return top_containers

    # reconstruct path when solution is found
    @staticmethod
    def reconstruct_path(solution_map, current_layout):
        # TODO: reconstruct solution
        return

    # check if goal state is satisfied
    # TODO: works fine now. but can be simpler after frontier is finished
    @staticmethod
    def check_goal_state(ship_layout, unload_list, load_list):
        return Load.check_unload_goal(ship_layout, unload_list) & Load.check_load_goal(ship_layout, load_list)
    
    # check if containers to unload are off the ship (and buffer)
    @staticmethod
    def check_unload_goal(ship_layout, unload_list):
        ship_containers = [container.name for row in ship_layout for container in row]

        # check if every container in unload_list is in ship_containers
        for container, _ in unload_list:
            if container.name in ship_containers:
                return False

        return True
    
    # check if containers to load are on the ship
    def check_load_goal(ship_layout, load_list):
        # check if every container in load_list is in ship_containers
        for container, location in load_list:
            x, y = location
            if ship_layout[x][y].name != container.name:
                return False

        return True

    # check if goal of loading is done

    # calculate the total heuristic
    @staticmethod
    def calc_heuristic(ship_layout, unload_list, load_list):
        return Load.calc_unload_h(ship_layout, unload_list) + Load.calc_load_h(load_list)


    # part of heuristic for unloading
    @staticmethod
    def calc_unload_h(ship_layout, unload_list):
        sum = 0
        lowest_per_col = {}

        for _, location in unload_list:
            r, c = location
            old_low = 8

            if c not in lowest_per_col:
                lowest_per_col[c] = r
            elif r < lowest_per_col[c]:
                old_low = lowest_per_col[c]
                lowest_per_col[c] = r
            else:
                old_low = lowest_per_col[c]
                sum -= 1

            # Check if there are containers on top (add to h)
            for row in range(r + 1, 8):  # Iterate above the current position
                if ship_layout[row][c].name != "NAN" and row < old_low:  # Check if empty
                    sum += 1
                else:
                    break
            # distance to (9,1)
            sum += Load.load_unload_heuristic(r, c)
        return sum


    # heuristic for an individual container to unload
    @staticmethod
    def load_unload_heuristic(x: int, y: int):
        return abs(8 - x) + y


    # part of heuristic for loading
    @staticmethod
    def calc_load_h(load_list):
        sum = 0
        for _, location, current_location in load_list:
            # distance to (9,1)
            r, c = location
            x, y = current_location
            # sum += Load.load_unload_heuristic(r, c)
            sum += abs(r-x) + abs(c-y)
        return sum





# testing
# Load.run(ship.Ship)
# print(ship.Ship.vector[8][12])

# container = Container("A", 120)
# print(container.name)
# print(container.weight)


# Testing
unload_container = Container("A", 120)
load_container = Container("B", 200)
load_container2 = Container("F", 300)

# 8 x 12
layout = [[Container() for i in range(0,12)] for j in range(0,8)]
layout[0][0] = Container("A", 120)
layout[1][0] = Container("C", 400)
layout[2][0] = Container("D", 500)

# Test case for running:
# Load.run(layout, [(unload_container, (1, 3))], [(load_container, (1, 4))])

# Test case for heuristic: (may still be glitchy with multiple containers in the same column)
# h = Load.calc_heuristic(layout, [(unload_container, (0, 0))], [(load_container, (0, 1))])
# print(h)
# h = Load.calc_heuristic(layout, [(Container("A", 120), (2,0)), (Container("C", 400), (0,0))], [])
# print(h)

# Test case for checking goal state:
# # loading:
# result = Load.check_goal_state(layout, [], [(Container("A", 120), (0,0)), (Container("C", 400), (1,0))])
# print(result)
# # unloading:
# result = Load.check_goal_state(layout, [(Container("C", 400), (1,0))], [])
# print(result)

# Test case for finding top empty containers for each column:
layout2 = [[Container() for i in range(0,12)] for j in range(0,8)]
layout2[0][0] = load_container
layout2[0][1] = load_container
# layout2[0][2] = load_container
# layout2[0][3] = load_container
# layout2[0][4] = load_container
# layout2[1][0] = load_container
# layout2[1][1] = load_container
# layout2[2][0] = load_container
output = Load.find_top_empty_containers(layout2)
for item in output:
    cords = "(" + str(item[0]) + ", " + str(item[1]) + ")"
    print(cords)
