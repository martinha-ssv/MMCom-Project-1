class Node():
    def __init__(self, coordinates, id):
        self.coordinates = coordinates
        self.id = id

    def x(self):
        return self.coordinates[0]

    def y(self):
        return self.coordinates[1]