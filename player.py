import pyray
from gameobject import GameObject

class Player(GameObject):
    def __init__(self, height, width, x, y, color, mass=50):
        super().__init__(height, width, x, y, color)
        self.vy = 0
        self.vx = 0
        self.gravity = 9.81
        self.speed = 400
        self.jump = 400
        self.mass = mass
        self.grounded = False
        self.ignore_controls = False
        self.ignore_controls_timer = 0
        self.apply_friction = True

    def movement(self, delta_time, blocks):
        self.grounded = False

        for block in blocks:
            vertical_collision = block.check_vertical_collision(self)
            horizontal_collision = block.check_horizontal_collision(self)

            if vertical_collision == "top":
                self.grounded = True
                if pyray.is_key_down(pyray.KeyboardKey.KEY_SPACE):
                    self.vy = -self.jump
                    self.grounded = False
            elif vertical_collision == "bottom":
                if self.vy < 0:
                    self.vy = -self.vy / 2

            if horizontal_collision == "left":
                if self.vx > 0:
                    self.vx = 0
                if pyray.is_key_down(pyray.KeyboardKey.KEY_SPACE):
                    self.vy = -self.jump
                    self.vx = -1*self.speed
                    self.grounded = False
                    self.ignore_controls = True
                    self.apply_friction = False
                    self.ignore_controls_timer = 0

            elif horizontal_collision == "right":
                if self.vx < 0:
                    self.vx = 0
                if pyray.is_key_down(pyray.KeyboardKey.KEY_SPACE):
                    self.vy = -self.jump
                    self.vx = 1*self.speed
                    self.grounded = False
                    self.ignore_controls = True
                    self.apply_friction = False
                    self.ignore_controls_timer = 0

        if not self.grounded:
            self.vy += self.gravity * delta_time * self.mass
        else:
            self.vy = 0

        if self.apply_friction:
            self.vx *= 0.9  # Apply friction

        self.y += self.vy * delta_time
        self.x += self.vx * delta_time

        if self.ignore_controls:
            self.ignore_controls_timer += delta_time
            if self.ignore_controls_timer >= 0.5:
                self.ignore_controls = False
                self.apply_friction = True

        if not self.ignore_controls:
            if pyray.is_key_down(pyray.KeyboardKey.KEY_D):
                self.vx += 0.1 * self.speed
            if pyray.is_key_down(pyray.KeyboardKey.KEY_A):
                self.vx += 0.1 * -self.speed