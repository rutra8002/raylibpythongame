import pyray
from UI.button import Button

class DeathMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.is_visible = False
        self.retry_button = Button(width / 2 - 100, height / 2 - 50, 200, 50, "Retry", 20, pyray.WHITE, pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)
        self.main_menu_button = Button(width / 2 - 100, height / 2 + 10, 200, 50, "Main Menu", 20, pyray.WHITE, pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)

    def toggle(self):
        self.is_visible = not self.is_visible

    def render(self):
        if self.is_visible:
            pyray.begin_drawing()
            pyray.clear_background(pyray.BLACK)
            pyray.draw_text("You Died", int(self.width / 2 - 100), 100, 40, pyray.WHITE)
            self.retry_button.update()
            self.retry_button.draw()
            self.main_menu_button.update()
            self.main_menu_button.draw()
            pyray.end_drawing()