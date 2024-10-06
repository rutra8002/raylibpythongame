import pyray
import images
import math

class Gun:
    def __init__(self, name, damage, range, ammo):
        self.name = name
        self.damage = damage
        self.range = range
        self.ammo = ammo
        self.texture = images.load_texture_with_error_check(b"images/deagle.png")

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            return True
        return False

    def reload(self, ammo):
        self.ammo += ammo

    def draw(self, player_x, player_y, player_width, player_height, player_angle, player_vx, camera):
        mouse_position = pyray.get_mouse_position()
        world_position = pyray.get_screen_to_world_2d(mouse_position, camera.camera)
        angle = math.degrees(math.atan2(world_position.y - player_y, world_position.x - player_x))

        source_rect = pyray.Rectangle(0, 0, self.texture.width, self.texture.height)
        dest_rect = pyray.Rectangle(player_x, player_y, player_width, player_height)

        if player_vx < 0 and angle == player_angle or angle < -90 or angle > 90:
            source_rect.height = -self.texture.height

        pyray.draw_texture_pro(self.texture, source_rect, dest_rect, pyray.Vector2(player_width / 2, player_height / 2),
                               angle, pyray.WHITE)