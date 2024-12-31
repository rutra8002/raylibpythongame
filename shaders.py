import raylib

shaders = {}

def load_shader_with_error_check(vs_path, fs_path):
    if fs_path not in shaders:
        shader = raylib.LoadShader(vs_path, fs_path)
        if shader.id == 0:
            raise ValueError(f"Failed to load shader from {fs_path}")
        shaders[fs_path] = shader
    return shaders[fs_path]

def load_shaders():
    try:
        shaders["bloom"] = load_shader_with_error_check(b"", b"shaders/bloom.fs")
        shaders["lava"] = load_shader_with_error_check(b"", b"shaders/lava.fs")
    except Exception as e:
        raise e