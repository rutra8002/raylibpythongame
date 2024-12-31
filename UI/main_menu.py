import sys
import pyray
import os
import shaders
from UI.button import Button
from particles import ParticleSystem
import random

class MainMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.show_menu = True
        self.show_map_selection = False
        self.show_settings = False
        self.maps = []
        self.selected_map = None
        self.fullscreen = False
        self.resolutions = [(1366, 768), (1920, 1080), (2560, 1440)]
        self.current_resolution_index = 0
        self.start_button = Button(width / 2 - 100, height / 2 - 50, 200, 50, "Start Game", 20, pyray.WHITE,
                                   pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)
        self.settings_button = Button(width / 2 - 100, height / 2 + 10, 200, 50, "Settings", 20, pyray.WHITE,
                                      pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)
        self.exit_button = Button(width / 2 - 100, height / 2 + 70, 200, 50, "Exit", 20, pyray.WHITE, pyray.DARKGRAY,
                                  pyray.GRAY, pyray.LIGHTGRAY)
        self.particle_system = ParticleSystem()

    def load_maps(self, directory):
        self.maps = [f for f in os.listdir(directory) if f.endswith('.json')]

    def render(self):
        pyray.begin_drawing()
        pyray.clear_background(pyray.BLACK)

        # Update and draw particles
        self.particle_system.update(pyray.get_frame_time(), None, None, None)
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
                'circle',
                None
            )

        if self.show_menu:
            text = "Main Menu"
            text_width = pyray.measure_text(text, 40)
            pyray.draw_text(text, int((self.width - text_width) / 2), int(self.height * 0.1), 40, pyray.WHITE)

            self.start_button.rect.x = self.width / 2 - self.start_button.rect.width / 2
            self.start_button.rect.y = self.height / 2 - self.start_button.rect.height - 10
            self.start_button.update()
            self.start_button.draw()
            if self.start_button.is_clicked:
                self.show_menu = False
                self.show_map_selection = True

            self.settings_button.rect.x = self.width / 2 - self.settings_button.rect.width / 2
            self.settings_button.rect.y = self.height / 2
            self.settings_button.update()
            self.settings_button.draw()
            if self.settings_button.is_clicked:
                self.show_menu = False
                self.show_settings = True

            self.exit_button.rect.x = self.width / 2 - self.exit_button.rect.width / 2
            self.exit_button.rect.y = self.height / 2 + self.exit_button.rect.height + 10
            self.exit_button.update()
            self.exit_button.draw()
            if self.exit_button.is_clicked:
                pyray.close_window()
                sys.exit()
        elif self.show_map_selection:
            text = "Select Map"
            text_width = pyray.measure_text(text, 40)
            pyray.draw_text(text, int((self.width - text_width) / 2), int(self.height * 0.1), 40, pyray.WHITE)

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
                map_button = Button(x, y, button_width, button_height, map_name, 20, pyray.WHITE, pyray.DARKGRAY,
                                    pyray.GRAY, pyray.LIGHTGRAY)
                map_button.update()
                map_button.draw()
                if map_button.is_clicked:
                    self.selected_map = map_name
                    self.show_map_selection = False

            back_button = Button(self.width / 2 - 100,
                                 start_y + (len(self.maps) // columns + 1) * (button_height + padding), 200, 50, "Back",
                                 20,
                                 pyray.WHITE, pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)
            back_button.update()
            back_button.draw()
            if back_button.is_clicked:
                self.show_map_selection = False
                self.show_menu = True
        elif self.show_settings:
            text = "Settings"
            text_width = pyray.measure_text(text, 40)
            pyray.draw_text(text, int((self.width - text_width) / 2), int(self.height * 0.1), 40, pyray.WHITE)

            shaders_text = "Shaders"
            pyray.draw_text(shaders_text, 50, 215, 20, pyray.WHITE)

            shaders_button_text = "Enabled" if shaders.shaders_enabled else "Disabled"
            shaders_button = Button(200, 200, 200, 50, shaders_button_text, 20,
                                    pyray.WHITE, pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)
            shaders_button.update()
            shaders_button.draw()
            if shaders_button.is_clicked:
                shaders.shaders_enabled = not shaders.shaders_enabled

            resolution_text = "Resolution"
            pyray.draw_text(resolution_text, 50, 275, 20, pyray.WHITE)

            resolution_button_text = f"{self.resolutions[self.current_resolution_index][0]}x{self.resolutions[self.current_resolution_index][1]}"
            resolution_button = Button(200, 260, 200, 50, resolution_button_text, 20,
                                       pyray.WHITE, pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)
            resolution_button.update()
            resolution_button.draw()
            if resolution_button.is_clicked:
                self.current_resolution_index = (self.current_resolution_index + 1) % len(self.resolutions)
                self.width, self.height = self.resolutions[self.current_resolution_index]
                pyray.set_window_size(self.width, self.height)

            fullscreen_text = "Fullscreen"
            pyray.draw_text(fullscreen_text, 50, 335, 20, pyray.WHITE)

            fullscreen_button_text = "Enabled" if self.fullscreen else "Disabled"
            fullscreen_button = Button(200, 320, 200, 50, fullscreen_button_text, 20,
                                       pyray.WHITE, pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)
            fullscreen_button.update()
            fullscreen_button.draw()
            if fullscreen_button.is_clicked:
                self.fullscreen = not self.fullscreen
                pyray.toggle_fullscreen()

            back_button = Button(self.width / 2 - 100, self.height / 2 + 70, 200, 50, "Back", 20, pyray.WHITE,
                                 pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)
            back_button.update()
            back_button.draw()
            if back_button.is_clicked:
                self.show_settings = False
                self.show_menu = True

        pyray.end_drawing()