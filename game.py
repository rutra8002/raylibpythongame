import random
import logging
import pyray
from player import Player
from block import Block
from camera import Camera
from particles import ParticleSystem

logging.basicConfig(filename='game_errors.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

class Game:
    def __init__(self, width=1366, height=768):
        self.width = width
        self.height = height
        self.player = Player(50, 50, 100, 100, pyray.RED, 70)
        self.blocks = [Block(50, 500, 100, 600, pyray.BLUE),
                       Block(50, 500, 800, 600, pyray.BLUE),
                       Block(50, 500, 1500, 600, pyray.BLUE),
                       Block(50, 100, 650, 500, pyray.BLUE),
                       Block(500, 50, 500, 0, pyray.BLUE),
                       Block(500, 200, 850, 0, pyray.BLUE)]
        self.camera = Camera(width, height, self.player.x + self.player.width / 2, self.player.y + self.player.height / 2, 0.05)
        self.particle_system = ParticleSystem()

    def run(self):
        try:
            pyray.init_window(self.width, self.height, "game")
            while not pyray.window_should_close():
                delta_time = pyray.get_frame_time()
                self.update(delta_time)
                self.render()
            pyray.close_window()
        except Exception as e:
            logging.error("An error occurred in the game loop", exc_info=True)

    def update(self, delta_time):
        self.camera.update_target(self.player.x + self.player.width / 2, self.player.y + self.player.height / 2)
        self.player.movement(delta_time, self.blocks)
        if pyray.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT):
            mouse_x, mouse_y = pyray.get_mouse_x(), pyray.get_mouse_y()
            for _ in range(10):
                vx, vy = random.uniform(-1, 1), random.uniform(-1, 1)
                self.pparticle_system.add_particle(mouse_x, mouse_y, vx, vy, 100, 2, 5, (255, 0, 0, 255), 'circle')
        self.particle_system.update(delta_time)

    def render(self):
        pyray.begin_drawing()
        pyray.clear_background(pyray.WHITE)
        self.camera.begin_mode()
        self.player.draw()
        for block in self.blocks:
            block.draw()
        self.particle_system.draw()
        self.camera.end_mode()
        pyray.draw_fps(10, 10)
        for parameter in self.player.__dict__:
            pyray.draw_text(parameter + ": " + str(self.player.__dict__[parameter]), 10,
                            30 + 10 * list(self.player.__dict__.keys()).index(parameter), 10, pyray.BLACK)
        for i, block in enumerate(self.blocks):
            pyray.draw_text("Block " + str(i), 200 * i + 200, 20, 10, pyray.BLACK)
            for parameter in block.__dict__:
                pyray.draw_text(parameter + ": " + str(block.__dict__[parameter]), 200 * i + 200,
                                30 + 10 * list(block.__dict__.keys()).index(parameter), 10, pyray.BLACK)
        pyray.end_drawing()
