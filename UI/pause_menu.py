import pyray
import shaders
from UI.button import Button
from particles import ParticleSystem
import raylib
import random

class PauseMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.is_visible = False
        self.resume_button = Button(width / 2 - 100, height / 2 - 50, 200, 50, "Resume", 20, pyray.WHITE, pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)
        self.settings_button = Button(width / 2 - 100, height / 2 + 10, 200, 50, "Settings", 20, pyray.WHITE, pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)
        self.main_menu_button = Button(width / 2 - 100, height / 2 + 70, 200, 50, "Main Menu", 20, pyray.WHITE, pyray.DARKGRAY, pyray.GRAY, pyray.LIGHTGRAY)
        self.particle_system = ParticleSystem()

    def toggle(self):
        self.is_visible = not self.is_visible

    def render(self):
        if self.is_visible:
            pyray.begin_drawing()

            if shaders.shaders_enabled:
                pyray.begin_shader_mode(shaders.shaders["main_menu_background"])

                time_value = pyray.ffi.new("float *", raylib.GetTime())
                raylib.SetShaderValue(shaders.shaders["main_menu_background"],
                                      raylib.GetShaderLocation(shaders.shaders["main_menu_background"], b"time"),
                                      time_value, raylib.SHADER_UNIFORM_FLOAT)

                resolution_value = pyray.ffi.new("float[2]", [self.width, self.height])
                raylib.SetShaderValue(shaders.shaders["main_menu_background"],
                                      raylib.GetShaderLocation(shaders.shaders["main_menu_background"], b"resolution"),
                                      resolution_value, raylib.SHADER_UNIFORM_VEC2)

                pyray.draw_rectangle(0, 0, self.width, self.height, pyray.WHITE)
                pyray.end_shader_mode()
            else:
                pyray.clear_background(pyray.BLACK)
                if random.randint(0, 10) > 8:
                    self.particle_system.add_particle(
                        random.uniform(0, self.width),
                        random.uniform(0, self.height),
                        random.uniform(-1, 1),
                        random.uniform(-1, 1),
                        random.randint(10, 50),
                        20,
                        3,
                        (random.randint(1, 150), random.randint(1, 150), random.randint(1, 150),
                         random.randint(50, 200)),
                        'circle',
                        None
                    )

            text = "Pause Menu"
            text_width = pyray.measure_text(text, 40)
            pyray.draw_text(text, int((self.width - text_width) / 2), int(self.height * 0.1), 40, pyray.WHITE)

            self.resume_button.rect.x = self.width / 2 - self.resume_button.rect.width / 2
            self.resume_button.rect.y = self.height / 2 - self.resume_button.rect.height - 10
            self.resume_button.update()
            self.resume_button.draw()

            self.settings_button.rect.x = self.width / 2 - self.settings_button.rect.width / 2
            self.settings_button.rect.y = self.height / 2
            self.settings_button.update()
            self.settings_button.draw()

            self.main_menu_button.rect.x = self.width / 2 - self.main_menu_button.rect.width / 2
            self.main_menu_button.rect.y = self.height / 2 + self.main_menu_button.rect.height + 10
            self.main_menu_button.update()
            self.main_menu_button.draw()

            pyray.end_drawing()