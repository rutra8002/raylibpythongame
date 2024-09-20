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

    def update_position(self, player_x, player_y, delta_time):
        if self.is_grappling:
            direction_x = self.target_x - player_x
            direction_y = self.target_y - player_y
            distance = (direction_x ** 2 + direction_y ** 2) ** 0.5
            if distance < self.speed * delta_time:
                return self.target_x, self.target_y, True
            else:
                new_x = player_x + direction_x / distance * self.speed * delta_time
                new_y = player_y + direction_y / distance * self.speed * delta_time
                return new_x, new_y, False
        return player_x, player_y, False