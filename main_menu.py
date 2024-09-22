import pyray
import os

class MainMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.show_menu = True
        self.show_map_selection = False
        self.maps = []
        self.selected_map = None

    def load_maps(self, directory):
        self.maps = [f for f in os.listdir(directory) if f.endswith('.json')]

    def render(self):
        pyray.begin_drawing()
        pyray.clear_background(pyray.BLACK)
        if self.show_menu:
            pyray.draw_text("Main Menu", int(self.width / 2 - 100), 100, 40, pyray.WHITE)

            if pyray.gui_button(pyray.Rectangle(self.width / 2 - 100, self.height / 2 - 50, 200, 50), "Start Game"):
                self.show_menu = False
                self.show_map_selection = True

            if pyray.gui_button(pyray.Rectangle(self.width / 2 - 100, self.height / 2 + 10, 200, 50), "Exit"):
                pyray.close_window()
        elif self.show_map_selection:
            pyray.draw_text("Select Map", int(self.width / 2 - 100), 100, 40, pyray.WHITE)

            for i, map_name in enumerate(self.maps):
                if pyray.gui_button(pyray.Rectangle(self.width / 2 - 100, self.height / 2 + 10 + i * 60, 200, 50), map_name):
                    self.selected_map = map_name
                    self.show_map_selection = False

            if pyray.gui_button(pyray.Rectangle(self.width / 2 - 100, self.height / 2 + 10 + len(self.maps) * 60, 200, 50), "Back"):
                self.show_map_selection = False
                self.show_menu = True

        pyray.end_drawing()