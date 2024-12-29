import pyray
import images
import math

class Gun:
    def __init__(self, damage, range, speed, ammo, particle_system):
        self.name = self.__class__.__name__
        self.damage = damage
        self.range = range
        self.ammo = ammo
        self.speed = speed
        self.texture = images.textures["deagle"]
        self.particle_system = particle_system

    def shoot(self, player_x, player_y, player_width, player_height, camera):
        if self.ammo > 0:
            self.ammo -= 1

            # Calculate the particle start position outside the player
            particle_x = player_x + player_width // 2
            particle_y = player_y + player_height // 2

            mouse_position = pyray.get_mouse_position()
            world_position = pyray.get_screen_to_world_2d(mouse_position, camera.camera)
            mouse_x, mouse_y = world_position.x, world_position.y

            direction_x = mouse_x - particle_x
            direction_y = mouse_y - particle_y
            length = math.sqrt(direction_x ** 2 + direction_y ** 2)
            direction_x /= length
            direction_y /= length

            offset_distance = player_width
            particle_x += direction_x * offset_distance
            particle_y += direction_y * offset_distance

            self.particle_system.add_particle(
                particle_x, particle_y, direction_x, direction_y, self.speed, 1, 5, (255, 255, 0, 255), 'circle', self.damage
            )
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

class DesertEagle(Gun):
    def __init__(self, damage, range, speed, ammo, particle_system):
        super().__init__(
            damage=damage,
            range=range,
            speed=speed,
            ammo=ammo,
            particle_system=particle_system
        )
        self.texture = images.textures["deagle"]