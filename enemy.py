import pyray
from gameobject import GameObject

class Enemy(GameObject):
    def __init__(self, height, width, x, y, color, health):
        super().__init__(height, width, x, y, color)
        self.health = health

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            return True  # Enemy is ded
        return False  # Enemy is still alive

    def draw(self):
        super().draw()
        self.draw_health_bar()

    def draw_health_bar(self):
        bar_width = self.width
        bar_height = 10
        health_percentage = self.health / 100
        health_bar_width = bar_width * health_percentage
        pyray.draw_rectangle(int(self.x), int(self.y) - 20, bar_width, bar_height, pyray.RED)
        pyray.draw_rectangle(int(self.x), int(self.y) - 20, int(health_bar_width), bar_height, pyray.GREEN)