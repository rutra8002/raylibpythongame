from block import Block

class JumpBoostBlock(Block):
    def __init__(self, height, width, x, y, color, jump_boost):
        super().__init__(height, width, x, y, color)
        self.jump_boost = jump_boost

    def check_vertical_collision(self, other):
        collision_side = super().check_vertical_collision(other)
        if collision_side == "top":
            other.grounded = False
            other.vy = -self.jump_boost
        return collision_side