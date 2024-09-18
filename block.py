from gameobject import GameObject

class Block(GameObject):
    def __init__(self, height, width, x, y, color):
        super().__init__(height, width, x, y, color)