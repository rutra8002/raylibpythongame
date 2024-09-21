import pyray
from gameobject import GameObject
from jumpboostblock import JumpBoostBlock
from grapplinggun import GrapplingGun

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
        self.sliding = False
        self.can_jump = True
        self.grappling_gun = GrapplingGun(range=500, speed=300)

    def movement(self, delta_time, blocks, camera):
        self.grounded = False

        for block in blocks:
            vertical_collision = block.check_vertical_collision(self)
            horizontal_collision = block.check_horizontal_collision(self)

            if vertical_collision == "top":
                if isinstance(block, JumpBoostBlock):
                    self.grounded = False
                else:
                    self.grounded = True
                    self.can_jump = True
                    if pyray.is_key_down(pyray.KeyboardKey.KEY_SPACE) and self.can_jump:
                        self.vy = -self.jump
                        self.can_jump = False
                        self.grounded = False
            elif vertical_collision == "bottom":
                if self.vy < 0:
                    self.vy += -2 * self.vy

            if horizontal_collision == "left" or horizontal_collision == "right":
                self.can_jump = True
                if pyray.is_key_down(pyray.KeyboardKey.KEY_SPACE) and self.can_jump:
                    self.vy = -self.jump
                    self.can_jump = False
                    if abs(self.vx) > self.speed:
                        self.vx = -self.vx
                    else:
                        self.vx = -self.speed if horizontal_collision == "left" else self.speed
                    self.grounded = False

            if horizontal_collision == "left" and self.vx > 0:
                self.vx = 0
            elif horizontal_collision == "right" and self.vx < 0:
                self.vx = 0

        if not self.grounded:
            self.vy += self.gravity * delta_time * self.mass
            if pyray.is_key_down(pyray.KeyboardKey.KEY_D):
                if not any(block.check_horizontal_collision(self) == "left" for block in blocks):
                    self.vx += 0.00025 * self.speed
            if pyray.is_key_down(pyray.KeyboardKey.KEY_A):
                if not any(block.check_horizontal_collision(self) == "right" for block in blocks):
                    self.vx += 0.00025 * -self.speed
            self.vx *= 0.99977
        else:
            if pyray.is_key_down(pyray.KeyboardKey.KEY_LEFT_CONTROL):
                self.sliding = True
                self.vx *= 0.9999
            else:
                self.sliding = False
                self.vx *= 0.9
            if not self.sliding:
                if pyray.is_key_down(pyray.KeyboardKey.KEY_D):
                    if not any(block.check_horizontal_collision(self) == "left" for block in blocks):
                        self.vx += 0.1 * self.speed
                if pyray.is_key_down(pyray.KeyboardKey.KEY_A):
                    if not any(block.check_horizontal_collision(self) == "right" for block in blocks):
                        self.vx += 0.1 * -self.speed
            self.vy = 0

        # Grappling gun logic
        if pyray.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT):
            mouse_position = pyray.get_mouse_position()
            world_position = pyray.get_screen_to_world_2d(mouse_position, camera.camera)
            mouse_x, mouse_y = world_position.x, world_position.y
            self.grappling_gun.shoot(mouse_x, mouse_y, blocks)

        if self.grappling_gun.target_x is not None and self.grappling_gun.target_y is not None:
            self.x, self.y, reached_target, new_vx, new_vy = self.grappling_gun.update_position(self.x, self.y, delta_time)
            if reached_target:
                self.grappling_gun.reset()
            else:
                self.vx = new_vx
                self.vy = new_vy

        # Apply friction
        self.y += self.vy * delta_time
        self.x += self.vx * delta_time

    def draw(self):
        super().draw()
        self.grappling_gun.draw(self.x, self.y)