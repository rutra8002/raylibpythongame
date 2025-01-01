import pyray

class Camera:
    def __init__(self, width, height, target_x, target_y, smooth_factor, initial_zoom=2.0):
        self.camera = pyray.Camera2D()
        self.camera.target = pyray.Vector2(target_x, target_y)
        self.camera.offset = pyray.Vector2(width / 2, height / 2)
        self.camera.rotation = 0.0
        self.camera.zoom = initial_zoom
        self.smooth_factor = smooth_factor
        self.target_zoom = self.calculate_target_zoom(width, height)

    def calculate_target_zoom(self, width, height):
        reference_width = 1366
        reference_height = 768
        return min(width / reference_width, height / reference_height)

    def update_target(self, target_x, target_y, delta_time):
        self.camera.target.x += (target_x - self.camera.target.x) * self.smooth_factor * delta_time
        self.camera.target.y += (target_y - self.camera.target.y) * self.smooth_factor * delta_time

    def adjust_zoom(self, player_speed, delta_time):
        self.target_zoom = self.calculate_target_zoom(self.camera.offset.x * 2, self.camera.offset.y * 2)
        self.camera.zoom += (self.target_zoom - self.camera.zoom) * self.smooth_factor * delta_time

    def zoom_intro(self, delta_time):
        self.camera.zoom += (self.target_zoom - self.camera.zoom) * self.smooth_factor * delta_time

    def begin_mode(self):
        pyray.begin_mode_2d(self.camera)

    def end_mode(self):
        pyray.end_mode_2d()