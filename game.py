import os
import pyray

from player import Player
from camera import Camera
from particles import ParticleSystem
from main_menu import MainMenu
from map_loader import load_map

class Game:
    def __init__(self, width=1366, height=768, fps=60):
        self.width = width
        self.height = height
        self.fps = fps
        self.player = None
        self.blocks = []
        self.camera = None
        self.weapon_particle_system = ParticleSystem()
        self.main_menu = MainMenu(width, height)
        self.main_menu.load_maps('maps')

    def run(self):
        pyray.init_window(self.width, self.height, "game")
        if self.fps is not None:
            pyray.set_target_fps(self.fps)
        pyray.set_exit_key(pyray.KeyboardKey.KEY_NULL)
        while not pyray.window_should_close():
            delta_time = pyray.get_frame_time()
            if self.main_menu.show_menu or self.main_menu.show_map_selection:
                self.main_menu.render()
            else:
                if not self.blocks and self.main_menu.selected_map:
                    map_data = load_map(os.path.join('maps', self.main_menu.selected_map))
                    self.blocks = map_data['blocks']
                    player_data = map_data['player']
                    self.player = Player(player_data['width'], player_data['height'], player_data['x'], player_data['y'], pyray.Color(player_data['color']['r'], player_data['color']['g'], player_data['color']['b'], player_data['color']['a']), self.weapon_particle_system)
                    self.camera = Camera(self.width, self.height, self.player.x + self.player.width / 2, self.player.y + self.player.height / 2, 3)
                self.update(delta_time)
                self.render()
        pyray.close_window()

    def update(self, delta_time):
        self.camera.update_target(self.player.x + self.player.width / 2, self.player.y + self.player.height / 2, delta_time)
        self.camera.adjust_zoom(self.player.vx, delta_time)
        self.player.movement(delta_time, self.blocks, self.camera)


        self.weapon_particle_system.update(delta_time)

    def render(self):
        pyray.begin_drawing()
        pyray.clear_background(pyray.BLACK)
        self.camera.begin_mode()
        self.player.draw(self.camera)
        for block in self.blocks:
            block.draw()
        self.weapon_particle_system.draw()
        self.camera.end_mode()
        pyray.draw_fps(10, 10)
        pyray.draw_text("Player", 10, 30, 10, pyray.RED)
        for parameter in self.player.__dict__:
            pyray.draw_text(parameter + ": " + str(self.player.__dict__[parameter]), 10,
                            40 + 10 * list(self.player.__dict__.keys()).index(parameter), 10, pyray.WHITE)
        self.player.inventory.render(self.width, self.height)
        pyray.end_drawing()


if __name__ == "__main__":
    game = Game()
    game.run()