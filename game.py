import os
import random
import pyray
from player import Player
from block import Block
from camera import Camera
from particles import ParticleSystem
from speedboostblock import SpeedBoostBlock
from jumpboostblock import JumpBoostBlock
from main_menu import MainMenu

class Game:
    def __init__(self, width=1366, height=768):
        self.width = width
        self.height = height
        self.player = Player(50, 50, 100, 100, pyray.RED, 70)
        self.blocks = [
            Block(50, 500, 100, 600, pyray.BLUE),
            Block(50, 450, 800, 600, pyray.BLUE),
            Block(50, 50000, 1500, 600, pyray.BLUE),
            Block(50, 100, 650, 500, pyray.BLUE),
            Block(500, 50, 500, 0, pyray.BLUE),
            Block(500, 200, 850, 0, pyray.BLUE),
            Block(500, 50, 500, 900, pyray.BLUE),
            Block(50, 550, 500, 1400, pyray.BLUE),
            Block(500, 50, 1000, 900, pyray.BLUE),
            SpeedBoostBlock(50, 50, 1200, 550, pyray.GREEN, 800),
            JumpBoostBlock(50, 50, 1300, 600, pyray.YELLOW, 800),
            #stairs
            Block(50, 100, 1200, 350, pyray.BLUE),
            Block(50, 100, 1250, 300, pyray.BLUE),
            Block(50, 100, 1300, 250, pyray.BLUE),
            Block(50, 100, 1350, 200, pyray.BLUE),
            Block(50, 100, 1400, 150, pyray.BLUE),
            Block(50, 100, 1450, 100, pyray.BLUE),
            Block(50, 100, 1500, 50, pyray.BLUE),
        ]
        self.camera = Camera(width, height, self.player.x + self.player.width / 2, self.player.y + self.player.height / 2, 3)
        self.particle_system = ParticleSystem()
        self.particle_update_timer = 0
        self.main_menu = MainMenu(width, height)

    def run(self):
        pyray.init_window(self.width, self.height, "game")
        # pyray.set_target_fps(60)
        while not pyray.window_should_close():
            delta_time = pyray.get_frame_time()
            if self.main_menu.show_menu:
                self.main_menu.render()
            else:
                self.update(delta_time)
                self.render()
        pyray.close_window()

    def update(self, delta_time):
        self.camera.update_target(self.player.x + self.player.width / 2, self.player.y + self.player.height / 2, delta_time)
        self.camera.adjust_zoom(self.player.vx, delta_time)
        self.player.movement(delta_time, self.blocks, self.camera)

        # # Update the timer
        self.particle_update_timer += delta_time
        #
        # # Add particles behind the player when moving, but only update once each second
        if self.particle_update_timer >= 0.01:
            if self.player.sliding:
                self.particle_system.add_particle(self.player.x + random.randint(0, self.player.width), self.player.y + self.player.height, -self.player.vx * 0.0001, random.uniform(-1, -3), 100, 5, random.randint(1, 5), (0, 0, 255, 100), 'circle')
            self.particle_update_timer = 0

        self.particle_system.update(delta_time)
        self.particle_system.apply_force_to_all(0, 9.81 * delta_time)

    def render(self):
        pyray.begin_drawing()
        pyray.clear_background(pyray.BLACK)
        self.camera.begin_mode()
        self.player.draw()
        for block in self.blocks:
            block.draw()
        self.particle_system.draw()
        self.camera.end_mode()
        pyray.draw_fps(10, 10)
        pyray.draw_text("Player", 10, 30, 10, pyray.RED)
        for parameter in self.player.__dict__:
            pyray.draw_text(parameter + ": " + str(self.player.__dict__[parameter]), 10,
                            40 + 10 * list(self.player.__dict__.keys()).index(parameter), 10, pyray.WHITE)
        for i, block in enumerate(self.blocks):
            pyray.draw_text("Block " + str(i), 200 * i + 200, 20, 10, pyray.BLUE)
            for parameter in block.__dict__:
                pyray.draw_text(parameter + ": " + str(block.__dict__[parameter]), 200 * i + 200,
                                30 + 10 * list(block.__dict__.keys()).index(parameter), 10, pyray.WHITE)
        pyray.end_drawing()