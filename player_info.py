
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
        info_spacing = screen_height * 0.06
        font_size = int(screen_height * 0.03)
        health_bar_width = info_width * 0.8
        health_bar_height = screen_height * 0.04
        health_percentage = self.player.health / 100
        health_bar_fill_width = health_bar_width * health_percentage

        if health_percentage > 0.7:
            health_color = pyray.GREEN
        elif health_percentage > 0.4:
            health_color = pyray.YELLOW
        else:
            health_color = pyray.RED

        pyray.draw_rectangle(int(info_x - padding), int(info_y - padding), int(info_width + 2 * padding), int(info_height + 2 * padding), pyray.fade(pyray.BLACK, 0.5))
        pyray.draw_rectangle_lines(int(info_x - padding), int(info_y - padding), int(info_width + 2 * padding), int(info_height + 2 * padding), pyray.WHITE)

        health_text = f"Health: {self.player.health}"
        speed_text = f"Speed: {self.player.vx/50:.2f}mps, {self.player.vy/50:.2f}mps"

        pyray.draw_rectangle(int(info_x), int(info_y), int(health_bar_width), int(health_bar_height), pyray.GRAY)
        pyray.draw_rectangle(int(info_x), int(info_y), int(health_bar_fill_width), int(health_bar_height), health_color)
        pyray.draw_rectangle_lines(int(info_x), int(info_y), int(health_bar_width), int(health_bar_height), pyray.WHITE)
        text_x = info_x + (health_bar_width - pyray.measure_text(health_text, font_size)) / 2
        text_y = info_y + (health_bar_height - font_size) / 2
        pyray.draw_text_ex(pyray.get_font_default(), health_text, pyray.Vector2(int(text_x), int(text_y)), font_size, 2, pyray.WHITE)

        pyray.draw_text_ex(pyray.get_font_default(), speed_text, pyray.Vector2(int(info_x), int(info_y + info_spacing)), font_size, 2, pyray.WHITE)