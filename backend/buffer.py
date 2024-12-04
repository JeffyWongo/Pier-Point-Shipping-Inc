"""
Purpose of class Buffer:
    Same as ship, just 24 * 4 (x * y) grid
"""

# !!!!!!!!! WATCHOUT, this is a ZERO-based array, so when inputting (1,3), should set as (0,2)

from ship import Ship

class Buffer(Ship):
    def __init__(self, name="Buffer"):
        super().__init__(name)
        self.grid = [["Place" for _ in range(24)] for _ in range(4)]

    def validate_input(self, y, x):
        if not (0 <= x < 24 and 0 <= y < 4): # since buffer is 24 * 4
            raise ValueError(f"Invalid coordinated: ({y + 1}, {x + 1}). Must be with in 24*4 grid.")