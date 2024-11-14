import pyray
import images
import raylib
from gameobject import GameObject
from blocks.jumpboostblock import JumpBoostBlock
from blocks.lavablock import LavaBlock

class Enemy(GameObject):
    def __init__(self, height, width, x, y, color, health):
        super().__init__(height, width, x, y, color)
        self.texture = images.load_texture_with_error_check(b"images/enemy.png")
        self.health = health
        self.vx = 0
        self.vy = 0
        self.gravity = 9.81
        self.speed = 200
        self.jump = 300
        self.mass = 50
        self.grounded = False
        self.time_since_last_damage = 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            return True  # Enemy is dead
        return False  # Enemy is still alive

    def movement(self, delta_time, blocks, player):
        self.grounded = False
        self.handle_collisions(blocks, delta_time)
        self.move_towards_player(blocks, player)
        self.apply_gravity_and_friction(delta_time)
        self.apply_movement(delta_time)

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
        if isinstance(block, JumpBoostBlock):
            self.grounded = False
        else:
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

    def move_towards_player(self, blocks, player):
        if self.grounded:
            if player.x < self.x:
                if not any(block.check_horizontal_collision(self) == "right" for block in blocks):
                    self.vx -= 0.1 * self.speed
            elif player.x > self.x:
                if not any(block.check_horizontal_collision(self) == "left" for block in blocks):
                    self.vx += 0.1 * self.speed
        elif not self.grounded:
            if player.x < self.x:
                if not any(block.check_horizontal_collision(self) == "right" for block in blocks):
                    self.vx -= 0.00025 * self.speed
            elif player.x > self.x:
                if not any(block.check_horizontal_collision(self) == "left" for block in blocks):
                    self.vx += 0.00025 * self.speed

    def apply_gravity_and_friction(self, delta_time):
        if not self.grounded:
            self.vy += self.gravity * delta_time * self.mass
            self.vx *= 0.99977
        else:
            self.vx *= 0.9
            self.vy = 0

    def apply_movement(self, delta_time):
        self.y += self.vy * delta_time
        self.x += self.vx * delta_time

    def draw(self):
        for i in range(0, self.width, self.texture.width):
            for j in range(0, self.height, self.texture.height):
                raylib.DrawTexture(self.texture, int(self.x + i), int(self.y + j), raylib.WHITE)
        self.draw_health_bar()

    def draw_health_bar(self):
        bar_width = self.width
        bar_height = 10
        health_percentage = self.health / 100
        health_bar_width = bar_width * health_percentage
        pyray.draw_rectangle(int(self.x), int(self.y) - 20, bar_width, bar_height, pyray.RED)
        pyray.draw_rectangle(int(self.x), int(self.y) - 20, int(health_bar_width), bar_height, pyray.GREEN)