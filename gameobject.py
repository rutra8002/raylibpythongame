import pyray

class GameObject:
    def __init__(self, height, width, x, y, color):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        pyray.draw_rectangle(int(self.x), int(self.y), self.width, self.height, self.color)

    def check_vertical_collision(self, other):
        touching_top = other.y + other.height > self.y and other.y < self.y
        touching_bottom = other.y <= self.y + self.height and other.y + other.height > self.y + self.height
        within_horizontal_bounds = other.x + other.width - 1 > self.x and other.x < self.x + self.width - 1
        if touching_top and within_horizontal_bounds:
            return "top"
        if touching_bottom and within_horizontal_bounds:
            return "bottom"

    def check_horizontal_collision(self, other):
        touching_left = other.x + other.width > self.x and other.x < self.x
        touching_right = other.x < self.x + self.width and other.x + other.width > self.x + self.width
        within_vertical_bounds = other.y + other.height - 1 > self.y and other.y < self.y + self.height - 1
        if touching_left and within_vertical_bounds:
            return "left"
        if touching_right and within_vertical_bounds:
            return "right"