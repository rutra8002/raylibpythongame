import pyray
import images
import raylib
from gameobject import GameObject
from blocks.lavablock import LavaBlock
from inventory import Inventory
from gun import Gun, DesertEagle
from grapplinggun import GrapplingGun

class Enemy(GameObject):
    def __init__(self, height, width, x, y, color, health, inventory_data=None):
        super().__init__(height, width, x, y, color)
        self.texture = images.textures["enemy"]
        self.health = health
        self.vx = 0
        self.vy = 0
        self.gravity = 9.81
        self.base_speed = 200
        self.speed = 200
        self.base_jump = 400
        self.jump = 400
        self.mass = 50
        self.grounded = False
        self.time_since_last_damage = 0
        self.has_seen_player = False
        self.inventory = Inventory()
        if inventory_data:
            for item_data in inventory_data:
                if item_data['type'] == 'GrapplingGun':
                    self.inventory.add_item(GrapplingGun(item_data['range'], item_data['speed'], item_data['ammo']))
                elif item_data['type'] == 'Gun':
                    self.inventory.add_item(
                        Gun(item_data['damage'], item_data['range'], item_data['speed'], item_data['ammo'], None))
                elif item_data['type'] == 'DesertEagle':
                    self.inventory.add_item(DesertEagle(item_data['damage'], item_data['range'], item_data['speed'], item_data['ammo'], None))

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            return True  # Enemy is dead
        return False  # Enemy is still alive

    def movement(self, delta_time, blocks, player):
        if not self.has_seen_player:
            if self.can_see_player(player):
                self.has_seen_player = True
            else:
                return

        self.grounded = False
        self.handle_collisions(blocks, delta_time)
        self.move_towards_player(delta_time, blocks, player)
        self.apply_gravity_and_friction(delta_time)
        self.apply_movement(delta_time)

    def can_see_player(self, player):
        return abs(self.x - player.x) < 500 and abs(self.y - player.y) < 500

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

    def handle_top_collision(self, block):
        self.grounded = True

    def handle_bottom_collision(self):
        if self.vy < 0:
            self.vy = 0

    def handle_side_collision(self, block, horizontal_collision):
        if self.grounded:
            if self.y - (self.height) < block.y:
                self.x += 0.05 * -self.speed if horizontal_collision == "right" else 0.05 * self.speed
                self.y = block.y - self.height

        if horizontal_collision == "left" and self.vx > 0:
            self.vx = 0
        elif horizontal_collision == "right" and self.vx < 0:
            self.vx = 0

    def move_towards_player(self, delta_time, blocks, player):
        if self.grounded:
            if player.x < self.x:
                if not any(block.check_horizontal_collision(self) == "right" for block in blocks):
                    self.vx -= 10 * self.speed * delta_time
            elif player.x > self.x:
                if not any(block.check_horizontal_collision(self) == "left" for block in blocks):
                    self.vx += 10 * self.speed * delta_time
        elif not self.grounded:
            if player.x < self.x:
                if not any(block.check_horizontal_collision(self) == "right" for block in blocks):
                    self.vx -= 0.45 * self.speed * delta_time
            elif player.x > self.x:
                if not any(block.check_horizontal_collision(self) == "left" for block in blocks):
                    self.vx += 0.45 * self.speed * delta_time

    def apply_gravity_and_friction(self, delta_time):
        if not self.grounded:
            self.vy += self.gravity * delta_time * self.mass
            self.vx -= 0.01 * self.vx * delta_time
        else:
            self.vx -= 10 * self.vx * delta_time
            self.vy = 0

    def apply_movement(self, delta_time):
        self.y += self.vy * delta_time
        self.x += self.vx * delta_time

    def draw(self, player):
        for i in range(0, self.width, self.texture.width):
            for j in range(0, self.height, self.texture.height):
                raylib.DrawTexture(self.texture, int(self.x + i), int(self.y + j), raylib.WHITE)
        self.draw_health_bar()
        self.draw_inventory()

        if self.inventory.items:
            selected_item = max(self.inventory.items, key=lambda item: getattr(item, 'damage', 0))
            if hasattr(selected_item, 'draw'):
                target_x, target_y = player.x, player.y
                selected_item.draw(self.x + self.width // 2, self.y + self.height // 2, self.width // 1.5, self.height // 1.5, 0, self.vx, None, target_x, target_y)

    def draw_health_bar(self):
        bar_width = self.width
        bar_height = 10
        health_percentage = self.health / 100
        health_bar_width = bar_width * health_percentage
        pyray.draw_rectangle(int(self.x), int(self.y) - 20, bar_width, bar_height, pyray.RED)
        pyray.draw_rectangle(int(self.x), int(self.y) - 20, int(health_bar_width), bar_height, pyray.GREEN)

    def draw_inventory(self):
        inventory_text = "Inventory: " + ", ".join([item.__class__.__name__ for item in self.inventory.items])
        pyray.draw_text(inventory_text, int(self.x), int(self.y) - 40, 10, pyray.WHITE)