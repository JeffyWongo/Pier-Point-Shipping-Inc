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
        # key is layout (hashable). value is previous layout
        hashed_layout = tuple(tuple(row) for row in ship_layout)
        explored[hashed_layout] = True
        solution_map[hashed_layout] = (ship_layout, None, None)

        # loops for each state in queue
        while not frontier.empty():
            _, current_cost, current_h, current_layout, unload_list, load_list = frontier.get()

            # check goal state
            if(Load.check_goal_state(current_layout, unload_list, load_list)):
                print(f"GOAL: {current_cost}, {current_h}")
                return Load.reconstruct_path(solution_map, current_layout)

            # finds all empty spots in each column. 3rd line filters
            # find all topmost containers in each column
            empty_spots = Load.find_top_empty_containers(current_layout)
            top_containers = [(x - 1, y) for x, y in empty_spots if x > 0 and current_layout[x-1][y].name!="NAN"]

            # Moves:
            # 1. Every container to load to empty_spots
            # 2. Every container in top_containers to empty_spots
            # 3. Every container in top_containers to unloaded

            # every load_list containers to empty_spots
            for load_index, info in enumerate(load_list):
                container, desired_cords, current_cords = info
                if(current_cords == desired_cords):
                    continue
                
                # move directly to desired_cords
                # check if empty
                r, c = desired_cords
                if(desired_cords in empty_spots):
                    layout = copy.deepcopy(current_layout)
                    layout[r][c] = container

                    new_load_list = copy.deepcopy(load_list)
                    new_load_list[load_index] = (container, desired_cords, desired_cords)

                    Load.push_new_state(frontier, explored, solution_map, layout, current_layout, unload_list, new_load_list, current_cost, (8, 0), desired_cords)

            # every top_container containers to empty_spots or unload
            for container_cord in top_containers:
                r, c = container_cord

                is_on_load_list = False
                for load_index, load_container in enumerate(load_list): # TODO: doesn't deal with duplicates
                    if(load_container[2] == container_cord):
                        is_on_load_list = True
                        break
                if(is_on_load_list):
                    continue

                is_on_unload_list = False
                unload_index = -1
                for idx, unload_container in enumerate(unload_list): # TODO: doesn't deal with duplicates
                    if(unload_container[2] == container_cord):
                        is_on_unload_list = True
                        unload_index = idx
                        break

                # move to every possible empty spot
                for empty_cord in empty_spots:
                    # if top_container and empty_spot are same col. will lead to floating container
                    if(empty_cord[1]==c or empty_cord[0]==8):
                        continue

                    # find row of highest container between container to move and empty spot
                    highest_empty_r = r
                    for col_index in range(min(c, empty_cord[1]), max(c, empty_cord[1])):
                        if(col_index==c):
                            continue
                        highest_empty_r = max(empty_spots[col_index][0], highest_empty_r)

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

                    # check if state is already explored
                    # hashable_layout = tuple(tuple(row) for row in layout)
                    # if explored.get(hashable_layout, False):
                    #     continue
                    # else:
                    #     explored[hashable_layout] = True
                    #     # key is layout (hashable). value is previous layout
                    #     solution_map[hashable_layout] = (current_layout, container_cord, empty_cord)
                    #     # add new state to frontier
                    #     cost = abs(empty_cord[1] - c) + abs(highest_empty_r - r) + abs(highest_empty_r - empty_cord[0])
                    #     h = Load.calc_heuristic(layout, unload_list, load_list)
                    #     stuff = (current_cost + cost + h, current_cost + cost, h, layout, unload_list, load_list)
                    #     frontier.put(stuff)
                    Load.push_new_state(frontier, explored, solution_map, layout, current_layout, unload_list, load_list, current_cost, container_cord, empty_cord)

                    
                if is_on_unload_list:
                    layout = copy.deepcopy(current_layout)
                    layout[r][c] = Container()

                    unload_item = list(unload_list[unload_index])
                    unload_item[2] = (8,0)
                    unload_list[unload_index] = tuple(unload_item)
                    
                    Load.push_new_state(frontier, explored, solution_map, layout, current_layout, unload_list, load_list, current_cost, container_cord, (8, 0))
        return None
            
    # find highest empty slot in each column
    @staticmethod
    def find_top_empty_containers(current_layout):
        empty_spots = []
        transposed_layout = zip(*current_layout)
        for col, column in enumerate(transposed_layout): # iterate through columns
            spot_found = False
            for row, item in enumerate(column):
                if(item.name == "UNUSED"):
                    empty_spots.append((row, col))
                    spot_found = True
                    break
            if not spot_found:
                empty_spots.append((8, col))
        return empty_spots

    @staticmethod
    def push_new_state(frontier, explored, solution_map, new_layout, current_layout, unload_list, load_list, current_cost, container_cord, empty_cord):
        # make layout hashable
        hashable_layout = tuple(tuple(row) for row in new_layout)

        # Check if the layout has already been explored
        if explored.get(hashable_layout, False):
            return
        explored[hashable_layout] = True

        # Record the current layout as the parent of the new layout in solution_map
        solution_map[hashable_layout] = (current_layout, container_cord, empty_cord)

        # Calculate the cost and heuristic
        # cost = abs(8 - r) + c
        cost = abs(container_cord[0] - empty_cord[0]) + abs(container_cord[1] - empty_cord[1])
        h = Load.calc_heuristic(new_layout, unload_list, load_list)

        # Add the new state to the frontier
        frontier.put((current_cost + cost + h, current_cost + cost, h, new_layout, unload_list, load_list))

    # reconstruct path when solution is found
    @staticmethod
    def reconstruct_path(solution_map, final_layout):
        path = []
        hashable_layout = tuple(tuple(row) for row in final_layout)
        layout_info = solution_map[hashable_layout]

        path.append((final_layout, None, None))

        while layout_info[1] is not None:
            path.append(layout_info)
            hashable_layout = tuple(tuple(row) for row in layout_info[0])

            previous_layout_info = solution_map[hashable_layout]
            layout_info = previous_layout_info


        path.reverse()
        
        return path

    @staticmethod
    def equal_states(layout1, layout2):
        for r in range(8):
            for c in range(12):
                container1 = layout1[r][c]
                container2 = layout2[r][c]
                if container1.name != container2.name or container1.weight != container2.weight:
                    return False
        return True

    # check if goal state is satisfied
    @staticmethod
    def check_goal_state(ship_layout, unload_list, load_list):
        return Load.check_unload_goal(ship_layout, unload_list) and Load.check_load_goal(ship_layout, load_list)
    
    # check if containers to unload are off the ship (and buffer)
    @staticmethod
    def check_unload_goal(ship_layout, unload_list):
        ship_containers = [container.name for row in ship_layout for container in row]

        # check if every container in unload_list is in ship_containers
        for container, _, _  in unload_list:
            if container.name in ship_containers:
                return False
        # for container, initial_location, current_location in unload_list:
        #     r,c = initial_location
        #     if ship_layout[r][c].name != container.name:
        #         return False
        #     if current_location != (8,0):
        #         return False

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





