from blocks.block import Block
import images

class JumpBoostBlock(Block):
    def __init__(self, height, width, x, y, color, jump_boost):
        super().__init__(height, width, x, y, color)
        self.jump_boost = jump_boost
        self.texture = images.textures["jump"]


    def check_vertical_collision(self, other):
        collision_side = super().check_vertical_collision(other)
        if collision_side:
            other.jump = self.jump_boost
        else:
            other.jump = other.base_jump
        return collision_side
