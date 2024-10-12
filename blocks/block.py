import os
import raylib
from gameobject import GameObject

class Block(GameObject):
    def __init__(self, height, width, x, y, color):
        super().__init__(height, width, x, y, color)
        texture_path = os.path.join(os.path.dirname(__file__), '../images/block.png')
        print(f"Loading texture from: {texture_path}")  # Debug logging
        self.texture = raylib.LoadTexture(texture_path.encode('utf-8'))
        if self.texture.id == 0:
            raise ValueError("Failed to load texture")

    def draw(self):
        for i in range(0, self.width, self.texture.width):
            for j in range(0, self.height, self.texture.height):
                raylib.DrawTexture(self.texture, int(self.x + i), int(self.y + j), raylib.WHITE)