import pyray
import json
from player import Player
from block import Block
from camera import Camera
from pypresence import Presence
from ai import AI
import time


def run_game(width=1366, height=768):
    pyray.init_window(width, height, "game")

    player = Player(50, 50, 100, 100, pyray.RED, 70)
    ai = AI(50, 50, 200, 200, pyray.GREEN)
    blocks = [Block(50, 500, 100, 600, pyray.BLUE),
              Block(50, 500, 800, 600, pyray.BLUE),
              Block(50, 500, 1500, 600, pyray.BLUE),
              Block(50, 100, 650, 450, pyray.BLUE),
              Block(500, 50, 500, 0, pyray.BLUE),
              Block(500, 200, 850, 0, pyray.BLUE)]

    camera = Camera(width, height, player.x + player.width / 2, player.y + player.height / 2, 0.05)

    while not pyray.window_should_close():
        delta_time = pyray.get_frame_time()

        camera.update_target(player.x + player.width / 2, player.y + player.height / 2)

        pyray.begin_drawing()
        pyray.clear_background(pyray.WHITE)

        camera.begin_mode()

        player.movement(delta_time, blocks)
        player.draw()

        ai.update(delta_time, player, blocks)
        ai.draw()

        for block in blocks:
            block.draw()

        camera.end_mode()

        pyray.draw_fps(10, 10)

        for parameter in player.__dict__:
            pyray.draw_text(parameter + ": " + str(player.__dict__[parameter]), 10, 30 + 10 * list(player.__dict__.keys()).index(parameter), 10, pyray.BLACK)

        for i, block in enumerate(blocks):
            pyray.draw_text("Block "+ str(i), 200 * i + 200, 20, 10,
                            pyray.BLACK)
            for parameter in block.__dict__:
                pyray.draw_text(parameter + ": " + str(block.__dict__[parameter]), 200*i+200, 30 + 10 * list(block.__dict__.keys()).index(parameter), 10, pyray.BLACK)

        pyray.end_drawing()

    pyray.close_window()