import pyray
from gameobject import GameObject

class Player(GameObject):
    def __init__(self, height, width, x, y, color, mass=50):
        super().__init__(height, width, x, y, color)
        self.vy = 0
        self.vx = 0
        self.gravity = 9.81
        self.speed = 250
        self.jump = 400
        self.mass = mass
        self.grounded = False

    def movement(self, delta_time, blocks):
        self.grounded = False
        tolerance = 0.1

        for block in blocks:
            vertical_collision = block.check_vertical_collision(self)
            horizontal_collision = block.check_horizontal_collision(self)

            if vertical_collision == "top":
                self.grounded = True
                self.y = block.y - self.height + tolerance  #tolerance
                self.vy = 0
                if pyray.is_key_down(pyray.KeyboardKey.KEY_SPACE):
                    self.vy = -self.jump
                    self.grounded = False
            elif vertical_collision == "bottom":
                self.y = block.y + block.height  #notolerance
                self.vy = -self.vy / 2

            if horizontal_collision == "left":
                self.x = block.x - self.width  #notolerance
                self.vx = 0
            elif horizontal_collision == "right":
                self.x = block.x + block.width #notolerance
                self.vx = 0

        if not self.grounded:
            self.vy += self.gravity * delta_time * self.mass
        else:
            self.vy = 0

        self.vx *= 0.9  # Apply friction
        self.y += self.vy * delta_time
        self.x += self.vx * delta_time

        if pyray.is_key_down(pyray.KeyboardKey.KEY_D):
            self.vx += 0.1 * self.speed
        if pyray.is_key_down(pyray.KeyboardKey.KEY_A):
            self.vx += 0.1 * -self.speed