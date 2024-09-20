from block import Block

class SpeedBoostBlock(Block):
    def __init__(self, height, width, x, y, color, speed_boost):
        super().__init__(height, width, x, y, color)
        self.speed_boost = speed_boost

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