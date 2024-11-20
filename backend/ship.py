"""
Purpose of class Ship:
    1. Create a 8*12 vector to store as ship
    2. Able to be accessed by manifest, load, and balancing program
    3. Each location stores: x y location, weight, and tags
"""

class Ship:
    def __init__(self, x: int, y: int, weight: int, tag: str):
        self.x = x
        self.y = y
        self.weight = weight
        self.tag = tag # this helps to identify the container type

    #--------------------------------------------------------------
    def get_location(self) -> tuple:
        return self.x, self.y
    
    def get_weight(self) -> int:
        return self.weight
    
    def get_tag(self) -> str:
        return self.tag
    
    #--------------------------------------------------------------
    def set_location(self, x: int, y: int):
        self.x = x
        self.y = y

    def set_weight(self, weight: int):
        self.weight = weight

    def set_name(self, tag:str):
        self.tag = tag

    #--------------------------------------------------------------
    def __str__(self):
        return f"[{self.x}, {self.y}], {{{self.weight}}}, {self.tag}"