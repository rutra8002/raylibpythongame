import pyray

class GrapplingGun:
    def __init__(self, range, speed):
        self.range = range
        self.speed = speed
        self.is_grappling = False
        self.target_x = None
        self.target_y = None

    def shoot(self, target_x, target_y):
        self.is_grappling = True
        self.target_x = target_x
        self.target_y = target_y

    def reset(self):
        self.is_grappling = False
        self.target_x = None
        self.target_y = None

    def draw(self, player_x, player_y):
        if self.is_grappling:
            pyray.draw_line(int(player_x), int(player_y), int(self.target_x), int(self.target_y), pyray.RED)