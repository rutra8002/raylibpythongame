import os
import pyray
from blocks.block import Block

class JumpBoostBlock(Block):
    def __init__(self, height, width, x, y, color, jump_boost):
        super().__init__(height, width, x, y, color)
        self.jump_boost = jump_boost
        texture_path = os.path.join(os.path.dirname(__file__), '../images/jump.png')
        print(f"Loading texture from: {texture_path}")  # Debug logging
        self.texture = pyray.load_texture(texture_path.encode('utf-8'))
        if self.texture.id == 0:
            raise ValueError("Failed to load texture")

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