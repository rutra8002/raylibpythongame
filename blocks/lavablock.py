import os
import pyray
from blocks.block import Block

class LavaBlock(Block):
    def __init__(self, height, width, x, y, color):
        super().__init__(height, width, x, y, color)

    def draw(self):
        pyray.draw_rectangle(int(self.x), int(self.y), self.width, self.height, self.color)