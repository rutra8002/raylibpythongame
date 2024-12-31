import raylib
import pyray
from blocks.block import Block
import shaders

class LavaBlock(Block):
    def __init__(self, height, width, x, y, color):
        super().__init__(height, width, x, y, color)
        self.shader = shaders.shaders["lava"]

    def draw(self):
        raylib.BeginShaderMode(self.shader)
        time_value = pyray.ffi.new("float *", raylib.GetTime())
        resolution_value = pyray.ffi.new("float[2]", [self.width, self.height])
        raylib.SetShaderValue(self.shader, raylib.GetShaderLocation(self.shader, b"time"), time_value, raylib.SHADER_UNIFORM_FLOAT)
        raylib.SetShaderValue(self.shader, raylib.GetShaderLocation(self.shader, b"resolution"), resolution_value, raylib.SHADER_UNIFORM_VEC2)
        raylib.DrawRectangle(int(self.x), int(self.y), self.width, self.height, pyray.WHITE)
        raylib.EndShaderMode()

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