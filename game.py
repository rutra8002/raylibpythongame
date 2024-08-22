import pyray
import json
from player import Player
from block import Block
from camera import Camera


WIDTH = 1366
HEIGHT = 768

def run_game():
    pyray.init_window(WIDTH, HEIGHT, "gmae")

    player = Player(50, 50, 100, 100, pyray.RED)
    blocks = [Block(50, 500, 100, 600, pyray.BLUE), Block(50, 500, 800, 600, pyray.BLUE), Block(500, 50, 500, 0, pyray.BLUE)]

    camera = Camera(WIDTH, HEIGHT, player.x + player.width / 2, player.y + player.height / 2, 0.05)

    while not pyray.window_should_close():
        delta_time = pyray.get_frame_time()

        camera.update_target(player.x + player.width / 2, player.y + player.height / 2)

        pyray.begin_drawing()
        pyray.clear_background(pyray.WHITE)

        camera.begin_mode()

        player.movement(delta_time, blocks)
        player.draw()

        for block in blocks:
            block.draw()

        camera.end_mode()

        pyray.draw_fps(10, 10)

        pyray.end_drawing()

    pyray.close_window()