import pyray

class Inventory:
    def __init__(self):
        self.items = []
        self.selected_index = 0

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def select_next_item(self):
        self.selected_index = (self.selected_index + 1) % len(self.items)

    def select_previous_item(self):
        self.selected_index = (self.selected_index - 1) % len(self.items)

    def get_selected_item(self):
        if self.items:
            return self.items[self.selected_index]
        return None

    def render(self, screen_width, screen_height):
        hotbar_width = screen_width // 2
        hotbar_height = screen_height // 15
        item_width = hotbar_width // len(self.items)
        hotbar_x = (screen_width - hotbar_width) // 2
        hotbar_y = screen_height - hotbar_height - 10
        font_size = int(screen_height * 0.03)
        ammo_font_size = int(screen_height * 0.02)

        for i, item in enumerate(self.items):
            item_x = hotbar_x + i * item_width
            item_y = hotbar_y
            color = pyray.GRAY if i == self.selected_index else pyray.DARKGRAY

            pyray.draw_rectangle(item_x + 2, item_y + 2, item_width, hotbar_height, pyray.fade(pyray.BLACK, 0.5))
            pyray.draw_rectangle_rounded(pyray.Rectangle(item_x, item_y, item_width, hotbar_height), 0.2, 10, color)

            if hasattr(item, 'texture'):
                max_texture_width = item_width // 2
                max_texture_height = hotbar_height - 20
                texture_aspect_ratio = item.texture.width / item.texture.height

                if max_texture_width / texture_aspect_ratio <= max_texture_height:
                    texture_width = max_texture_width
                    texture_height = max_texture_width / texture_aspect_ratio
                else:
                    texture_height = max_texture_height
                    texture_width = max_texture_height * texture_aspect_ratio

                texture_x = item_x + 10
                texture_y = item_y + (hotbar_height - texture_height) // 2

                pyray.draw_texture_pro(
                    item.texture,
                    pyray.Rectangle(0, 0, item.texture.width, item.texture.height),
                    pyray.Rectangle(texture_x, texture_y, texture_width, texture_height),
                    pyray.Vector2(0, 0),
                    0,
                    pyray.WHITE
                )

                text_x = texture_x + texture_width + 10
            else:
                text_x = item_x + 10

            pyray.draw_text_ex(pyray.get_font_default(), item.name, pyray.Vector2(int(text_x), int(item_y) + int(screen_height * 0.005)), font_size, 2, pyray.WHITE)

            if hasattr(item, 'ammo'):
                ammo_text = f"Ammo: {item.ammo}"
                ammo_text_x = text_x
                pyray.draw_text_ex(pyray.get_font_default(), ammo_text, pyray.Vector2(int(ammo_text_x), int(item_y) + int(screen_height * 0.04)), ammo_font_size, 2, pyray.RED)

        for i, item in enumerate(self.items):
            if i == self.selected_index:
                item_x = hotbar_x + i * item_width
                item_y = hotbar_y
                pyray.draw_rectangle_rounded_lines_ex(pyray.Rectangle(item_x, item_y, item_width, hotbar_height), 0.2, 10, 4, pyray.YELLOW)