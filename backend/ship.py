"""
Purpose of class Ship:
    1. Create a 8*12 vector to store as ship
    2. Able to be accessed by manifest, load, and balancing program
    3. Each location stores: x y location, weight, and tags
"""

class Ship:
    def __init__(self):
        self.vector = [
            [{"x": x, "y": y, "weight": 0, "tag": None} for y in range(12)]
            for x in range(8)
        ]
    #--------------------------------------------------------------
    def validate_input(self, x: int, y: int):
        if not (0 <= x < 8 and 0 <= y < 12):
            raise ValueError(f"Invalid coordinated: ({x}, {y}). Must be with in 8*12 grid.")
        
    def validate_weight(self, weight: int):
        if not (0 <= weight <= 99999):
            raise ValueError(f"Invalid weight: {weight}. Must be between 0 and 99999 lbs.")
        
    #--------------------------------------------------------------
    def get_location(self, x: int, y: int) -> dict:
        self.validate_input(x, y)
        return self.vector[x][y]
    
    def get_weight(self, x: int, y: int) -> int:
        self.validate_input(x, y)
        return self.vector[x][y]["weight"]
    
    def get_tag(self, x: int, y: int) -> str:
        self.validate_input(x, y)
        return self.vector[x][y]["tag"]
    
    #--------------------------------------------------------------
    def set_location(self, x: int, y: int, weight: int, tag: str):
        self.validate_input(x, y)
        self.validate_weight(weight)
        self.vector[x][y]["weight"] = weight
        self.vector[x][y]["tag"] = tag

    def set_weight(self, x: int, y: int, weight: int):
        self.validate_input(x, y)
        self.validate_weight(weight)
        self.vector[x][y]["weight"] = weight

    def set_name(self, x: int, y: int, tag:str):
        self.validate_input(x, y)
        self.vector[x][y]["tag"] = tag

    #--------------------------------------------------------------
    def __str__(self):
        return f"[{self.x}, {self.y}], {{{self.weight}}}, {self.tag}"