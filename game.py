import os
import sys
import time

import pyray
import raylib
from entities.player import Player
from camera import Camera
from particles import ParticleSystem
from UI.main_menu import MainMenu
from UI.pause_menu import PauseMenu
from UI.death_menu import DeathMenu
from map_loader import load_map
from UI.player_info import PlayerInfo
import images
import sounds
import shaders


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
        self.player_info = None
        self.show_settings_from_pause = False

    def show_loading_screen(self, message):
        pyray.begin_drawing()
        pyray.clear_background(pyray.Color(0, 0, 0, 255))
        raylib.DrawText(message.encode('utf-8'), self.width // 2 - 100, self.height // 2, 20, raylib.WHITE)
        pyray.end_drawing()

    def run(self):
        raylib.SetConfigFlags(raylib.FLAG_MSAA_4X_HINT)
        raylib.InitWindow(self.width, self.height, b"Jeff the Grappler")
        self.render_texture = pyray.load_render_texture(self.width, self.height)
        if self.fps is not None:
            pyray.set_target_fps(self.fps)
        pyray.set_exit_key(pyray.KeyboardKey.KEY_NULL)

        self.show_loading_screen("Compiling Sounds...")
        sounds.load_sounds()
        self.show_loading_screen("Compiling Textures...")
        images.load_textures()
        self.show_loading_screen("Compiling Shaders...")
        shaders.load_shaders()

        pyray.play_music_stream(sounds.soundes["music"])
        while not pyray.window_should_close():
            start_time = time.time()
            pyray.update_music_stream(sounds.soundes["music"])
            if pyray.is_key_pressed(pyray.KeyboardKey.KEY_ESCAPE):
                self.pause_menu.toggle()
            if self.main_menu.show_menu or self.main_menu.show_map_selection or self.main_menu.show_settings:
                self.main_menu.render()
                self.update_resolution()
            elif self.pause_menu.is_visible:
                self.pause_menu.render()
                if self.pause_menu.resume_button.is_clicked:
                    self.pause_menu.toggle()
                if self.pause_menu.settings_button.is_clicked:
                    self.pause_menu.toggle()
                    self.show_settings_from_pause = True
                    self.main_menu.show_settings = True
                    self.main_menu.opened_from_pause_menu = True  # Set flag
                if self.pause_menu.main_menu_button.is_clicked:
                    self.blocks = []
                    self.player = None
                    self.pause_menu.toggle()
                    self.main_menu.show_menu = True
            elif self.show_settings_from_pause:
                self.main_menu.render()
                if not self.main_menu.show_settings:
                    self.show_settings_from_pause = False
                    self.pause_menu.toggle()
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
                if self.player:
                    self.player_info = PlayerInfo(self.player)
                if not self.blocks and self.main_menu.selected_map:
                    map_data = load_map(os.path.join('maps', self.main_menu.selected_map))
                    self.blocks = map_data['blocks']
                    self.enemies = map_data['enemies']
                    player_data = map_data['player']
                    self.player = Player(
                        player_data['width'], player_data['height'], player_data['x'], player_data['y'],
                        pyray.Color(player_data['color']['r'], player_data['color']['g'], player_data['color']['b'],
                                    player_data['color']['a']),
                        self.weapon_particle_system,
                        inventory_data=player_data.get('inventory', [])
                    )
                    self.camera = Camera(self.width, self.height, self.player.x + self.player.width / 2,
                                         self.player.y + self.player.height / 2, 3, initial_zoom=2.0)
                    self.intro_zooming = True
                self.update(delta_time)
                self.render()
            end_time = time.time()
            delta_time = end_time - start_time
        pyray.close_window()
        sys.exit()

    def update_resolution(self):
        if self.width != pyray.get_screen_width() or self.height != pyray.get_screen_height():
            self.width = pyray.get_screen_width()
            self.height = pyray.get_screen_height()
            self.render_texture = pyray.load_render_texture(self.width, self.height)
            self.main_menu.width = self.width
            self.main_menu.height = self.height
            self.pause_menu.width = self.width
            self.pause_menu.height = self.height
            self.death_menu.width = self.width
            self.death_menu.height = self.height
            if self.camera:
                self.camera.width = self.width
                self.camera.height = self.height

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
        self.weapon_particle_system.update(delta_time, self.player, self.enemies, self.blocks)
        self.check_player_health()
        self.enemies = [enemy for enemy in self.enemies if not enemy.take_damage(0)]


    def render(self):
        # Render the scene to the texture
        pyray.begin_texture_mode(self.render_texture)
        pyray.clear_background(pyray.Color(0, 0, 0, 255))

        if shaders.shaders_enabled:
            pyray.begin_shader_mode(shaders.shaders["background"])

            time_value = pyray.ffi.new("float *", raylib.GetTime())
            raylib.SetShaderValue(shaders.shaders["background"],
                                  raylib.GetShaderLocation(shaders.shaders["background"], b"time"),
                                  time_value, raylib.SHADER_UNIFORM_FLOAT)

            resolution_value = pyray.ffi.new("float[2]", [self.width, self.height])
            raylib.SetShaderValue(shaders.shaders["background"],
                                  raylib.GetShaderLocation(shaders.shaders["background"], b"resolution"),
                                  resolution_value, raylib.SHADER_UNIFORM_VEC2)

            pyray.draw_rectangle(0, 0, self.width, self.height, pyray.WHITE)
            pyray.end_shader_mode()
        else:
            pyray.draw_rectangle_gradient_v(0, 0, self.width, self.height, pyray.Color(0, 0, 88, 255),
                                            pyray.Color(0, 0, 0, 255))

        self.camera.begin_mode()
        self.player.draw(self.camera)
        for block in self.blocks:
            if block.__class__.__name__ == "LavaBlock":
                block.draw(self.camera)
            else:
                block.draw()
        for enemy in self.enemies:
            enemy.draw(self.player)
        self.weapon_particle_system.draw()
        self.camera.end_mode()

        pyray.end_texture_mode()

        # Apply bloom shader to the rendered texture
        pyray.clear_background(pyray.Color(0, 0, 0, 255))
        if shaders.shaders_enabled:
            pyray.begin_shader_mode(shaders.shaders["bloom"])
            pyray.draw_texture_rec(self.render_texture.texture, pyray.Rectangle(0, 0, self.width, -self.height),
                                   pyray.Vector2(0, 0), pyray.WHITE)
            pyray.end_shader_mode()
        else:
            pyray.draw_texture_rec(self.render_texture.texture, pyray.Rectangle(0, 0, self.width, -self.height),
                                   pyray.Vector2(0, 0), pyray.WHITE)

        raylib.DrawFPS(10, 10)
        raylib.DrawText(b"Player", 10, 30, 10, raylib.RED)
        for parameter in self.player.__dict__:
            text = f"{parameter}: {self.player.__dict__[parameter]}".encode('utf-8')
            raylib.DrawText(text, 10, 40 + 10 * list(self.player.__dict__.keys()).index(parameter), 10, pyray.WHITE)
        self.player.inventory.render(self.width, self.height)
        if self.player_info:
            self.player_info.render(self.width, self.height)

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