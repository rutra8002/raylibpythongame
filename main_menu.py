import sys

import pyray
import os
from button import Button
from particles import ParticleSystem
import random


class MainMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.show_menu = True
        self.show_map_selection = False
        self.maps = []
        self.selected_map = None
        self.start_button = Button(width / 2 - 100, height / 2 - 50, 200, 50, "Start Game", 20, pyray.WHITE,
                                   pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)
        self.exit_button = Button(width / 2 - 100, height / 2 + 10, 200, 50, "Exit", 20, pyray.WHITE, pyray.DARKGRAY,
                                  pyray.GRAY, pyray.LIGHTGRAY)
        self.particle_system = ParticleSystem()

    def load_maps(self, directory):
        self.maps = [f for f in os.listdir(directory) if f.endswith('.json')]

    def render(self):
        pyray.begin_drawing()
        pyray.clear_background(pyray.BLACK)

        # Update and draw particles
        self.particle_system.update(pyray.get_frame_time())
        self.particle_system.draw()

        if random.randint(0, 10) > 8:
            self.particle_system.add_particle(
                random.uniform(0, self.width),
                random.uniform(0, self.height),
                random.uniform(-1, 1),
                random.uniform(-1, 1),
                random.randint(10, 50),
                20,
                3,
                (random.randint(1, 150), random.randint(1, 150), random.randint(1, 150), random.randint(50, 200)),
                'circle'
            )

        if self.show_menu:
            pyray.draw_text("Main Menu", int(self.width / 2 - 100), 100, 40, pyray.WHITE)

            self.start_button.update()
            self.start_button.draw()
            if self.start_button.is_clicked:
                self.show_menu = False
                self.show_map_selection = True

            self.exit_button.update()
            self.exit_button.draw()
            if self.exit_button.is_clicked:
                pyray.close_window()
                sys.exit()
        elif self.show_map_selection:
            pyray.draw_text("Select Map", int(self.width / 2 - 100), 100, 40, pyray.WHITE)

            columns = 3
            button_width = 200
            button_height = 50
            padding = 10
            start_x = (self.width - (columns * (button_width + padding) - padding)) / 2
            start_y = 200

            for i, map_name in enumerate(self.maps):
                col = i % columns
                row = i // columns
                x = start_x + col * (button_width + padding)
                y = start_y + row * (button_height + padding)
                map_button = Button(x, y, button_width, button_height, map_name, 20, pyray.WHITE, pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)
                map_button.update()
                map_button.draw()
                if map_button.is_clicked:
                    self.selected_map = map_name
                    self.show_map_selection = False

            back_button = Button(self.width / 2 - 100, start_y + (len(self.maps) // columns + 1) * (button_height + padding), 200, 50, "Back", 20,
                                 pyray.WHITE, pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)
            back_button.update()
            back_button.draw()
            if back_button.is_clicked:
                self.show_map_selection = False
                self.show_menu = True

        pyray.end_drawing()