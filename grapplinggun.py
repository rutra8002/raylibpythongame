import pyray

class GrapplingGun:
    def __init__(self, range, speed):
        self.range = range
        self.speed = speed
        self.is_grappling = False
        self.target_x = None
        self.target_y = None

    def shoot(self, target_x, target_y, blocks):
        self.is_grappling = True
        nearest_edge = self.find_nearest_edge(target_x, target_y, blocks)
        if nearest_edge:
            self.target_x, self.target_y = nearest_edge

    def find_nearest_edge(self, target_x, target_y, blocks):
        nearest_edge = None
        min_distance = float('inf')
        for block in blocks:
            edges = [
                (block.x, block.y),  # top-left
                (block.x + block.width, block.y),  # top-right
                (block.x, block.y + block.height),  # bottom-left
                (block.x + block.width, block.y + block.height)  # bottom-right
            ]
            for edge_x, edge_y in edges:
                distance = ((target_x - edge_x) ** 2 + (target_y - edge_y) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    nearest_edge = (edge_x, edge_y)
        return nearest_edge

    def reset(self):
        self.is_grappling = False
        self.target_x = None
        self.target_y = None

    def draw(self, player_x, player_y):
        if self.is_grappling and self.target_x is not None and self.target_y is not None:
            pyray.draw_line(int(player_x), int(player_y), int(self.target_x), int(self.target_y), pyray.RED)

    def update_position(self, player_x, player_y, delta_time):
        if self.is_grappling and self.target_x is not None and self.target_y is not None:
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