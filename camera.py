import pyray
import random

class Camera:
    def __init__(self, width, height, target_x, target_y, smooth_factor):
        self.camera = pyray.Camera2D()
        self.camera.target = pyray.Vector2(target_x, target_y)
        self.camera.offset = pyray.Vector2(width / 2, height / 2)
        self.camera.rotation = 0.0
        self.camera.zoom = 1.0
        self.smooth_factor = smooth_factor
        self.shake_duration = 0
        self.shake_magnitude = 0

    def update_target(self, target_x, target_y, delta_time):
        self.camera.target.x += (target_x - self.camera.target.x) * self.smooth_factor * delta_time
        self.camera.target.y += (target_y - self.camera.target.y) * self.smooth_factor * delta_time

    def adjust_zoom(self, player_speed, delta_time):
        if abs(player_speed) > 400:
            target_zoom = 400/abs(player_speed)
        else:
            target_zoom = 1
        self.camera.zoom += (target_zoom - self.camera.zoom) * self.smooth_factor * delta_time

    def apply_shake(self, duration, magnitude):
        self.shake_duration = duration
        self.shake_magnitude = magnitude

    def update_shake(self, delta_time):
        if self.shake_duration > 0:
            self.shake_duration -= delta_time
            shake_x = random.uniform(-1, 1) * self.shake_magnitude
            shake_y = random.uniform(-1, 1) * self.shake_magnitude
            self.camera.target.x += shake_x
            self.camera.target.y += shake_y

    def begin_mode(self):
        self.update_shake(pyray.get_frame_time())
        pyray.begin_mode_2d(self.camera)

    def end_mode(self):
        pyray.end_mode_2d()