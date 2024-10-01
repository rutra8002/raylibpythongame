import pyray
from gameobject import GameObject
from jumpboostblock import JumpBoostBlock
from grapplinggun import GrapplingGun
from gun import Gun
from inventory import Inventory
from hotbar import Hotbar
import math
import images


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
        self.grappling_gun = GrapplingGun(range=500, speed=200)
        self.texture = images.load_texture_with_error_check("images/player.png")
        self.inventory = Inventory()
        self.inventory.add_item(self.grappling_gun)
        self.inventory.add_item(Gun("Pistol", 10, 300, 15))
        self.hotbar = Hotbar(self.inventory.items)

    def movement(self, delta_time, blocks, camera):
        self.grounded = False

        # Switch items
        if pyray.is_key_pressed(pyray.KeyboardKey.KEY_E):
            self.inventory.select_next_item()
            self.hotbar.selected_index = self.inventory.selected_index
        if pyray.is_key_pressed(pyray.KeyboardKey.KEY_Q):
            self.inventory.select_previous_item()
            self.hotbar.selected_index = self.inventory.selected_index

        selected_item = self.inventory.get_selected_item()


        if isinstance(selected_item, GrapplingGun):
            if pyray.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT):
                mouse_position = pyray.get_mouse_position()
                world_position = pyray.get_screen_to_world_2d(mouse_position, camera.camera)
                mouse_x, mouse_y = world_position.x, world_position.y
                selected_item.shoot(mouse_x, mouse_y, blocks)

            if selected_item.target_x is not None and selected_item.target_y is not None:
                self.vx, self.vy, reached_target = selected_item.update_position(self.x, self.y, self.vx, self.vy, delta_time)
                if reached_target:
                    selected_item.reset()

        # Gun logic
        elif isinstance(selected_item, Gun):
            if pyray.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT):
                if selected_item.shoot():
                    # Implement shooting logic here
                    pass

        # Existing movement and collision logic
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
                if not self.grappling_gun.is_grappling:
                    if self.vy < 0:
                        self.vy += -2 * self.vy
                else:
                    if self.vy < 0:
                        self.vy = 0

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

                if self.grounded:
                    if self.y - (self.height//4)< block.y:
                        self.x += 0.05 * self.speed if horizontal_collision == "left" else -0.05 * self.speed
                        self.y = block.y - self.height

            if horizontal_collision == "left" and self.vx > 0:
                self.vx = 0
            elif horizontal_collision == "right" and self.vx < 0:
                self.vx = 0

        if not self.grounded:
            self.sliding = False
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

        # Apply friction
        self.y += self.vy * delta_time
        self.x += self.vx * delta_time

    def draw(self):
        angle = 0
        draw_x = self.x
        source_rect = pyray.Rectangle(0, 0, self.texture.width, self.texture.height)
        dest_rect = pyray.Rectangle(draw_x, self.y, self.width, self.height)

        if self.vx < 0:
            source_rect.width = -self.texture.width

        pyray.draw_texture_pro(self.texture, source_rect, dest_rect, pyray.Vector2(0, 0), angle, pyray.WHITE)
        self.grappling_gun.draw(self.x, self.y, self.width, self.height)