"""
Purpose of class Ship:
    1. Create a 12*8 vector to store as ship
    2. Able to be accessed by manifest, load, and balancing program
    3. Each location stores: x y location, weight, and names
    4. When an item is moved, note that this program !!! WILL NOT !!! delete the source item

    ADDED:
    1. add new content in the bridge
    2. move imported content from a place to UNUSED
    3. move imported content from a place to NAN, and should prompt rejected
    4. move imported content to another place already with content, should reject

    REMEMBER:
    When your program finished running, RUN set_location again to update the ship :)!
"""
# WATCHOUT, this is a ZERO-based array

class Ship:
    def __init__(self):
        self.vector = [
            [{"y": y, "x": x, "weight": 0, "name": "UNUSED"} for x in range(12)]
            for y in range(8)
        ]
    #VALIDATIONS--------------------------------------------------------------
    def validate_input(self, y: int, x: int):
        if not (0 <= x < 12 and 0 <= y < 8):
            raise ValueError(f"Invalid coordinated: ({y + 1}, {x + 1}). Must be with in 12*8 grid.")
        
    def validate_weight(self, weight: int):
        if not (0 <= weight <= 99999):
            raise ValueError(f"Invalid weight: {weight}. Must be between 0 and 99999 lbs.")
        
    def validate_access(self, y: int, x: int):
        self.validate_input(y, x) # implement validate input here, for simplicity
        if self.vector[y][x]["name"] == "NAN" and self.vector[y][x]["weight"] != 0:
            raise PermissionError(f"Access denied for ({y}, {x}). Container is marked as 'NAN.'")
        
    #GETS--------------------------------------------------------------
    def get_location(self, y: int, x: int) -> dict:
        self.validate_access(y, x)
        return self.vector[y][x]
    
    def get_weight(self, y: int, x: int) -> int:
        self.validate_access(y, x)
        return self.vector[y][x]["weight"]
    
    def get_name(self, y: int, x: int) -> str:
        self.validate_access(y, x)
        return self.vector[y][x]["tag"]
    
    #SETS--------------------------------------------------------------
    def set_location(self, y: int, x: int, weight: int, name: str):
        self.validate_access(y, x)
        self.validate_weight(weight)
        # check if occupied
        if self.vector[y][x]["name"] != "UNUSED" or self.vector[y][x]["weight"] != 0:
            raise ValueError(f"Location ({y + 1}, {x + 1} already occupied)")
        self.vector[y][x]["weight"] = weight
        self.vector[y][x]["name"] = name

    def set_weight(self, y: int, x: int, weight: int):
        self.validate_access(y, x)
        self.validate_weight(weight)
        self.vector[y][x]["weight"] = weight

    def set_name(self, y: int, x: int, name:str):
        if name == "NAN": # can mark as NAN ONCE
            self.vector[y][x]["name"] = name
        else:
            self.validate_access(y, x)
            self.vector[y][x]["name"] = name

    #--------------------------------------------------------------
    def __str__(self):
        return f"[{self.y}, {self.x}], {{{self.weight}}}, {self.name}"