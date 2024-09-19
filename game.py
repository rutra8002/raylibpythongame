import os
import random
import pyray
from player import Player
from block import Block
from camera import Camera
from particles import ParticleSystem

class Game:
    def __init__(self, width=1366, height=768):
        self.width = width
        self.height = height
        self.player = Player(50, 50, 100, 100, pyray.RED, 70)
        self.blocks = [Block(50, 500, 100, 600, pyray.BLUE),
                       Block(50, 500, 800, 600, pyray.BLUE),
                       Block(50, 50000, 1500, 600, pyray.BLUE),
                       Block(50, 100, 650, 500, pyray.BLUE),
                       Block(500, 50, 500, 0, pyray.BLUE),
                       Block(500, 200, 850, 0, pyray.BLUE),
                       Block(500, 50, 500, 900, pyray.BLUE),
                       Block(50, 550, 500, 1400, pyray.BLUE),
                       Block(500, 50, 1000, 900, pyray.BLUE),]
        self.camera = Camera(width, height, self.player.x + self.player.width / 2, self.player.y + self.player.height / 2, 3)
        self.particle_system = ParticleSystem()
        self.particle_update_timer = 0

    def run(self):
        pyray.init_window(self.width, self.height, "game")
        # pyray.set_target_fps(60)
        while not pyray.window_should_close():
            delta_time = pyray.get_frame_time()
            self.update(delta_time)
            self.render()

        pyray.close_window()

    def update(self, delta_time):
        self.camera.update_target(self.player.x + self.player.width / 2, self.player.y + self.player.height / 2, delta_time)
        self.player.movement(delta_time, self.blocks)

        # Update the timer
        self.particle_update_timer += delta_time

        # Add particles behind the player when moving, but only update once each second
        if self.particle_update_timer >= 0.01:
            if round(self.player.vx, 10) != 0 or self.player.vy != 0:
                self.particle_system.add_particle(
                    self.player.x + random.randint(0, self.player.width),  # x position
                    self.player.y + random.randint(0, self.player.height),  # y position (behind the player)
                    random.uniform(-1, 1),  # vx
                    random.uniform(-1, 1),  # vy
                    50,  # speed
                    1,  # lifespan
                    5,  # size
                    (255, 0, 0, 100),  # color (red)
                    'circle'  # shape
                )
            self.particle_update_timer = 0  # Reset the timer

        self.particle_system.update(delta_time)
        self.particle_system.apply_force_to_all(0, 9.81*delta_time)

    def render(self):
        pyray.begin_drawing()
        pyray.clear_background(pyray.WHITE)
        self.camera.begin_mode()
        self.player.draw()
        for block in self.blocks:
            block.draw()
        self.particle_system.draw()
        self.camera.end_mode()
        pyray.draw_fps(10, 10)
        for parameter in self.player.__dict__:
            pyray.draw_text(parameter + ": " + str(self.player.__dict__[parameter]), 10,
                            30 + 10 * list(self.player.__dict__.keys()).index(parameter), 10, pyray.BLACK)
        for i, block in enumerate(self.blocks):
            pyray.draw_text("Block " + str(i), 200 * i + 200, 20, 10, pyray.BLACK)
            for parameter in block.__dict__:
                pyray.draw_text(parameter + ": " + str(block.__dict__[parameter]), 200 * i + 200,
                                30 + 10 * list(block.__dict__.keys()).index(parameter), 10, pyray.BLACK)
        pyray.end_drawing()