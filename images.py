import raylib

textures = {}

def load_texture_with_error_check(file_path):
    if file_path not in textures:
        texture = raylib.LoadTexture(file_path)
        if texture.id == 0:
            raise ValueError(f"Failed to load texture from {file_path}")
        textures[file_path] = texture
        print(textures)
    return textures[file_path]

def load_textures():
    try:
        textures["block"] = load_texture_with_error_check(b"images/block.png")
        textures["jump"] = load_texture_with_error_check(b"images/jump.png")
        textures["speed"] = load_texture_with_error_check(b"images/speeed.png")
        textures["player"] = load_texture_with_error_check(b"images/player.png")
        textures["deagle"] = load_texture_with_error_check(b"images/deagle.png")
        textures["enemy"] = load_texture_with_error_check(b"images/enemy.png")
        textures["grappling_gun"] = load_texture_with_error_check(b"images/grappling_gun.png")
    except Exception as e:
        raise e

