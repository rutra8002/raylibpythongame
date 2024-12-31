import pyray
from UI.button import Button

class PauseMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.is_visible = False
        self.resume_button = Button(width / 2 - 100, height / 2 - 50, 200, 50, "Resume", 20, pyray.WHITE, pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)
        self.settings_button = Button(width / 2 - 100, height / 2 + 10, 200, 50, "Settings", 20, pyray.WHITE, pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)
        self.main_menu_button = Button(width / 2 - 100, height / 2 + 70, 200, 50, "Main Menu", 20, pyray.WHITE, pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)

    def toggle(self):
        self.is_visible = not self.is_visible

    def render(self):
        if self.is_visible:
            pyray.begin_drawing()
            pyray.clear_background(pyray.BLACK)
            text = "Pause Menu"
            text_width = pyray.measure_text(text, 40)
            pyray.draw_text(text, int((self.width - text_width) / 2), int(self.height * 0.1), 40, pyray.WHITE)

            self.resume_button.rect.x = self.width / 2 - self.resume_button.rect.width / 2
            self.resume_button.rect.y = self.height / 2 - self.resume_button.rect.height - 10
            self.resume_button.update()
            self.resume_button.draw()

            self.settings_button.rect.x = self.width / 2 - self.settings_button.rect.width / 2
            self.settings_button.rect.y = self.height / 2
            self.settings_button.update()
            self.settings_button.draw()

            self.main_menu_button.rect.x = self.width / 2 - self.main_menu_button.rect.width / 2
            self.main_menu_button.rect.y = self.height / 2 + self.main_menu_button.rect.height + 10
            self.main_menu_button.update()
            self.main_menu_button.draw()

            pyray.end_drawing()