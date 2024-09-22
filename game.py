import os
import random
import pyray
from player import Player
from camera import Camera
from particles import ParticleSystem
from main_menu import MainMenu
from map_selection_menu import MapSelectionMenu
from map_loader import load_map

class Game:
    def __init__(self, width=1366, height=768):
        self.width = width
        self.height = height
        self.player = Player(50, 50, 100, 100, pyray.RED, 70)
        self.blocks = []
        self.camera = Camera(width, height, self.player.x + self.player.width / 2, self.player.y + self.player.height / 2, 3)
        self.particle_system = ParticleSystem()
        self.particle_update_timer = 0
        self.main_menu = MainMenu(width, height)
        self.map_selection_menu = MapSelectionMenu(width, height)
        self.map_selection_menu.load_maps('maps')

    def run(self):
        pyray.init_window(self.width, self.height, "game")
        while not pyray.window_should_close():
            delta_time = pyray.get_frame_time()
            if self.main_menu.show_menu:
                self.main_menu.render()
            elif self.map_selection_menu.show_menu:
                self.map_selection_menu.render()
            else:
                if not self.blocks and self.map_selection_menu.selected_map:
                    self.blocks = load_map(os.path.join('maps', self.map_selection_menu.selected_map))
                self.update(delta_time)
                self.render()
        pyray.close_window()

    def update(self, delta_time):
        self.camera.update_target(self.player.x + self.player.width / 2, self.player.y + self.player.height / 2, delta_time)
        self.camera.adjust_zoom(self.player.vx, delta_time)
        self.player.movement(delta_time, self.blocks, self.camera)

        self.particle_update_timer += delta_time
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