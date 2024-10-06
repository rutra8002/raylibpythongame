import pyray
from button import Button

class PauseMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.is_visible = False
        self.resume_button = Button(width / 2 - 100, height / 2 - 50, 200, 50, "Resume", 20, pyray.WHITE, pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)
        self.main_menu_button = Button(width / 2 - 100, height / 2 + 10, 200, 50, "Main Menu", 20, pyray.WHITE, pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)
        self.toggle_callback = None

    def toggle(self):
        self.is_visible = not self.is_visible
        if self.toggle_callback:
            self.toggle_callback(self.is_visible)

    def render(self):
        if self.is_visible:
            pyray.begin_drawing()
            pyray.clear_background(pyray.BLACK)
            pyray.draw_text("Pause Menu", int(self.width / 2 - 100), 100, 40, pyray.WHITE)
            self.resume_button.update()
            self.resume_button.draw()
            self.main_menu_button.update()
            self.main_menu_button.draw()
            pyray.end_drawing()