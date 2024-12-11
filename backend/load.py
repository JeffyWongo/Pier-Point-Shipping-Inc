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
    def __init__(self):
        pass

    # function called by main program
    @staticmethod
    def run(ship_layout, unload_list, load_list):
        # adds their current location to the tuples
        # 1. unload containers are at where they're specified
        # 2. load container are at (8, 0)
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
        initial_h = Load.calc_heuristic(full_unload_list, full_load_list)
        frontier.put((initial_h, 0, initial_h, copy.deepcopy(ship_layout), full_unload_list, full_load_list))
        # key is layout (hashable). value is previous layout
        hashed_layout = tuple(tuple(row) for row in ship_layout)
        explored[hashed_layout] = True
        solution_map[hashed_layout] = (ship_layout, None, None)

        # loops for each state in queue
        while not frontier.empty():
            _, current_cost, _, current_layout, unload_list, load_list = frontier.get()

            # check goal state
            if(Load.check_goal_state(unload_list, load_list)):
                # print(f"GOAL: {current_cost}, {current_h}") # (good line for testing)
                return Load.reconstruct_path(solution_map, current_layout)

            # finds all empty spots in each column. 3rd line filters
            # find all topmost containers in each column
            empty_spots = Load.find_top_empty_containers(current_layout)
            top_containers = [(x - 1, y) for x, y in empty_spots if x > 0 and current_layout[x-1][y].name!="NAN"]

            # Moves:
            # 1. Every container to load to empty_spots (only to where we want them to go)
            # 2. Every container in top_containers to empty_spots
            # 3. Every container in top_containers to unloaded

            # every load_list containers to their desired location
            for load_index, info in enumerate(load_list):
                container, desired_cords, current_cords = info
                # skip element if already in desired location
                if(current_cords == desired_cords):
                    continue
                
                # move directly to desired_cords
                # check if moving there is possible
                r, c = desired_cords
                if(desired_cords in empty_spots):
                    new_layout = copy.deepcopy(current_layout)
                    new_layout[r][c] = container

                    new_load_list = copy.deepcopy(load_list)
                    new_load_list[load_index] = (container, desired_cords, desired_cords)

                    Load.push_new_state(frontier, explored, solution_map, new_layout, current_layout, unload_list, new_load_list, current_cost, (8, 0), desired_cords)

            # every top_container containers to empty_spots or unload
            for container_cord in top_containers:
                r, c = container_cord

                # checks if container (to move) is on load list
                # if yes, skip
                is_on_load_list = False
                for load_index, load_container in enumerate(load_list):
                    if(load_container[2] == container_cord):
                        is_on_load_list = True
                        break
                if(is_on_load_list):
                    continue

                # checks if container (to move) is on unload list
                # if yes, note that and which element in the unload list
                is_on_unload_list = False
                unload_index = -1
                for idx, unload_container in enumerate(unload_list):
                    if(unload_container[2] == container_cord):
                        is_on_unload_list = True
                        unload_index = idx
                        break

                # move to every possible empty spot
                for empty_cord in empty_spots:
                    # if top_container and empty_spot are same col, skip. will lead to floating container
                    # if empty cord is beyond bounds, skip
                    if(empty_cord[1]==c or empty_cord[0]==8):
                        continue

                    new_layout = copy.deepcopy(current_layout)
                    new_unload_list = copy.deepcopy(unload_list)

                    # assumes heuristic functions will take care of everything
                    # update current_position in unload list if it's on
                    if is_on_unload_list:
                        unload_item = list(new_unload_list[unload_index])
                        unload_item[2] = empty_cord
                        new_unload_list[unload_index] = tuple(unload_item)

                    # swap
                    new_layout[empty_cord[0]][empty_cord[1]], new_layout[r][c] = (
                        new_layout[r][c], 
                        new_layout[empty_cord[0]][empty_cord[1]]
                    )

                    Load.push_new_state(frontier, explored, solution_map, new_layout, current_layout, new_unload_list, load_list, current_cost, container_cord, empty_cord)

                # if container (to move) is on unload list, unload
                if is_on_unload_list:
                    new_layout = copy.deepcopy(current_layout)
                    new_layout[r][c] = Container()

                    # update current_position in unload list
                    new_unload_list = copy.deepcopy(unload_list)
                    unload_item = list(new_unload_list[unload_index])
                    unload_item[2] = (8,0)
                    new_unload_list[unload_index] = tuple(unload_item)
                    
                    Load.push_new_state(frontier, explored, solution_map, new_layout, current_layout, new_unload_list, load_list, current_cost, container_cord, (8, 0))
        return None
            
    # find highest empty slot in each column
    @staticmethod
    def find_top_empty_containers(current_layout):
        empty_spots = []
        transposed_layout = zip(*current_layout)
        for col, column in enumerate(transposed_layout): # iterate through columns
            spot_found = False
            # iterate through rows (upward) till empty column is found
            for row, item in enumerate(column):
                if(item.name == "UNUSED"):
                    empty_spots.append((row, col))
                    spot_found = True
                    break
            # if empty container not found in column
            if not spot_found:
                empty_spots.append((8, col))
        return empty_spots

    @staticmethod
    def push_new_state(frontier, explored, solution_map, new_layout, current_layout, unload_list, load_list, current_cost, container_cord, empty_cord):
        # make layout hashable
        hashable_layout = tuple(tuple(row) for row in new_layout)

        # check if the layout has already been explored
        if explored.get(hashable_layout, False):
            return
        explored[hashable_layout] = True

        # record the current layout as the parent of the new layout in solution_map
        solution_map[hashable_layout] = (current_layout, container_cord, empty_cord)

        # calculate the cost and heuristic
        highest_empty_r = Load.find_highest_between(current_layout, container_cord, empty_cord)
        cost = abs(container_cord[1] - empty_cord[1]) + abs(highest_empty_r - container_cord[0]) + abs(highest_empty_r - empty_cord[0])
        h = Load.calc_heuristic(unload_list, load_list)

        # add the new state to the frontier
        frontier.put((current_cost + cost + h, current_cost + cost, h, new_layout, unload_list, load_list))

    # finds highest container between container (to move) and empty_cord
    # then add 1 to that number for the empty row number
    def find_highest_between(current_layout, container_cord, empty_cord):
        empty_spots = Load.find_top_empty_containers(current_layout)
        highest_empty_r = max(container_cord[0], empty_cord[0])
        
        for col_index in range(min(container_cord[1], empty_cord[1]), max(container_cord[1], empty_cord[1])):
            candidate_r = empty_spots[col_index][0]
            # container to move is not an empty spot (edge case), minus 1
            if(col_index==container_cord[1]):
                candidate_r -= 1
            highest_empty_r = max(highest_empty_r, candidate_r)
        return highest_empty_r

    # reconstruct path when solution is found
    # returns list of tuple (steps)
    # each tuple has (current_layout, location of next container to move, location to move that container to)
    @staticmethod
    def reconstruct_path(solution_map, final_layout):
        path = []
        hashable_layout = tuple(tuple(row) for row in final_layout)
        layout_info = solution_map[hashable_layout]

        # None because nothing has to move in the final layout
        path.append((final_layout, None, None))

        while layout_info[1] is not None:
            path.append(layout_info)
            hashable_layout = tuple(tuple(row) for row in layout_info[0])

            previous_layout_info = solution_map[hashable_layout]
            layout_info = previous_layout_info

        path.reverse()

        return path

    # check if goal state is satisfied
    @staticmethod
    def check_goal_state(unload_list, load_list):
        return Load.check_unload_goal(unload_list) and Load.check_load_goal(load_list)
    
    # check if containers to unload are off the ship (and buffer)
    @staticmethod
    def check_unload_goal(unload_list):
        for _, _, current_location in unload_list:
            if current_location != (8,0):
                return False
        return True
    
    # check if containers to load are on the ship
    def check_load_goal(load_list):
        for _, initial_location, current_location in load_list:
            if initial_location != current_location:
                return False

        return True

    # calculate the total heuristic
    @staticmethod
    def calc_heuristic(unload_list, load_list):
        return Load.calc_unload_h(unload_list) + Load.calc_load_h(load_list)

    # part of heuristic for unloading
    @staticmethod
    def calc_unload_h(unload_list):
        sum = 0
        for _, _, curr_location in unload_list:
            r, c = curr_location
            sum += abs(8 - r) + c
        return sum

    # part of heuristic for loading
    @staticmethod
    def calc_load_h(load_list):
        sum = 0
        for _, location, current_location in load_list:
            r, c = location
            x, y = current_location
            sum += abs(r-x) + abs(c-y)
        return sum

    # check if two layouts are equal (for testing)
    @staticmethod
    def equal_states(layout1, layout2):
        for r in range(8):
            for c in range(12):
                container1 = layout1[r][c]
                container2 = layout2[r][c]
                if container1.name != container2.name or container1.weight != container2.weight:
                    return False
        return True
    
    # print ship layout (for testing)
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


if __name__ != "__main__":
    pass
else:
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
    # test_layout[0][2] = container1
    # test_layout[1][2] = container2
    # test_layout[0][10] = container4
    # test_layout[0][1] = nan_container

    # extreme case
    # for i in range(8):
    #     test_layout[i][1] = container2
    # test_layout[0][0] = container1
    # test_layout[1][0] = container3

    # test_output = Load.run(test_layout, [(container1, (0,0))], [])

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
    # test_output = Load.run(test_layout, [(container1, (0, 0)), (container1, (0, 2))], [(container4, (1, 9))])

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
    test_layout[1][1] = container4

    test_output = Load.run(test_layout, [(container1, (0, 1)), (container3, (0, 3))], [(container6, (1, 0))])

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
