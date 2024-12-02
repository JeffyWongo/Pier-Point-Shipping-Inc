"""
Purpose of class Load:
    1. Run load / unload operation with A*
"""

import queue
import copy

# for testing
class Container:
    def __init__(self, name = "UNUSED", weight = 0):
        self.name = name
        self.weight = weight
    
    def __lt__(self, other):
        if isinstance(other, Container):
            return self.name < other.name
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Container):
            return self.name == other.name
        return NotImplemented

    def __hash__(self):
        return hash((self.name, self.weight))



class Load:
    # function called by main program
    @staticmethod
    def run(ship_layout, unload_list, load_list):
        for i in range(len(unload_list)):
            unload_list[i] = unload_list[i] + (unload_list[i][1],)
    
        for i in range(len(load_list)):
            load_list[i] = load_list[i] + ((8, 0),)

        return Load.a_star(ship_layout, unload_list, load_list)

    
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
        frontier.put((initial_h, 0, initial_h, copy.deepcopy(ship_layout), full_unload_list, full_load_list))

        # loops for each state in queue
        while not frontier.empty():
            _, current_cost, current_h, current_layout, unload_list, load_list = frontier.get()
            hashable_layout = tuple(tuple(row) for row in current_layout)

            # print(f"{current_cost}, {current_h}")
            # Load.print_layout(current_layout)

            # check goal state
            if(Load.check_goal_state(current_layout, unload_list, load_list)):
                print(f"GOAL: {current_cost}, {current_h}")
                return Load.reconstruct_path(solution_map, current_layout)

            # check if state is already explored
            if explored.get(hashable_layout, False):
                continue
            else:
                explored[hashable_layout] = True

            # finds all empty spots in each column. 3rd line filters
            # find all topmost containers in each column
            empty_spots = Load.find_top_empty_containers(current_layout)
            empty_spots = [cord for cord in empty_spots if cord[0] != 8]
            top_containers = [(x - 1, y) for x, y in empty_spots if x > 0]

            # TODO: add all possible moves to the frontier
            # don't load already explored states into frontier (when frontier implemented)
            # update load and unload list for each state
            # TODO: keep track of previous states
            # Moves:
            # 1. Every container to load to empty_spots
            # 2. Every container in top_containers to empty_spots
            # 3. Every container in top_containers to unloaded

            # every load_list containers to empty_spots
            # TODO: load containers onboard to other possible empty spots
            for load_index, info in enumerate(load_list):
                container, desired_cords, current_cords = info
                if(current_cords == desired_cords):
                    print(f"{load_index} is onboard")
                    continue
                else:
                    print(f"{load_index} is not onboard")
                
                # move directly to desired_cords
                # check if empty
                r, c = desired_cords
                print(empty_spots)
                print(c)
                print(empty_spots[c])
                print(desired_cords)
                if(empty_spots[c]==desired_cords):
                    layout = copy.deepcopy(current_layout)
                    # print(f"h: {current_h}")
                    Load.print_layout(layout)
                    layout[r][c] = container

                    new_load_list = copy.deepcopy(load_list)
                    new_load_list[load_index] = (container, desired_cords, desired_cords)

                    cost = abs(8 - r) + c
                    h = Load.calc_heuristic(layout, unload_list, new_load_list)

                    print(desired_cords)
                    print(f"{current_cost + cost}, {h}")
                    Load.print_layout(layout)
                    
                    stuff = (current_cost + cost + h, current_cost + cost, h, layout, unload_list, new_load_list)
                    frontier.put(stuff)

                # for empty_spot in empty_spots:
                #     layout = copy.deepcopy(current_layout)
                #     if(current_cords!=(8,0)):
                #         layout[current_cords[0]][current_cords[1]] = Container()
                    
                #     layout[empty_spot[0]][empty_spot[1]] = container.copy()
                    
                #     info = list(info)
                #     info[2] = empty_spot
                #     info = tuple(info)


                #     cost = abs(empty_spot[0] - current_cords[0]) + abs(empty_spot[1] - current_cords[1])
                #     h = Load.calc_heuristic(layout, unload_list, load_list)

                #     current_cords = empty_spot

                #     stuff = (current_cost + cost + h, current_cost + cost, h, copy.deepcopy(layout), unload_list, load_list)
                    
                #     frontier.put(stuff)

            # every top_container containers to empty_spots or unload
            for container_cord in top_containers:
                r, c = container_cord

                #TODO: what if move the loaded container around
                is_on_load_list = False
                for load_index, load_container in enumerate(load_list): # TODO: doesn't deal with duplicates
                    if(load_container[0].name == current_layout[r][c].name):
                        is_on_load_list = True
                        break
                if(is_on_load_list):
                    continue

                is_on_unload_list = False
                unload_index = -1
                for idx, unload_container in enumerate(unload_list): # TODO: doesn't deal with duplicates
                    if(unload_container[0].name == current_layout[r][c].name):
                        is_on_unload_list = True
                        unload_index = idx
                        break

                # move to every possible empty spot
                for empty_cord in empty_spots:
                    # if top_container and empty_spot are same col. will lead to floating container
                    if(empty_cord[1]==c):
                        continue

                    highest_empty_r = r
                    for col_index in range(min(c, empty_cord[1]), max(c, empty_cord[1]) + 1):
                        if(col_index==c):
                            continue
                        # if(c==0 and (empty_cord[1]>=1 and empty_cord[1]<=3)):
                        #     print(f"{col_index}, {empty_spots[col_index][0]}, {highest_empty_r}")
                        highest_empty_r = max(empty_spots[col_index][0], highest_empty_r)
                    
                    # if(c==0 and (empty_cord[1]>=1 and empty_cord[1]<=3)):
                    #     print(f"{c} to {empty_cord[1]}: {r} and {empty_cord[0]}, {highest_empty_r}")

                    layout = copy.deepcopy(current_layout)

                    # assumes heuristic functions will take care of everything
                    if is_on_unload_list:
                        unload_item = list(unload_list[unload_index])
                        unload_item[2] = empty_cord
                        unload_list[unload_index] = tuple(unload_item)

                    # swap
                    layout[empty_cord[0]][empty_cord[1]], layout[r][c] = (
                        layout[r][c], 
                        layout[empty_cord[0]][empty_cord[1]]
                    )


                    cost = abs(empty_cord[0] - highest_empty_r) + abs(empty_cord[1] - c) + abs(r - highest_empty_r)
                    h = Load.calc_heuristic(layout, unload_list, load_list)
                    stuff = (current_cost + cost + h, current_cost + cost, h, layout, unload_list, load_list)
                    
                    frontier.put(stuff)

                if is_on_unload_list:
                    layout = copy.deepcopy(current_layout)
                    layout[r][c] = Container()

                    cost = abs(8 - r) + c
                    unload_item = list(unload_list[unload_index])
                    unload_item[2] = (8,0)
                    unload_list[unload_index] = tuple(unload_item)
                    h = Load.calc_heuristic(layout, unload_list, load_list)
                    
                    stuff = (current_cost + cost + h, current_cost + cost, h, layout, unload_list, load_list)
                    frontier.put(stuff)
        print("solution not found")
            
    # find highest empty slot in each column
    @staticmethod
    def find_top_empty_containers(current_layout):
        empty_spots = []
        transposed_layout = zip(*current_layout)
        for col, column in enumerate(transposed_layout): # iterate through columns
            for row, item in enumerate(column):
                if(item.name == "UNUSED"):
                    empty_spots.append((row, col))
                    break
            empty_spots.append((8, col))
        return empty_spots

    # reconstruct path when solution is found
    @staticmethod
    def reconstruct_path(solution_map, current_layout):
        # TODO: reconstruct solution
        # path = []
        # current = tuple(tuple(row) for row in current_layout)
        
        # while current in solution_map:
        #     path.append(current_layout)
        #     current_layout = solution_map[current]
        #     current = tuple(tuple(row) for row in current_layout)

        # path.reverse()
        # return path
        return current_layout

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
        for container, _, _ in unload_list:
            if container.name in ship_containers:
                return False

        return True
    
    # check if containers to load are on the ship
    def check_load_goal(ship_layout, load_list):
        # check if every container in load_list is in ship_containers
        for container, location, _ in load_list:
            x, y = location
            if ship_layout[x][y].name != container.name:
                return False

        return True

    # calculate the total heuristic
    @staticmethod
    def calc_heuristic(ship_layout, unload_list, load_list):
        return Load.calc_unload_h(ship_layout, unload_list) + Load.calc_load_h(load_list)


    # part of heuristic for unloading
    @staticmethod
    def calc_unload_h(ship_layout, unload_list):
        sum = 0
        lowest_per_col = {}

        for _, _, curr_location in unload_list:
            r, c = curr_location
            # TODO: revise this code later
            # old_low = 8

            # if c not in lowest_per_col:
            #     lowest_per_col[c] = r
            # elif r < lowest_per_col[c]:
            #     old_low = lowest_per_col[c]
            #     lowest_per_col[c] = r
            # else:
            #     old_low = lowest_per_col[c]
            #     sum -= 1

            # # Check if there are containers on top (add to h)
            # for row in range(r + 1, 8):  # Iterate above the current position
            #     if ship_layout[row][c].name != "UNUSED" and row < old_low:  # Check if empty
            #         sum += 1
            #     else:
            #         break
            # distance to (8,0)
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
            r, c = location
            x, y = current_location
            # sum += Load.load_unload_heuristic(r, c)
            sum += abs(r-x) + abs(c-y)
        return sum

    @staticmethod
    def print_layout(test_layout):
        if(test_layout==None):
            print("Cannot print layout")
            return

        for x, row in enumerate(reversed(test_layout)):
            row_output = ""
            for y, container in enumerate(row):
                row_output += f"({7-x},{y}): {container.name:6}, "
            print(row_output)





