from blocks.block import Block
import images

class SpeedBoostBlock(Block):
    def __init__(self, height, width, x, y, color, speed_boost):
        super().__init__(height, width, x, y, color)
        self.speed_boost = speed_boost
        self.texture = images.textures["speed"]

    def check_vertical_collision(self, other):
        collision_side = super().check_vertical_collision(other)
        if collision_side:
            other.speed = self.speed_boost
        else:
            other.speed = other.base_speed
        return collision_side
