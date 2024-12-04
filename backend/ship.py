"""
Purpose of class Ship:
    1. Create a 12*8 vector to store as ship
    2. When an item is moved, note that this program !!! WILL NOT !!! delete the source item

    ADDED:
    1. add new content in the bridge
    2. move imported content from a place to UNUSED
    3. move imported content from a place to NAN, and should prompt rejected
    4. move imported content to another place already with content, should reject

    REMEMBER:
    When your program finished running, RUN set_location again to update the ship :)!
"""
# !!!!!!!!! WATCHOUT, this is a ZERO-based array, so when inputting (1,3), should set as (0,2)

from container import Container

class Ship:
    def __init__(self, name = "Ship"):
        self.grid = [["Place" for _ in range(12)] for _ in range(8)]
        self.name = name # distinguse between SHIP and BUFFER

    #VALIDATIONS--------------------------------------------------------------
    def validate_input(self, y: int, x: int):
        if not (0 <= x < 12 and 0 <= y < 8):
            raise ValueError(f"Invalid coordinated: ({y + 1}, {x + 1}). Must be with in 12*8 grid.")
        
    def validate_access(self, y: int, x: int):
        self.validate_input(y, x) # implement validate input here, for simplicity
        container = self.grid[y][x]
        if container != "Place" and container.name == "NAN" and container.weight != 0:
            raise PermissionError(f"Access denied for ({y}, {x}). Container is marked as 'NAN.'")
        
    #SETTING CONTAINER--------------------------------------------------------------
    def place_container(self, y: int, x: int, container: Container):
        self.validate_input(y, x)
        self.validate_access(y, x)
        if self.grid[y][x] != "Place":
            raise ValueError(f"Cannot place container at ({y + 1}, {x + 1}. Spot already occupied.)")
        container.set_location(self.name, y, x)
        self.grid[y][x] = container

    def remove_container(self, y: int, x: int) -> Container:
        self.validate_access(y, x)
        container = self.grid[y][x]
        if container == "Place":
            raise ValueError(f"No container to remove at ({y + 1}, {x + 1}).")
        self.grid[y][x] = "Place"
        container.set_location(None, None, None)
        return container
    
    #GETS--------------------------------------------------------------
    def get_container(self, y: int, x: int) -> Container:
        self.validate_access(y, x)
        container = self.grid[y][x]
        if container == "Place":
            raise ValueError(f"No container at ({y + 1}, {x + 1}).")
        return container
    
    def get_ALLcontainerS(self):
        containerS = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] != "Place":
                    containerS.append(self.grid[y][x])
        return containerS

    #--------------------------------------------------------------
    def __str__(self):
        grid_str = []
        for row in self.grid:
            row_str = [
                str(container) if container != "Place" else "Empty"
                for container in row
            ]
            grid_str.append(" | ".join(row_str))
        return "\n".join(grid_str)