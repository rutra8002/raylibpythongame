import raylib
from blocks.block import Block

class LavaBlock(Block):
    def __init__(self, height, width, x, y, color):
        super().__init__(height, width, x, y, color)

    def draw(self):
        raylib.DrawRectangle(int(self.x), int(self.y), self.width, self.height, self.color)

    def check_vertical_collision(self, other):
        collision_side = super().check_vertical_collision(other)
        if collision_side:
            other.speed = 6.9
            if other.time_since_last_damage > 0.1:
                other.take_damage(10)
                other.time_since_last_damage = 0
        return collision_side

    def check_horizontal_collision(self, other):
        collision_side = super().check_horizontal_collision(other)
        if collision_side:
            other.speed = 6.9
            if other.time_since_last_damage > 0.1:
                other.take_damage(10)
                other.time_since_last_damage = 0
        return collision_side
