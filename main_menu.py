import pyray

class MainMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.show_menu = True

    def render(self):
        pyray.begin_drawing()
        pyray.clear_background(pyray.BLACK)
        pyray.draw_text("Main Menu", int(self.width / 2 - 100), 100, 40, pyray.WHITE)

        if pyray.gui_button(pyray.Rectangle(self.width / 2 - 100, self.height / 2 - 50, 200, 50), "Start Game"):
            self.show_menu = False

        if pyray.gui_button(pyray.Rectangle(self.width / 2 - 100, self.height / 2 + 10, 200, 50), "Exit"):
            pyray.close_window()

        pyray.end_drawing()