# Testing
container1 = Container("A", 120)
container2 = Container("B", 200)
container3 = Container("C", 400)
container4 = Container("D", 500)
container5 = Container("E", 2200)
container6 = Container("F", 300)
container7 = Container("G", 212)
container8 = Container("H", 1212)
nan_container = Container("NAN", -1)

# 8 x 12
test_layout = [[Container() for i in range(0,12)] for j in range(0,8)]
# test_layout[0][0] = container1
# test_layout[1][0] = container1
# test_layout[0][2] = container3
# test_layout[0][10] = container4
# test_layout[0][1] = nan_container

# Test case for running:
# unloading
# test_output = Load.run(test_layout, [(container1, (0, 0))], [])
# test_output = Load.run(test_layout, [(container1, (0, 0)), (container3, (0, 2))], [])
# loading
# test_output = Load.run(test_layout, [], [(container4, (0, 3))])
# test_output = Load.run(test_layout, [], [(container4, (0, 0)), (container5, (0, 11))])
# both
# test_output = Load.run(test_layout, [(container1, (0, 0))], [(container4, (0, 10)), (container5, (0, 11))])
# test_output = Load.run(test_layout, [(container1, (0, 0))], [(container6, (0, 11))])
# test_output = Load.run(test_layout, [(container1, (0, 0)), (container3, (0, 2))], [(container6, (0, 11))])

# NAN test case
# for i in range(0, 12):
#     test_layout[0][i] = nan_container

# test_output = Load.run(test_layout, [(nan_container, (0, 0))], [])


# Given test cases
# test case 1
# test_layout[0][0] = nan_container
# test_layout[0][11] = nan_container
# test_layout[0][1] = container1
# test_layout[0][2] = container2

# test_output = Load.run(test_layout, [(container1, (0,1))], [])

# test case 2
# test_layout[0][0] = nan_container
# test_layout[0][1] = nan_container
# test_layout[0][2] = nan_container
# test_layout[0][9] = nan_container
# test_layout[0][10] = nan_container
# test_layout[0][11] = nan_container
# test_layout[1][0] = nan_container
# test_layout[1][11] = nan_container
# test_layout[2][0] = container1
# test_layout[1][1] = container2
# test_layout[0][3] = container3
# test_layout[0][8] = container4

# test_output = Load.run(test_layout, [], [(container5, (0, 6))])

# test case 3
# test_layout[0][0] = container1
# test_layout[0][1] = container2
# test_layout[0][2] = container3
# test_layout[0][3] = container4
# test_layout[1][0] = container5
# test_layout[1][1] = container6

# test_output = Load.run(test_layout, [(container2, (0, 1))], [(container4, (0, 10)), (container7, (2,0))])

# test case 4
# for i in range(0, 12):
#     test_layout[0][i] = nan_container
# test_layout[1][0] = nan_container
# test_layout[1][11] = nan_container
# test_layout[1][4] = container1
# test_layout[2][4] = container2
# test_layout[3][4] = container3
# test_layout[4][4] = container4
# test_layout[5][4] = container5
# test_layout[6][4] = container6
# test_layout[7][4] = container7

# test_output = Load.run(test_layout, [(container6, (6, 4))], [(container8, (2, 0))])

# test case 5
# test_layout[0][0] = nan_container
# test_layout[0][11] = nan_container
# test_layout[0][1] = container1
# test_layout[0][2] = container2
# test_layout[0][3] = container3
# test_layout[0][4] = container4
# test_layout[0][5] = container5

# test_output = Load.run(test_layout, [(container3, (0, 3)), (container4, (0, 4))], [(container6, (1, 1)), (container5, (1, 5))])

# test case 6
test_layout[0][0] = nan_container
test_layout[0][11] = nan_container
test_layout[0][1] = container1
test_layout[0][2] = container2
test_layout[0][3] = container3
# test_layout[1][1] = container4

test_output = Load.run(test_layout, [(container1, (0, 1)), (container3, (0, 3))], [(container6, (0, 10))])

if test_output is not None:
    print("SOLUTION:")
    for item in test_output:
        Load.print_layout(item[0])
        print(f"{item[1]} -> {item[2]}")
        print("=============")
else:
    print("No SOLUTION")
    Load.print_layout(test_layout)


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
