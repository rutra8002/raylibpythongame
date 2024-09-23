from block import Block

import pyray

class SpeedBoostBlock(Block):
    def __init__(self, height, width, x, y, color, speed_boost):
        super().__init__(height, width, x, y, color)
        self.speed_boost = speed_boost
        self.texture = pyray.load_texture("images/speeed.png")
        if self.texture.id == 0:
            raise ValueError("Failed to load texture")


    def check_vertical_collision(self, other):
        collision_side = super().check_vertical_collision(other)
        if collision_side:
            if self.speed_boost > other.vx > 0:
                other.vx += self.speed_boost
            elif -self.speed_boost < other.vx < 0:
                other.vx -= self.speed_boost
            else:
                pass
        return collision_side

    def draw(self):
        for i in range(0, self.width, self.texture.width):
            for j in range(0, self.height, self.texture.height):
                pyray.draw_texture(self.texture, int(self.x + i), int(self.y + j), pyray.WHITE)