# testing
# Load.run(ship.Ship)
# print(ship.Ship.vector[8][12])

# container = Container("A", 120)
# print(container.name)
# print(container.weight)


# Testing
container1 = Container("A", 120)
container2 = Container("B", 200)
container3 = Container("C", 400)
container4 = Container("D", 500)
container5 = Container("E", 2200)
container6 = Container("F", 300)

# 8 x 12
test_layout = [[Container() for i in range(0,12)] for j in range(0,8)]
# test_layout[0][0] = container1
# test_layout[1][0] = container2
# test_layout[0][2] = container3
# test_layout[1][2] = container5

# Test case for running:
# test_layout2 = Load.run(test_layout, [(container1, (0, 0))], [])
# Load.print_layout(test_layout2)
# unloading
# test_layout2 = Load.run(test_layout, [(container1, (0, 0)), (container3, (0, 2))], [])
# Load.print_layout(test_layout2)
# test_layout2 = Load.run(test_layout, [(container5, (1, 2)), (container3, (0, 2))], [])
# Load.print_layout(test_layout2)
# loading
# test_layout2 = Load.run(test_layout, [], [(container4, (0, 3))])
# Load.print_layout(test_layout2)
test_layout2 = Load.run(test_layout, [], [(container4, (0, 0)), (container5, (0, 11))])
Load.print_layout(test_layout2)
# both
# test_layout2 = Load.run(test_layout, [(container1, (0, 0))], [(container4, (0, 3)), (container5, (0, 2))])
# Load.print_layout(test_layout2)

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
# layout2 = [[Container() for i in range(0,12)] for j in range(0,8)]
# layout2[0][0] = load_container
# layout2[1][0] = load_container
# layout2[2][0] = load_container
# layout2[0][1] = load_container
# layout2[0][4] = load_container
# output = Load.find_top_empty_containers(layout2)
# for item in output:
#     cords = "(" + str(item[0]) + ", " + str(item[1]) + ")"
#     print(cords)
