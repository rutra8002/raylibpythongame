import pyray
import os

class MapSelectionMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maps = []
        self.selected_map = None
        self.show_menu = True

    def load_maps(self, directory):
        self.maps = [f for f in os.listdir(directory) if f.endswith('.json')]

    def render(self):
        pyray.begin_drawing()
        pyray.clear_background(pyray.BLACK)
        pyray.draw_text("Select Map", int(self.width / 2 - 100), 100, 40, pyray.WHITE)

        for i, map_name in enumerate(self.maps):
            if pyray.gui_button(pyray.Rectangle(self.width / 2 - 100, self.height / 2 + 10 + i * 60, 200, 50), map_name):
                self.selected_map = map_name
                self.show_menu = False

        if pyray.gui_button(pyray.Rectangle(self.width / 2 - 100, self.height / 2 + 10 + len(self.maps) * 60, 200, 50), "Back"):
            self.show_menu = False
            self.selected_map = None

        pyray.end_drawing()