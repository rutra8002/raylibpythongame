import raylib
import pyray

class Button:
    def __init__(self, x, y, width, height, text, text_size, text_color, button_color, hover_color, click_color):
        self.rect = pyray.Rectangle(x, y, width, height)
        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.click_color = click_color
        self.is_hovered = False
        self.is_clicked = False

    def update(self):
        mouse_point = raylib.GetMousePosition()
        self.is_hovered = raylib.CheckCollisionPointRec(mouse_point, self.rect)
        self.is_clicked = self.is_hovered and raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_LEFT)

    def draw(self):
        if self.is_clicked:
            color = self.click_color
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.button_color

        raylib.DrawRectangleRec(self.rect, color)
        text_width = raylib.MeasureText(self.text.encode('utf-8'), self.text_size)
        text_x = self.rect.x + (self.rect.width - text_width) / 2
        text_y = self.rect.y + (self.rect.height - self.text_size) / 2
        raylib.DrawText(self.text.encode('utf-8'), int(text_x), int(text_y), self.text_size, self.text_color)