import pyray
from gameobject import GameObject

class AI(GameObject):
    def __init__(self, height, width, x, y, color, speed=200):
        super().__init__(height, width, x, y, color)
        self.vx = 0
        self.vy = 0
        self.speed = speed

    def update(self, delta_time, player, blocks):
        direction_x = player.x - self.x
        direction_y = player.y - self.y
        distance = (direction_x**2 + direction_y**2)**0.5

        if distance > 0:
            direction_x /= distance
            direction_y /= distance

        self.vx = direction_x * self.speed
        self.vy = direction_y * self.speed

        for block in blocks:
            if block.check_vertical_collision(self) == "top" and self.vy > 0:
                self.vy = 0
            elif block.check_vertical_collision(self) == "bottom" and self.vy < 0:
                self.vy = 0
            if block.check_horizontal_collision(self) == "left" and self.vx > 0:
                self.vx = 0
            elif block.check_horizontal_collision(self) == "right" and self.vx < 0:
                self.vx = 0

        if self.check_vertical_collision(player) == "top" and self.vy > 0:
            self.vy = 0
        elif self.check_vertical_collision(player) == "bottom" and self.vy < 0:
            self.vy = 0
        if self.check_horizontal_collision(player) == "left" and self.vx > 0:
            self.vx = 0
        elif self.check_horizontal_collision(player) == "right" and self.vx < 0:
            self.vx = 0

        self.x += self.vx * delta_time
        self.y += self.vy * delta_time