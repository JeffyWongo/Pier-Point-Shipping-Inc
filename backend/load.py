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
        # TODO: how we getting containers (or location) to unload and locations to load to
        Load.a_star(ship_layout, unload_list, load_list)

    
    # a star algorithm for moves to do
    @staticmethod
    def a_star(ship_layout, unload_list, load_list):
        # ASSUMPTION: unload_list and load_list stores a pair (container (name needed) and its location)

        # initialize frontier, explored, and solution
        frontier = queue.PriorityQueue()
        explored = dict() # TODO: getting dictionary key value pair working (ship_layout, True)
        solution = queue.Queue() # TODO: keep track of previous states using tree?
        
        # TODO: have total cost (for priority), keep cost and heuristic separate
        frontier.put((0, Load.calc_heuristic(ship_layout, unload_list, load_list), ship_layout.copy()))

        # loops for each state in queue
        while not frontier.empty():
            current = frontier.get()

            current_layout = current[2]

            # TODO: check goal state
            if(Load.check_goal_state(ship_layout, unload_list, load_list)):
                break

            # note that current state is explored (map / dictionary)
            explored[current_layout] = True

            # TODO: add all possible moves to the frontier
            frontier.put(current.first, Load.calc_heuristic(ship_layout, unload_list, load_list), [])

    # check if goal state is satisfied
    @staticmethod
    def check_goal_state(ship_layout, unload_list, load_list):
        return Load.check_unload_goal(ship_layout, unload_list) & Load.check_load_goal(ship_layout, load_list)
    
    # check if containers to unload are off the ship (and buffer)
    @staticmethod
    def check_unload_goal(ship_layout, unload_list):
        return True
    
    # check if containers to load are on the ship
    def check_load_goal(ship_layout, load_list):
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
        for location in unload_list:
            # Dummy variable (0,0) right now until i know how this is being represented
            # TODO: check if container is off
            # function param: (x, y)
            sum += Load.load_unload_heuristic(0, 0) # TODO: add number of containers on top
        return sum


    # heuristic for an individual container to unload
    @staticmethod
    def load_unload_heuristic(x: int, y: int):
        return abs(7 - x) + (y)


    # part of heuristic for loading
    @staticmethod
    def calc_load_h(load_list):
        sum = 0
        for location in load_list:
            # Dummy variable (0,0) right now until i know how this is being represented
            # function param: (x, y)
            sum += Load.load_unload_heuristic(0, 0)
        return sum





# testing
# Load.run(ship.Ship)
# print(ship.Ship.vector[8][12])

container = Container("A", 12)
print(container.name)
print(container.weight)


# Testing
unload_container = Container("A", 120)
load_container = Container("B", 200)

# 8 x 12
layout = [[Container() for i in range(0,12)] for j in range(0,8)]
layout[1][3] = Container("A", 120)

Load.run(layout, [(unload_container, (1, 3))], [(load_container, (1, 4))])