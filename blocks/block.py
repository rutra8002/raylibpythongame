import os
import raylib
from gameobject import GameObject
import images

class Block(GameObject):
    def __init__(self, height, width, x, y, color):
        super().__init__(height, width, x, y, color)
        self.texture = images.textures["block"]

    def draw(self):
        for i in range(0, self.width, self.texture.width):
            for j in range(0, self.height, self.texture.height):
                raylib.DrawTexture(self.texture, int(self.x + i), int(self.y + j), raylib.WHITE)