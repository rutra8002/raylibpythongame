from block import Block
import images
import pyray

class SpeedBoostBlock(Block):
    def __init__(self, height, width, x, y, color, speed_boost):
        super().__init__(height, width, x, y, color)
        self.speed_boost = speed_boost
        self.texture = images.load_texture_with_error_check(b"images/speeed.png")


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