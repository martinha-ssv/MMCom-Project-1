from src.objects.node import Node

class Load():
    def __init__(self, line: list):
        self.node = Node.getNodeById(int(line[0]))
        self.magnitude = float(line[2])
        self.direction = line[3]
        self.node.loads.append(self)