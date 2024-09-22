import pyray

class Camera:
    def __init__(self, width, height, target_x, target_y, smooth_factor):
        self.camera = pyray.Camera2D()
        self.camera.target = pyray.Vector2(target_x, target_y)
        self.camera.offset = pyray.Vector2(width / 2, height / 2)
        self.camera.rotation = 0.0
        self.camera.zoom = 1.0
        self.smooth_factor = smooth_factor

    def update_target(self, target_x, target_y, delta_time):
        self.camera.target.x += (target_x - self.camera.target.x) * self.smooth_factor * delta_time
        self.camera.target.y += (target_y - self.camera.target.y) * self.smooth_factor * delta_time

    def adjust_zoom(self, player_speed, delta_time):
        if abs(player_speed) > 400:
            target_zoom = 400/abs(player_speed)
        else:
            target_zoom = 1
        self.camera.zoom += (target_zoom - self.camera.zoom) * self.smooth_factor * delta_time

    def begin_mode(self):
        pyray.begin_mode_2d(self.camera)

    def end_mode(self):
        pyray.end_mode_2d()