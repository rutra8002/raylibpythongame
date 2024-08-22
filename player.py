import pyray

class Player:
    def __init__(self, height, width, x, y, color, mass=50):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.color = color
        self.vy = 0
        self.vx = 0
        self.gravity = 9.81
        self.speed = 200
        self.jump = 400
        self.mass = mass

    def draw(self):
        pyray.draw_rectangle(int(self.x), int(self.y), self.width, self.height, self.color)

    def check_vertical_collision(self, block):
        touching_top = self.y + self.height > block.y and self.y < block.y
        touching_bottom = self.y <= block.y + block.height and self.y + self.height > block.y + block.height
        within_horizontal_bounds = self.x + self.width -1 > block.x and self.x < block.x + block.width -1
        if touching_top and within_horizontal_bounds:
            return "top"
        if touching_bottom and within_horizontal_bounds:
            return "bottom"

    def check_horizontal_collision(self, block):
        touching_left = self.x + self.width > block.x and self.x < block.x
        touching_right = self.x < block.x + block.width and self.x + self.width > block.x + block.width
        within_vertical_bounds = self.y + self.height -1 > block.y and self.y < block.y + block.height -1
        if touching_left and within_vertical_bounds:
            return "left"
        if touching_right and within_vertical_bounds:
            return "right"

    def movement(self, delta_time, blocks):
        for block in blocks:
            print(self.check_horizontal_collision(block), self.check_vertical_collision(block))

            if self.check_vertical_collision(block) == "top":
                if pyray.is_key_down(pyray.KeyboardKey.KEY_SPACE):
                    self.vy = -self.jump
                else:
                    if self.vy > 0:
                        self.vy = 0
            elif self.check_vertical_collision(block) == "bottom":
                if self.vy < 0:
                    self.vy = 0
            if self.check_horizontal_collision(block) == "left":
                if self.vx > 0:
                    self.vx = 0
            elif self.check_horizontal_collision(block) == "right":
                if self.vx < 0:
                    self.vx = 0



        self.vy += self.gravity * delta_time * self.mass
        self.vx = self.vx * 0.9
        self.y += self.vy * delta_time
        self.x += self.vx * delta_time

        if pyray.is_key_down(pyray.KeyboardKey.KEY_D):
            self.vx = self.speed
        if pyray.is_key_down(pyray.KeyboardKey.KEY_A):
            self.vx = -self.speed




