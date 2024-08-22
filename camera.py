import pyray

class Camera:
    def __init__(self, width, height, target_x, target_y):
        self.camera = pyray.Camera2D()
        self.camera.target = pyray.Vector2(target_x, target_y)
        self.camera.offset = pyray.Vector2(width / 2, height / 2)
        self.camera.rotation = 0.0
        self.camera.zoom = 1.0

    def update_target(self, target_x, target_y):
        self.camera.target = pyray.Vector2(target_x, target_y)

    def begin_mode(self):
        pyray.begin_mode_2d(self.camera)

    def end_mode(self):
        pyray.end_mode_2d()