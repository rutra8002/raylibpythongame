
import pyray

class PlayerInfo:
    def __init__(self, player):
        self.player = player

    def render(self, screen_width, screen_height):
        info_x = screen_width * 0.01
        info_y = screen_height * 0.85
        info_width = screen_width * 0.22
        info_height = screen_height * 0.1
        padding = screen_width * 0.01
        info_spacing = screen_height * 0.04
        font_size = int(screen_height * 0.03)

        pyray.draw_rectangle(int(info_x - padding), int(info_y - padding), int(info_width + 2 * padding), int(info_height + 2 * padding), pyray.fade(pyray.BLACK, 0.5))
        pyray.draw_rectangle_lines(int(info_x - padding), int(info_y - padding), int(info_width + 2 * padding), int(info_height + 2 * padding), pyray.WHITE)

        health_text = f"Health: {self.player.health}"
        speed_text = f"Speed: {self.player.vx/50:.2f}mps, {self.player.vy/50:.2f}mps"

        pyray.draw_text(health_text, int(info_x), int(info_y), font_size, pyray.WHITE)
        pyray.draw_text(speed_text, int(info_x), int(info_y + info_spacing), font_size, pyray.WHITE)