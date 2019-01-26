"""
Book: Clean code in python.
Chapter: Container Objects, p45.

Container is an object that implements __contains__,
which is invoked by the 'in' keyword in Python.
"""


class Boundaries:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def __contains__(self, coordinate):
        x, y = coordinate
        return 0 <= x < self.width and 0 <= y < self.height 


class Grid:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.limits = Boundaries(height, width)

    def __contains__(self, coordinates):
        return coordinates in self.limits


grid = Grid(10, 10)
coord = (3, 5)
print(coord in grid)
