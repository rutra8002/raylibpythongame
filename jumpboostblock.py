import pyray
import images

from block import Block

class JumpBoostBlock(Block):
    def __init__(self, height, width, x, y, color, jump_boost):
        super().__init__(height, width, x, y, color)
        self.jump_boost = jump_boost
        self.texture = images.load_texture_with_error_check("images/jump.png")

    def check_vertical_collision(self, other):
        collision_side = super().check_vertical_collision(other)
        if collision_side == "top":
            other.grounded = False
            other.vy = -self.jump_boost
        return collision_side

    def draw(self):
        for i in range(0, self.width, self.texture.width):
            for j in range(0, self.height, self.texture.height):
                pyray.draw_texture(self.texture, int(self.x + i), int(self.y + j), pyray.WHITE)