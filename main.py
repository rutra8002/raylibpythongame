import pyray
import json
import player
import block


WIDTH = 1366
HEIGHT = 768

pyray.init_window(WIDTH, HEIGHT, "gmae")

player = player.Player(50, 50, 100, 100, pyray.RED)

blocks = [block.Block(50, 500, 100, 600, pyray.BLUE), block.Block(50, 500, 800, 600, pyray.BLUE), block.Block(500, 50, 500, 0, pyray.BLUE)]


while not pyray.window_should_close():
    delta_time = pyray.get_frame_time()

    pyray.begin_drawing()
    pyray.clear_background(pyray.WHITE)

    player.movement(delta_time, blocks)
    player.draw()


    for block in blocks:
        block.draw()

    pyray.draw_fps(10, 10)

    pyray.end_drawing()

pyray.close_window()