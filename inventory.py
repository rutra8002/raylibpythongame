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