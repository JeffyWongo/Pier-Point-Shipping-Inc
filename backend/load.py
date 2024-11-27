"""
Purpose of class Load:
    1. Run load / unload operation with A*
"""

import queue

# for testing
class Container:
    def __init__(self, name = "NaN", weight = 0):
        self.name = name
        self.weight = weight


class Load:
    # function called by main program
    @staticmethod
    def run(ship_layout, unload_list, load_list):
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
        frontier.put((initial_h, 0, initial_h, ship_layout.copy(), full_unload_list, full_load_list)) # TODO: need to update unload and load list as we go (put in the tuple)

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
            # TODO: don't load these states into frontier (when frontier implemented)
            # TODO: update load and unload list for each state
            # TODO: keep track of previous states
            frontier.put()


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
        ship_containers = [container for row in ship_layout for container in row]

        # check if every container in unload_list is in ship_containers
        for container in unload_list:
            if container in ship_containers:
                # TODO: paranoia about equals function (pass by ref?)
                return False

        return True
    
    # check if containers to load are on the ship
    def check_load_goal(ship_layout, load_list):
        ship_containers = [container for row in ship_layout for container in row]

        # check if every container in load_list is in ship_containers
        for container in load_list:
            if container not in ship_containers:
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
        for _, location in unload_list:
            r, c = location
            # TODO: for each column, check what lowest container is (currenly, if 2 containers same col, we overcount)
            # Check if there are containers on top (add to h)
            for row in range(r + 1, 8):  # Iterate above the current position
                if ship_layout[row][c].name != "NaN":  # Check if empty
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
        for _, location in load_list:
            # distance to (9,1)
            r, c = location
            sum += Load.load_unload_heuristic(r, c)
        return sum





# testing
# Load.run(ship.Ship)
# print(ship.Ship.vector[8][12])

container = Container("A", 120)
print(container.name)
print(container.weight)


# Testing
unload_container = Container("A", 120)
load_container = Container("B", 200)

# 8 x 12
layout = [[Container() for i in range(0,12)] for j in range(0,8)]
layout[0][0] = Container("A", 120)
layout[1][0] = Container("C", 400)

# Load.run(layout, [(unload_container, (1, 3))], [(load_container, (1, 4))])
h = Load.calc_heuristic(layout, [(unload_container, (0, 0))], [(load_container, (0, 1))])
print(h)