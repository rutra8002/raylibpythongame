import pyray
import json
from player import Player
from block import Block


WIDTH = 1366
HEIGHT = 768

def run_game():
    pyray.init_window(WIDTH, HEIGHT, "gmae")

    player = Player(50, 50, 100, 100, pyray.RED)

    blocks = [Block(50, 500, 100, 600, pyray.BLUE), Block(50, 500, 800, 600, pyray.BLUE), Block(500, 50, 500, 0, pyray.BLUE)]

    camera = pyray.Camera2D()
    camera.target = pyray.Vector2(player.x + player.width / 2, player.y + player.height / 2)
    camera.offset = pyray.Vector2(WIDTH / 2, HEIGHT / 2)
    camera.rotation = 0.0
    camera.zoom = 1.0

    while not pyray.window_should_close():
        delta_time = pyray.get_frame_time()

        camera.target = pyray.Vector2(player.x + player.width / 2, player.y + player.height / 2)

        pyray.begin_drawing()
        pyray.clear_background(pyray.WHITE)

        pyray.begin_mode_2d(camera)

        player.movement(delta_time, blocks)
        player.draw()

        for block in blocks:
            block.draw()

        pyray.end_mode_2d()

        pyray.draw_fps(10, 10)

        pyray.end_drawing()

    pyray.close_window()