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
        self.speed = 250
        self.jump = 400
        self.mass = mass

    def draw(self):
        pyray.draw_rectangle(int(self.x), int(self.y), self.width, self.height, self.color)

    def movement(self, delta_time, blocks):
        for block in blocks:
            if block.check_vertical_collision(self) == "top":
                if pyray.is_key_down(pyray.KeyboardKey.KEY_SPACE):
                    self.vy = -self.jump
                else:
                    if self.vy > 0:
                        self.vy = 0
            elif block.check_vertical_collision(self) == "bottom":
                if self.vy < 0:
                    self.vy = -self.vy /2
            if block.check_horizontal_collision(self) == "left":
                if self.vx > 0:
                    self.vx = 0
            elif block.check_horizontal_collision(self) == "right":
                if self.vx < 0:
                    self.vx = 0



        self.vy += self.gravity * delta_time * self.mass
        self.vx = self.vx * 0.9
        self.y += self.vy * delta_time
        self.x += self.vx * delta_time

        if pyray.is_key_down(pyray.KeyboardKey.KEY_D):
            self.vx += 0.1*self.speed
        if pyray.is_key_down(pyray.KeyboardKey.KEY_A):
            self.vx += 0.1*-self.speed




