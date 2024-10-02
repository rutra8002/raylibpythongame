import pyray
import images
import math

class GrapplingGun:
    def __init__(self, range, speed, ammo=10, name="Grappling Gun"):
        self.range = range
        self.speed = speed
        self.ammo = ammo
        self.is_grappling = False
        self.target_x = None
        self.target_y = None
        self.name = name
        self.texture = images.load_texture_with_error_check("images/grappling_gun.png")

    def __str__(self):
        return f"range={self.range}, speed={self.speed}, ammo={self.ammo}"

    def shoot(self, target_x, target_y, blocks):
        if self.is_grappling:
            self.reset()
            if self.ammo <= 0:
                return
        else:
            if self.ammo <= 0:
                return
            self.is_grappling = True
            nearest_edge = self.find_nearest_edge(target_x, target_y, blocks)
            if nearest_edge:
                self.target_x, self.target_y = nearest_edge
                self.ammo -= 1  # Decrease ammo

    def find_nearest_edge(self, target_x, target_y, blocks):
        def closest_point_on_segment(px, py, ax, ay, bx, by):
            abx, aby = bx - ax, by - ay
            apx, apy = px - ax, py - ay
            ab_ap_product = abx * apx + aby * apy
            ab_ab_product = abx * abx + aby * aby
            t = ab_ap_product / ab_ab_product
            t = max(0, min(1, t))
            return ax + t * abx, ay + t * aby

        nearest_point = None
        min_distance = float('inf')
        for block in blocks:
            edges = [
                (block.x, block.y, block.x + block.width, block.y),  # top edge
                (block.x, block.y, block.x, block.y + block.height),  # left edge
                (block.x + block.width, block.y, block.x + block.width, block.y + block.height),  # right edge
                (block.x, block.y + block.height, block.x + block.width, block.y + block.height)  # bottom edge
            ]
            for ax, ay, bx, by in edges:
                closest_x, closest_y = closest_point_on_segment(target_x, target_y, ax, ay, bx, by)
                distance = ((target_x - closest_x) ** 2 + (target_y - closest_y) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    nearest_point = (closest_x, closest_y)
        return nearest_point

    def reset(self):
        self.is_grappling = False
        self.target_x = None
        self.target_y = None

    def draw(self, player_x, player_y, player_width, player_height, player_angle, player_vx, camera):
        if self.is_grappling and self.target_x is not None and self.target_y is not None:
            pyray.draw_line(int(player_x), int(player_y), int(self.target_x),
                            int(self.target_y), pyray.RED)

        if self.is_grappling and self.target_x is not None and self.target_y is not None:
            angle = math.degrees(math.atan2(self.target_y - player_y, self.target_x - player_x))
        else:
            mouse_position = pyray.get_mouse_position()
            world_position = pyray.get_screen_to_world_2d(mouse_position, camera.camera)
            angle = math.degrees(math.atan2(world_position.y - player_y, world_position.x - player_x))

        self.source_rect = pyray.Rectangle(0, 0, self.texture.width, self.texture.height)
        dest_rect = pyray.Rectangle(player_x, player_y, player_width, player_height)

        if player_vx < 0 and angle == player_angle or angle < -90 or angle > 90:
            self.source_rect.height = -self.texture.height

        pyray.draw_texture_pro(self.texture, self.source_rect, dest_rect, pyray.Vector2(player_width / 2, player_height / 2),
                               angle, pyray.WHITE)

    def update_position(self, player_x, player_y, vx, vy, delta_time):
        if self.is_grappling and self.target_x is not None and self.target_y is not None:
            direction_x = self.target_x - player_x
            direction_y = self.target_y - player_y
            distance = (direction_x ** 2 + direction_y ** 2) ** 0.5
            if distance < self.speed * delta_time:
                return vx, vy, True
            else:
                direction_x /= distance
                direction_y /= distance
                new_vx = vx + 8 * direction_x * self.speed * delta_time
                new_vy = vy + 8 * direction_y * self.speed * delta_time
                return new_vx, new_vy, False
        return vx, vy, False