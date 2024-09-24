import pyray

textures = {}

def load_texture_with_error_check(file_path):
    if file_path not in textures:
        texture = pyray.load_texture(file_path)
        if texture.id == 0:
            raise ValueError(f"Failed to load texture from {file_path}")
        textures[file_path] = texture
        print(textures)
    return textures[file_path]

