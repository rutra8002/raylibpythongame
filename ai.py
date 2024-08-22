import pyray

class AI:
    def __init__(self, height, width, x, y, color, speed=200):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.color = color
        self.vx = 0
        self.vy = 0
        self.speed = speed

    def draw(self):
        pyray.draw_rectangle(int(self.x), int(self.y), self.width, self.height, self.color)

    def update(self, delta_time, player, blocks):
        # Calculate direction to player
        direction_x = player.x - self.x
        direction_y = player.y - self.y
        distance = (direction_x**2 + direction_y**2)**0.5

        if distance > 0:
            direction_x /= distance
            direction_y /= distance

        self.vx = direction_x * self.speed
        self.vy = direction_y * self.speed

        # Check for collisions with blocks
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

        # Update position
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time

    def check_vertical_collision(self, player):
        touching_top = self.y + self.height > player.y and self.y < player.y
        touching_bottom = self.y <= player.y + player.height and self.y + self.height > player.y + player.height
        within_horizontal_bounds = self.x + self.width - 1 > player.x and self.x < player.x + player.width - 1
        if touching_top and within_horizontal_bounds:
            return "top"
        if touching_bottom and within_horizontal_bounds:
            return "bottom"

    def check_horizontal_collision(self, player):
        touching_left = self.x + self.width > player.x and self.x < player.x
        touching_right = self.x < player.x + player.width and self.x + self.width > player.x + player.width
        within_vertical_bounds = self.y + self.height - 1 > player.y and self.y < player.y + player.height - 1
        if touching_left and within_vertical_bounds:
            return "left"
        if touching_right and within_vertical_bounds:
            return "right"