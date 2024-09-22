import pyray
import os

class MainMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.show_menu = True
        self.maps = []
        self.selected_map = None

    def load_maps(self, directory):
        self.maps = [f for f in os.listdir(directory) if f.endswith('.json')]

    def render(self):
        pyray.begin_drawing()
        pyray.clear_background(pyray.BLACK)
        pyray.draw_text("Main Menu", int(self.width / 2 - 100), 100, 40, pyray.WHITE)

        if pyray.gui_button(pyray.Rectangle(self.width / 2 - 100, self.height / 2 - 50, 200, 50), "Start Game"):
            self.show_menu = False

        for i, map_name in enumerate(self.maps):
            if pyray.gui_button(pyray.Rectangle(self.width / 2 - 100, self.height / 2 + 10 + i * 60, 200, 50), map_name):
                self.selected_map = map_name
                self.show_menu = False

        if pyray.gui_button(pyray.Rectangle(self.width / 2 - 100, self.height / 2 + 10 + len(self.maps) * 60, 200, 50), "Exit"):
            pyray.close_window()

        pyray.end_drawing()