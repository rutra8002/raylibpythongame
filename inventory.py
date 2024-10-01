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
        hotbar_width = 400
        hotbar_height = 50
        item_width = hotbar_width // len(self.items)
        hotbar_x = (screen_width - hotbar_width) // 2
        hotbar_y = screen_height - hotbar_height - 10

        for i, item in enumerate(self.items):
            item_x = hotbar_x + i * item_width
            item_y = hotbar_y
            color = pyray.GRAY if i == self.selected_index else pyray.DARKGRAY
            pyray.draw_rectangle(item_x, item_y, item_width, hotbar_height, color)
            pyray.draw_text(item.name, item_x + 10, item_y + 10, 20, pyray.WHITE)

            # Highlight the selected item
            if i == self.selected_index:
                pyray.draw_rectangle_lines(item_x, item_y, item_width, hotbar_height, pyray.YELLOW)