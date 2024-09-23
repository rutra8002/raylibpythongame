import pyray
from block import Block

class LavaBlock(Block):
    def __init__(self, height, width, x, y, color):
        super().__init__(height, width, x, y, color)

    def check_vertical_collision(self, other):
        collision_side = super().check_vertical_collision(other)
        if collision_side == "top":
            other.vy = 0
            other.y = self.y - other.height
            other.health = 0
        return collision_side

    def draw(self):
        pyray.draw_rectangle(int(self.x), int(self.y), self.width, self.height, self.color)