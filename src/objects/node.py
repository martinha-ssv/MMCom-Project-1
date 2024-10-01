class Node():
    def __init__(self, coordinates, id):
        self.coordinates = coordinates
        self.id = id

    def get_x(self):
        return self.coordinates[0]

    def get_y(self):
        return self.coordinates[1]

    def get_id(self):
        return self.id