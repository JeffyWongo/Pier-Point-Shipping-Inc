"""
Purpose of class Load:
    1. Run load / unload operation with A*
"""

import ship
import queue

class Load:
    # function called by main program
    @staticmethod
    def run(ship_layout: ship):
        # TODO: how we getting containers to unload and load
        Load.a_star(ship, [], [])

    
    # a star algorithm for moves to do
    @staticmethod
    def a_star(ship_layout:ship, unload_list, load_list):
        # initialize frontier, explored, and solution
        frontier = queue.PriorityQueue()
        explored = dict(ship_layout, True)
        solution = queue.Queue() # not sure
        
        frontier.put((0, ship_layout.copy()))

        while not frontier.empty():
            current = frontier.get()
            print("placeholder")

    # part of heuristic for unloading
    @staticmethod
    def calc_unload_h(containers):
        sum = 0

        for container in containers:
            # Dummy variable (0,0) right now until i know how this is being represented
            # function param: (x, y)
            sum += Load.load_unload_heuristic(0, 0)

        return sum

    # heuristic for an individual container to unload
    @staticmethod
    def load_unload_heuristic(x: int, y: int):
        return abs(7 - x) + (y)

    # part of heuristic for loading
    @staticmethod
    def calc_load_h(locations):
        sum = 0

        for location in locations:
            # Dummy variable (0,0) right now until i know how this is being represented
            # function param: (x, y)
            sum += Load.load_unload_heuristic(0, 0)


# testing
Load.run(ship.Ship)