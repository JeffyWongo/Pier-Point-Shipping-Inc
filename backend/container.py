"""
Purpose of Container class:
    1. Able to be accessed by manifest, load, and balancing program
    2. Each location stores: x + y location, weight, and names
    3. When an item is moved, note that this program !!! WILL NOT !!! delete the source item

    REMEMBER:
    When your program finished running, RUN set_location again to update the ship :)!
"""
# added "Placement," so we know inside the program is the container is on the SHIP or BUFFER
# !!!!!!!!! WATCHOUT, this is a ZERO-based array, so when inputting (1,3), should set as (0,2)


class Container:
    def __init__(self, weight: int, name: str, placement: str = "Ship", y: int = None, x: int = None):
        if not (0 <= weight <= 99999): # do validation here instead, since alr inputting
            raise ValueError(f"Invalid weight: {weight}. Must be between 0 and 99999 lbs.")
        self.weight = weight
        self.name = name
        self.placement = placement
        self.y = y
        self.x = x

    def set_location(self, placement: str, y: int, x: int): # keep updating, easy access
        self.placement = placement
        self.y = y
        self.x = x

    def get_location(self):
        return{"placement": self.placement, "y": self.y, "x": self.x}
    
    def __str__(self):
        return f"Container(name={self.name}, weight={self.weight}, location=({self.y}, {self.x}, placement={self.placement}))"