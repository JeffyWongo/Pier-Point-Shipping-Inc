class Container:
    def __init__(self, row, col, weight, name, color):
        self.row = row
        self.col = col
        self.weight = weight
        self.name = name
        self.color = color
        
    def show_info(self): # for debugging
        print(f"Container Info:")
        print(f"  Position: ({self.row}, {self.col})")
        print(f"  Name: {self.name}")
        print(f"  Weight: {self.weight}")
        print(f"  Color: {self.color}")