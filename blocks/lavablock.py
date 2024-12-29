import raylib
from blocks.block import Block

class LavaBlock(Block):
    def __init__(self, height, width, x, y, color):
        super().__init__(height, width, x, y, color)

    def draw(self):
        raylib.DrawRectangle(int(self.x), int(self.y), self.width, self.height, self.color)

    def check_horizontal_collision(self, other):
        pass

    def check_vertical_collision(self, other):
        pass