import heapq
from math import inf
from datetime import datetime
from Container import Container

class Ship:
    def __init__(self, initial_ship):
        self.ship = initial_ship # 2d array of Containers
        self.rows = len(initial_ship)
        self.cols = len(initial_ship[0])
        self.left_sum = 0
        self.right_sum = 0
        self.total_sum = 0
        self.optimal_balance = False
        self.previous_best_move = (-1, -1)

    def read_file(self, filename):
        # Log the file opening
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(filename, 'r') as file:
            container_count = 0

            for line in file:
                line = line.strip()
                parts = line.split(", ")

                position = parts[0].strip("[]").split(",")
                weight = int(parts[1].strip("{}"))
                name = parts[2]

                row = 7 - (int(position[0]) - 1)  # flip and adjust for 0-based indexing
                col = int(position[1]) - 1  # Adjust for 0-based indexing

                if name == "NAN":
                    color = 'gray20'  # Special color for "NAN"
                elif name == "UNUSED":
                    color = 'white'
                else:
                    color = 'lightgreen'
                    container_count += 1
                
                container = Container(row=7 - row, col=col + 1, weight=weight, name=name, color=color)
                self.ship[row][col] = container

            # Log the file reading
            log_entry = f"{current_time}        Manifest {filename.split('/')[-1]} is opened, there are {container_count} containers on the ship\n"
            with open("logfile2024.txt", "a") as log_file:
                log_file.write(log_entry)

    def calculate_heuristic(self, row, col, target_row, target_col):
        return abs(row - target_row) + abs(col - target_col)

    def find_shortest_path(self, start_row, start_col):
        open_list = []
        visited = set()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Check for obstacles above
        for r in range(start_row): #can prob change to while loop
            container = self.ship[r][start_col]
            if container and container.weight > 0:  # Obstacle found
                if not self.move_obstacle(r, start_col):
                    print(f"Error: Unable to move obstacle at ({r}, {start_col}).")
                    return []

        move_to_right = start_col < self.cols // 2
        target_col = self.cols // 2 if move_to_right else self.cols // 2 - 1
        target_row = -1

        while 0 <= target_col < self.cols:
            for r in range(self.rows - 1, -1, -1):
                container = self.ship[r][target_col]
                if container.weight == 0:  # Empty spot
                    if r == self.rows - 1 or self.ship[r + 1][target_col].weight > 0:
                        target_row = r
                        break
            if target_row != -1:
                break
            target_col += 1 if not move_to_right else -1

        if target_row == -1:
            print("Error: Unable to find target position.")
            return []

        # Initialize starting node
        start_node = (0, start_row, start_col, [])
        heapq.heappush(open_list, start_node)

        while open_list:
            g, row, col, path = heapq.heappop(open_list)

            if (row, col) == (target_row, target_col):
                return path

            state = (row, col)
            if state in visited:
                continue
            visited.add(state)

            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if not (0 <= new_row < self.rows and 0 <= new_col < self.cols):
                    continue
                if (new_row, new_col) in visited:
                    continue

                container = self.ship[new_row][new_col]
                if container and container.weight > 0:  # Obstacle
                    continue

                new_g = g + 1
                new_h = self.calculate_heuristic(new_row, new_col, target_row, target_col)
                heapq.heappush(open_list, (new_g + new_h, new_row, new_col, path + [(new_row, new_col)]))

        return []

    def calculate_sums(self):
        self.left_sum = self.right_sum = self.total_sum = 0
        for i in range(self.rows):
            for j in range(self.cols):
                container = self.ship[i][j]
                if container.name == "NAN":  # Ignore "NAN"
                    continue
                self.total_sum += container.weight
                if j < self.cols // 2:
                    self.left_sum += container.weight
                else:
                    self.right_sum += container.weight

    def print_ship_weight(self):
        print(f"Weights on left half: {self.left_sum}")
        print(f"Weights on right half: {self.right_sum}")
        print(f"Total weight: {self.total_sum}")

    def is_balanced(self):
        if self.optimal_balance:
            return True

        self.calculate_sums()
        total_weight = self.left_sum + self.right_sum

        if total_weight == 0:
            return True

        tolerance = total_weight * 0.1  # 10%
        return abs(self.left_sum - self.right_sum) <= tolerance

    def move_obstacle(self, row, col):
        target_col = col + 1 if col >= self.cols // 2 else col - 1
        if not (0 <= target_col < self.cols):
            target_col = 6 if col >= self.cols // 2 else 5

        for target_row in range(self.rows - 1, -1, -1):
            target_container = self.ship[target_row][target_col]

            if target_container.name == "NAN" or target_container.name == "UNUSED":  # Empty spot or NaN container
                print(f"Adjusting obstacle position [{row}][{col}] to [{target_row}][{target_col}]")
                # Move the container to the new position
                self.ship[target_row][target_col] = self.ship[row][col]
                # Set the original position to an empty container (None)
                self.ship[row][col].name = "UNUSED"
                self.ship[row][col].weight = 0
                return True
        return False

    def find_best_move(self):
        middle_number = self.total_sum / 2
        best_move = (-1, -1)
        closest_diff = inf
        min_col_diff = inf
        min_row_diff = inf
 
        self.calculate_sums()
        self.print_ship_weight()
        side_condition = self.left_sum > self.right_sum
        range_col = range(self.cols // 2) if side_condition else range(self.cols // 2, self.cols)

        for i in range(self.rows):
            for j in range_col:
                container = self.ship[i][j]

                # Skip empty or "UNUSED" containers
                if container.name in ("NAN", "UNUSED"):
                    continue

                weight = container.weight

                # Calculate the temporary sum based on side_condition
                temp_sum = self.right_sum + weight if side_condition else self.left_sum + weight
                diff = abs(temp_sum - middle_number)

                # Calculate column and row differences for tie-breaking
                col_diff = abs(j - (self.cols // 2 - 1 if side_condition else self.cols // 2))
                row_diff = abs(i - (self.rows - 1))

                # Check if this move is better (closer to balancing the ship)
                if (diff < closest_diff or
                    (diff == closest_diff and col_diff < min_col_diff) or
                    (diff == closest_diff and col_diff == min_col_diff and row_diff < min_row_diff)):
                    closest_diff = diff
                    min_col_diff = col_diff
                    min_row_diff = row_diff
                    best_move = (i, j)

        return best_move

    # def print_best_move(self):
    #     best_move = self.find_best_move()
    #     if self.previous_best_move == best_move:
    #         print("Optimal balance achieved!")
    #         self.optimal_balance = True
    #         return

    #     row, col = best_move
    #     path = self.find_shortest_path(row, col)
    #     if path:
    #         print(f"Target position: [{row}][{col}] = {self.container_weight(row, col)}")
    #         print("Successful! Here's the route:")
    #         for i, step in enumerate(path, 1):
    #             print(f"Step {i}: {step}")
    #         self.modify_ship(path[-1][0], path[-1][1], self.container_weight(row, col))
    #         self.previous_best_move = path[-1]
    #         self.modify_ship(row, col, 0)
    #     else:
    #         print("Failed, can't find a route.")

# if __name__ == "__main__":
#     balance = Balance(file)
#     balance.modify_ship(7, 0, -1)
#     balance.modify_ship(7, 1, 96)
#     balance.modify_ship(7, 2, 8)
#     balance.modify_ship(7, 3, 4)
#     balance.modify_ship(7, 4, 4)
#     balance.modify_ship(7, 5, 1)
#     balance.modify_ship(7, 11, -1)
    
#     balance.print_ship()
#     while not balance.is_balanced():
#         balance.calculate_sums()
#         balance.print_ship_weight()
#         balance.print_best_move()
#         balance.print_ship()
#         balance.calculate_sums()
#         balance.print_ship_weight()

#     print("Congrats! It's balanced now.")