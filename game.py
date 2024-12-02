import os
import sys

import pyray
import raylib
from player import Player
from camera import Camera
from particles import ParticleSystem
from UI.main_menu import MainMenu
from UI.pause_menu import PauseMenu
from UI.death_menu import DeathMenu
from map_loader import load_map


class Game:
    def __init__(self, width=1366, height=768, fps=60):
        self.width = width
        self.height = height
        self.fps = fps
        self.player = None
        self.blocks = []
        self.enemies = []
        self.camera = None
        self.weapon_particle_system = ParticleSystem()
        self.main_menu = MainMenu(width, height)
        self.pause_menu = PauseMenu(width, height)
        self.death_menu = DeathMenu(width, height)
        self.main_menu.load_maps('maps')
        self.intro_zooming = True

    def run(self):
        raylib.SetConfigFlags(raylib.FLAG_MSAA_4X_HINT)
        pyray.init_window(self.width, self.height, "game")
        if self.fps is not None:
            pyray.set_target_fps(self.fps)
        pyray.set_exit_key(pyray.KeyboardKey.KEY_NULL)
        while not pyray.window_should_close():
            delta_time = pyray.get_frame_time()
            if pyray.is_key_pressed(pyray.KeyboardKey.KEY_ESCAPE):
                self.pause_menu.toggle()
            if self.main_menu.show_menu or self.main_menu.show_map_selection:
                self.main_menu.render()
            elif self.pause_menu.is_visible:
                self.pause_menu.render()
                if self.pause_menu.resume_button.is_clicked:
                    self.pause_menu.toggle()
                if self.pause_menu.main_menu_button.is_clicked:
                    self.blocks = []
                    self.player = None
                    self.pause_menu.toggle()
                    self.main_menu.show_menu = True
            elif self.death_menu.is_visible:
                self.death_menu.render()
                if self.death_menu.retry_button.is_clicked:
                    self.reset_game()
                if self.death_menu.main_menu_button.is_clicked:
                    self.blocks = []
                    self.player = None
                    self.death_menu.toggle()
                    self.main_menu.show_menu = True
            else:
                if not self.blocks and self.main_menu.selected_map:
                    map_data = load_map(os.path.join('maps', self.main_menu.selected_map))
                    self.blocks = map_data['blocks']
                    self.enemies = map_data['enemies']
                    player_data = map_data['player']
                    self.player = Player(
                        player_data['width'], player_data['height'], player_data['x'], player_data['y'],
                        pyray.Color(player_data['color']['r'], player_data['color']['g'], player_data['color']['b'], player_data['color']['a']),
                        self.weapon_particle_system,
                        inventory_data=player_data.get('inventory', [])
                    )
                    self.camera = Camera(self.width, self.height, self.player.x + self.player.width / 2, self.player.y + self.player.height / 2, 3, initial_zoom=2.0)
                    self.intro_zooming = True
                self.update(delta_time)
                self.render()
        pyray.close_window()
        sys.exit()

    def update(self, delta_time):
        self.camera.update_target(self.player.x + self.player.width / 2, self.player.y + self.player.height / 2,
                                  delta_time)
        if self.intro_zooming:
            self.camera.zoom_intro(delta_time)
            if abs(self.camera.camera.zoom - self.camera.target_zoom) < 0.01:
                self.intro_zooming = False
        else:
            self.camera.adjust_zoom(self.player.vx, delta_time)
        self.player.movement(delta_time, self.blocks, self.camera)
        for enemy in self.enemies:
            enemy.movement(delta_time, self.blocks, self.player)
        self.weapon_particle_system.update(delta_time, self.player, self.enemies)
        self.check_player_health()
        self.enemies = [enemy for enemy in self.enemies if not enemy.take_damage(0)]

    def render(self):
        pyray.begin_drawing()
        pyray.clear_background(pyray.BLACK)
        self.camera.begin_mode()
        self.player.draw(self.camera)
        for block in self.blocks:
            block.draw()
        for enemy in self.enemies:
            enemy.draw()
        self.weapon_particle_system.draw()
        self.camera.end_mode()
        raylib.DrawFPS(10, 10)
        raylib.DrawText(b"Player", 10, 30, 10, raylib.RED)
        for parameter in self.player.__dict__:
            text = f"{parameter}: {self.player.__dict__[parameter]}".encode('utf-8')
            raylib.DrawText(text, 10, 40 + 10 * list(self.player.__dict__.keys()).index(parameter), 10, pyray.WHITE)
        self.player.inventory.render(self.width, self.height)
        pyray.end_drawing()

    def check_player_health(self):
        if self.player.health <= 0:
            self.death_menu.toggle()

    def reset_game(self):
        map_data = load_map(os.path.join('maps', self.main_menu.selected_map))
        self.blocks = map_data['blocks']
        self.enemies = map_data['enemies']
        player_data = map_data['player']
        self.player = Player(player_data['width'], player_data['height'], player_data['x'], player_data['y'],
                             pyray.Color(player_data['color']['r'], player_data['color']['g'],
                                         player_data['color']['b'], player_data['color']['a']),
                             self.weapon_particle_system, inventory_data=player_data.get('inventory', []))
        self.camera = Camera(self.width, self.height, self.player.x + self.player.width / 2,
                             self.player.y + self.player.height / 2, 3, initial_zoom=2.0)
        self.intro_zooming = True
        self.main_menu.show_menu = False
        self.death_menu.toggle()

if __name__ == "__main__":
    game = Game()
    game.run()