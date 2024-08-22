import pyray

class Block:
    def __init__(self, height, width, x, y, color):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        pyray.draw_rectangle(int(self.x), int(self.y), self.width, self.height, self.color)

    def check_vertical_collision(self, player):
        touching_top = player.y + player.height > self.y and player.y < self.y
        touching_bottom = player.y <= self.y + self.height and player.y + player.height > self.y + self.height
        within_horizontal_bounds = player.x + player.width - 1 > self.x and player.x < self.x + self.width - 1
        if touching_top and within_horizontal_bounds:
            return "top"
        if touching_bottom and within_horizontal_bounds:
            return "bottom"

    def check_horizontal_collision(self, player):
        touching_left = player.x + player.width > self.x and player.x < self.x
        touching_right = player.x < self.x + self.width and player.x + player.width > self.x + self.width
        within_vertical_bounds = player.y + player.height - 1 > self.y and player.y < self.y + self.height - 1
        if touching_left and within_vertical_bounds:
            return "left"
        if touching_right and within_vertical_bounds:
            return "right"