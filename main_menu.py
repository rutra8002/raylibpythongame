import pyray
import os
from button import Button
class MainMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.show_menu = True
        self.show_map_selection = False
        self.maps = []
        self.selected_map = None
        self.start_button = Button(width / 2 - 100, height / 2 - 50, 200, 50, "Start Game", 20, pyray.WHITE, pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)
        self.exit_button = Button(width / 2 - 100, height / 2 + 10, 200, 50, "Exit", 20, pyray.WHITE, pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)

    def load_maps(self, directory):
        self.maps = [f for f in os.listdir(directory) if f.endswith('.json')]

    def render(self):
        pyray.begin_drawing()
        pyray.clear_background(pyray.BLACK)
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
        elif self.show_map_selection:
            pyray.draw_text("Select Map", int(self.width / 2 - 100), 100, 40, pyray.WHITE)

            for i, map_name in enumerate(self.maps):
                map_button = Button(self.width / 2 - 100, self.height / 2 - 50 + i * 60, 200, 50, map_name, 20, pyray.WHITE, pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)
                map_button.update()
                map_button.draw()
                if map_button.is_clicked:
                    self.selected_map = map_name
                    self.show_map_selection = False

            back_button = Button(self.width / 2 - 100, self.height / 2 - 50 + len(self.maps) * 60, 200, 50, "Back", 20, pyray.WHITE, pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)
            back_button.update()
            back_button.draw()
            if back_button.is_clicked:
                self.show_map_selection = False
                self.show_menu = True

        pyray.end_drawing()