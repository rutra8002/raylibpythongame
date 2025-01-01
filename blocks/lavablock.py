import raylib
import pyray
from blocks.block import Block
import shaders

class LavaBlock(Block):
    def __init__(self, height, width, x, y, color):
        super().__init__(height, width, x, y, color)
        self.shader = shaders.shaders["lava"]

    def draw(self, camera):
        if camera is not None and shaders.shaders_enabled:
            raylib.BeginShaderMode(self.shader)

            # Time uniform
            time_value = pyray.ffi.new("float *", raylib.GetTime())
            raylib.SetShaderValue(self.shader, raylib.GetShaderLocation(self.shader, b"time"), time_value,
                                  raylib.SHADER_UNIFORM_FLOAT)

            # Resolution uniform
            resolution_value = pyray.ffi.new("float[2]", [camera.camera.offset.x * 2, -camera.camera.offset.y * 2])
            raylib.SetShaderValue(self.shader, raylib.GetShaderLocation(self.shader, b"resolution"), resolution_value,
                                  raylib.SHADER_UNIFORM_VEC2)

            # Camera offset uniform
            camera_offset_value = pyray.ffi.new("float[2]", [camera.camera.target.x, -camera.camera.target.y])
            raylib.SetShaderValue(self.shader, raylib.GetShaderLocation(self.shader, b"camera_offset"),
                                  camera_offset_value, raylib.SHADER_UNIFORM_VEC2)

            # Block position uniform
            block_position_value = pyray.ffi.new("float[2]", [self.x, self.y])
            raylib.SetShaderValue(self.shader, raylib.GetShaderLocation(self.shader, b"block_position"),
                                  block_position_value, raylib.SHADER_UNIFORM_VEC2)

            # Block size uniform
            block_size_value = pyray.ffi.new("float[2]", [self.width, self.height])
            raylib.SetShaderValue(self.shader, raylib.GetShaderLocation(self.shader, b"block_size"), block_size_value,
                                  raylib.SHADER_UNIFORM_VEC2)

            # Camera zoom uniform
            camera_zoom_value = pyray.ffi.new("float *", camera.camera.zoom)
            raylib.SetShaderValue(self.shader, raylib.GetShaderLocation(self.shader, b"camera_zoom"), camera_zoom_value,
                                  raylib.SHADER_UNIFORM_FLOAT)

            # Draw block
            raylib.DrawRectangle(int(self.x), int(self.y), self.width, self.height, pyray.WHITE)
            raylib.EndShaderMode()
        else:
            raylib.DrawRectangle(int(self.x), int(self.y), self.width, self.height, pyray.ORANGE)

    def check_vertical_collision(self, other):
        collision_side = super().check_vertical_collision(other)
        if collision_side:
            other.can_jump = False
            other.speed = 6.9
            if other.time_since_last_damage > 0.1:
                other.take_damage(10)
                other.time_since_last_damage = 0
                other.vx = 0
                other.vy = 0

    def check_horizontal_collision(self, other):
        collision_side = super().check_horizontal_collision(other)
        if collision_side:
            other.can_jump = False
            other.speed = 6.9
            if other.time_since_last_damage > 0.1:
                other.take_damage(10)
                other.time_since_last_damage = 0
                other.vx = 0
                other.vy = 0