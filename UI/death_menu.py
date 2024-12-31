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
            text = "You Died"
            text_width = pyray.measure_text(text, 40)
            pyray.draw_text(text, int((self.width - text_width) / 2), int(self.height * 0.1), 40, pyray.WHITE)

            self.retry_button.rect.x = self.width / 2 - self.retry_button.rect.width / 2
            self.retry_button.rect.y = self.height / 2 - self.retry_button.rect.height - 10
            self.retry_button.update()
            self.retry_button.draw()

            self.main_menu_button.rect.x = self.width / 2 - self.main_menu_button.rect.width / 2
            self.main_menu_button.rect.y = self.height / 2 + self.main_menu_button.rect.height + 10
            self.main_menu_button.update()
            self.main_menu_button.draw()

            pyray.end_drawing()