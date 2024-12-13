class Container:
    def __init__(self, row, col, weight, name, color):
        self.row = row
        self.col = col
        self.weight = weight
        self.name = name
        self.color = color
        
    def show_info(self):
        return f"{self.name}\n{self.weight}"