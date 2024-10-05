import pyray
import math
from gameobject import GameObject
from jumpboostblock import JumpBoostBlock
from grapplinggun import GrapplingGun
from gun import Gun
from inventory import Inventory
import images

class Player(GameObject):
    def __init__(self, height, width, x, y, color, particle_system, mass=50):
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
        self.texture = images.load_texture_with_error_check("images/player.png")
        self.inventory = Inventory()
        self.inventory.add_item(GrapplingGun(500, 100, 10))
        self.inventory.add_item(Gun("Desert Eagle", 10, 300, 15))
        self.health = 100
        self.particle_system = particle_system

    def movement(self, delta_time, blocks, camera):
        self.grounded = False
        self.handle_item_switching()
        selected_item = self.inventory.get_selected_item()
        self.handle_item_usage(selected_item, camera, blocks, delta_time)
        self.handle_collisions(blocks)
        self.apply_gravity_and_friction(delta_time, blocks)
        self.apply_movement(delta_time)

    def handle_item_switching(self):
        if pyray.is_key_pressed(pyray.KeyboardKey.KEY_E):
            self.inventory.select_next_item()
        if pyray.is_key_pressed(pyray.KeyboardKey.KEY_Q):
            self.inventory.select_previous_item()

    def handle_item_usage(self, selected_item, camera, blocks, delta_time):
        if isinstance(selected_item, GrapplingGun):
            self.handle_grappling_gun(selected_item, camera, blocks, delta_time)
        elif isinstance(selected_item, Gun):
            self.handle_gun(selected_item)

    def handle_grappling_gun(self, selected_item, camera, blocks, delta_time):
        if pyray.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT):
            mouse_position = pyray.get_mouse_position()
            world_position = pyray.get_screen_to_world_2d(mouse_position, camera.camera)
            mouse_x, mouse_y = world_position.x, world_position.y
            selected_item.shoot(mouse_x, mouse_y, blocks)

        if selected_item.target_x is not None and selected_item.target_y is not None:
            self.vx, self.vy, reached_target = selected_item.update_position(self.x, self.y, self.vx, self.vy, delta_time)
            if reached_target:
                selected_item.reset()

    def handle_gun(self, selected_item):
        if pyray.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT):
            if selected_item.shoot():
                # Get the position to shoot the particle from
                particle_x = self.x + self.width // 2
                particle_y = self.y + self.height // 2
                # Add a particle to the particle system
                self.particle_system.add_particle(
                    particle_x, particle_y, 1, 0, 500, 1, 5, (255, 255, 0, 255), 'circle'
                )

    def handle_collisions(self, blocks):
        for block in blocks:
            vertical_collision = block.check_vertical_collision(self)
            horizontal_collision = block.check_horizontal_collision(self)

            if vertical_collision == "top":
                self.handle_top_collision(block)
            elif vertical_collision == "bottom":
                self.handle_bottom_collision()

            if horizontal_collision == "left" or horizontal_collision == "right":
                self.handle_side_collision(block, horizontal_collision)

    def handle_top_collision(self, block):
        if isinstance(block, JumpBoostBlock):
            self.grounded = False
        else:
            self.grounded = True
            self.can_jump = True
            if pyray.is_key_down(pyray.KeyboardKey.KEY_SPACE) and self.can_jump:
                self.vy = -self.jump
                self.can_jump = False
                self.grounded = False

    def handle_bottom_collision(self):
        if self.vy < 0:
            self.vy += -2 * self.vy

    def handle_side_collision(self, block, horizontal_collision):
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
            if self.y - (self.height // 4) < block.y:
                self.x += 0.05 * self.speed if horizontal_collision == "left" else -0.05 * self.speed
                self.y = block.y - self.height

        if horizontal_collision == "left" and self.vx > 0:
            self.vx = 0
        elif horizontal_collision == "right" and self.vx < 0:
            self.vx = 0

    def apply_gravity_and_friction(self, delta_time, blocks):
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

    def apply_movement(self, delta_time):
        self.y += self.vy * delta_time
        self.x += self.vx * delta_time

    def draw(self, camera):
        if camera != None:
            angle = 0
            draw_x = self.x
            source_rect = pyray.Rectangle(0, 0, self.texture.width, self.texture.height)
            dest_rect = pyray.Rectangle(draw_x, self.y, self.width, self.height)

            if self.vx < 0:
                source_rect.width = -self.texture.width

            pyray.draw_texture_pro(self.texture, source_rect, dest_rect, pyray.Vector2(0, 0), angle, pyray.WHITE)

            selected_item = self.inventory.get_selected_item()
            if selected_item and hasattr(selected_item, 'draw'):
                selected_item.draw(draw_x + self.width // 2, self.y + self.height // 2, self.width//1.5, self.height//1.5, angle,
                                   self.vx, camera)

            self.draw_health_bar()
        else:
            pyray.draw_rectangle(int(self.x), int(self.y), self.width, self.height, self.color)
            self.draw_health_bar()

    def draw_health_bar(self):
        bar_width = self.width
        bar_height = 10
        health_percentage = self.health / 100
        health_bar_width = bar_width * health_percentage
        pyray.draw_rectangle(int(self.x), int(self.y) - 20, bar_width, bar_height, pyray.RED)
        pyray.draw_rectangle(int(self.x), int(self.y) - 20, int(health_bar_width), bar_height, pyray.GREEN)
