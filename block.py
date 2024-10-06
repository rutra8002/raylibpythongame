import raylib
from gameobject import GameObject

class Block(GameObject):
    def __init__(self, height, width, x, y, color):
        super().__init__(height, width, x, y, color)
        self.texture = raylib.LoadTexture(b"images/block.png")
        if self.texture.id == 0:
            raise ValueError("Failed to load texture")

    def draw(self):
        for i in range(0, self.width, self.texture.width):
            for j in range(0, self.height, self.texture.height):
                raylib.DrawTexture(self.texture, int(self.x + i), int(self.y + j), raylib.WHITE)