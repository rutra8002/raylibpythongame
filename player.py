# player.py

import pyray
import math
from gameobject import GameObject
from blocks.jumpboostblock import JumpBoostBlock
from grapplinggun import GrapplingGun
from gun import *
from inventory import Inventory
import images
from blocks.lavablock import LavaBlock

class Player(GameObject):
    def __init__(self, height, width, x, y, color, particle_system, inventory_data=None, mass=50):
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
        self.texture = images.load_texture_with_error_check(b"images/player.png")
        self.inventory = Inventory()
        if inventory_data:
            for item_data in inventory_data:
                if item_data['type'] == 'GrapplingGun':
                    self.inventory.add_item(GrapplingGun(item_data['range'], item_data['speed'], item_data['ammo']))
                elif item_data['type'] == 'Gun':
                    self.inventory.add_item(
                        Gun(item_data['damage'], item_data['range'], item_data['speed'], item_data['ammo'], particle_system))
                elif item_data['type'] == 'DesertEagle':
                    self.inventory.add_item(DesertEagle(item_data['damage'], item_data['range'], item_data['speed'], item_data['ammo'], particle_system))
        else:
            self.inventory.add_item(Gun(10, 300, 0, 0, particle_system))
        self.health = 100
        self.particle_system = particle_system
        self.time_since_last_damage = 0

    def movement(self, delta_time, blocks, camera):
        self.grounded = False
        self.handle_item_switching()
        selected_item = self.inventory.get_selected_item()
        self.handle_item_usage(selected_item, camera, blocks, delta_time)
        self.handle_collisions(blocks, delta_time)
        self.apply_gravity_and_friction(delta_time, blocks)
        self.apply_movement(delta_time)

        self.is_inside_lava(blocks)

    def handle_item_switching(self):
        if pyray.is_key_pressed(pyray.KeyboardKey.KEY_E):
            self.inventory.select_next_item()
        if pyray.is_key_pressed(pyray.KeyboardKey.KEY_Q):
            self.inventory.select_previous_item()

    def handle_item_usage(self, selected_item, camera, blocks, delta_time):
        if isinstance(selected_item, GrapplingGun):
            self.handle_grappling_gun(selected_item, camera, blocks, delta_time)
        elif isinstance(selected_item, Gun):
            self.handle_gun(selected_item, camera)

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

    def handle_gun(self, selected_item, camera):
        if pyray.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT):
            selected_item.shoot(self.x, self.y, self.width, self.height, camera)


    def is_inside_lava(self, blocks):
        for block in blocks:
            if isinstance(block, LavaBlock):
                if (self.x + self.width > block.x and self.x < block.x + block.width and
                        self.y + self.height > block.y and self.y < block.y + block.height):
                    if self.time_since_last_damage >= 0.1:
                        self.take_damage(10)
                        self.time_since_last_damage = 0
                    return True
        return False

    def handle_collisions(self, blocks, delta_time):
        self.time_since_last_damage += delta_time
        for block in blocks:
            vertical_collision = block.check_vertical_collision(self)
            horizontal_collision = block.check_horizontal_collision(self)

            if vertical_collision == "top":
                self.handle_top_collision(block)
            elif vertical_collision == "bottom":
                self.handle_bottom_collision()

            if horizontal_collision == "left" or horizontal_collision == "right":
                self.handle_side_collision(block, horizontal_collision)


    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

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
        print(horizontal_collision)
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
            if self.y - (self.height) < block.y:
                self.x += 0.05 * -self.speed if horizontal_collision == "right" else 0.05 * self.speed
                self.y = block.y - self.height

        if horizontal_collision == "left" and self.vx > 0:
            self.vx = 0
        elif horizontal_collision == "right" and self.vx < 0:
            self.vx = 0

    def apply_gravity_and_friction(self, delta_time, blocks):
        if not self.grounded:
            self.sliding = False
            if self.is_inside_lava(blocks):
                self.vy -= 0.05 * self.vy
                self.vx -= 0.05 * self.vx
            else:
                self.vy += self.gravity * delta_time * self.mass
            if pyray.is_key_down(pyray.KeyboardKey.KEY_D):
                if not any(block.check_horizontal_collision(self) == "left" for block in blocks):
                    self.vx += 0.00045 * self.speed
            if pyray.is_key_down(pyray.KeyboardKey.KEY_A):
                if not any(block.check_horizontal_collision(self) == "right" for block in blocks):
                    self.vx += 0.00045 * -self.speed
            self.vx -= 0.0001 * self.vx
        else:
            if pyray.is_key_down(pyray.KeyboardKey.KEY_LEFT_CONTROL):
                self.sliding = True
                self.vx -= 0.0001 * self.vx
            else:
                self.sliding = False
                self.vx -= 0.1 * self.vx
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