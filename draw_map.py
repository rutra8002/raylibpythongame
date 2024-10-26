import pyray
import os
import json

from grapplinggun import GrapplingGun
from gun import Gun, DesertEagle
from map_loader import load_map, list_maps
from blocks.block import Block
from blocks.speedboostblock import SpeedBoostBlock
from blocks.jumpboostblock import JumpBoostBlock
from blocks.lavablock import LavaBlock
from player import Player
from enemy import Enemy  # Import Enemy
from button import Button

# Define block types
BLOCK_TYPES = {
    "Block": Block,
    "SpeedBoostBlock": SpeedBoostBlock,
    "JumpBoostBlock": JumpBoostBlock,
    "LavaBlock": LavaBlock,
    "Player": Player,
    "Enemy": Enemy
}

def snap_to_grid(x, y, grid_size=50):
    return (x // grid_size) * grid_size, (y // grid_size) * grid_size

def save_map(file_path, blocks, player, enemies):  # Add enemies parameter
    if isinstance(player.color, tuple):
        player_color = player.color
    else:
        player_color = (player.color.r, player.color.g, player.color.b, player.color.a)

    data = {
        "blocks": [],
        "enemies": [],
        "player": {
            "x": player.x,
            "y": player.y,
            "width": player.width,
            "height": player.height,
            "color": {
                "r": player_color[0],
                "g": player_color[1],
                "b": player_color[2],
                "a": player_color[3]
            },
            "inventory": [
                {"type": item.__class__.__name__, "range": item.range, "speed": item.speed, "ammo": item.ammo} if isinstance(item, GrapplingGun) else
                {"type": item.__class__.__name__, "damage": item.damage, "range": item.range, "ammo": item.ammo} if isinstance(item, Gun) else
                {"type": item.__class__.__name__, "damage": item.damage, "range": item.range, "ammo": item.ammo} if isinstance(item, DesertEagle) else
                {} for item in player.inventory.items
            ]
        }
    }
    for block in blocks:
        if isinstance(block.color, tuple):
            color = block.color
        else:
            color = (block.color.r, block.color.g, block.color.b, block.color.a)

        block_data = {
            "type": block.__class__.__name__,
            "width": block.width,
            "height": block.height,
            "x": block.x,
            "y": block.y,
            "color": {
                "r": color[0],
                "g": color[1],
                "b": color[2],
                "a": color[3]
            }
        }
        if isinstance(block, SpeedBoostBlock):
            block_data["speed"] = block.speed_boost
        elif isinstance(block, JumpBoostBlock):
            block_data["jump"] = block.jump_boost
        data["blocks"].append(block_data)

    for enemy in enemies:  # Save enemies
        if isinstance(enemy.color, tuple):
            color = enemy.color
        else:
            color = (enemy.color.r, enemy.color.g, enemy.color.b, enemy.color.a)

        enemy_data = {
            "height": enemy.height,
            "width": enemy.width,
            "x": enemy.x,
            "y": enemy.y,
            "color": {
                "r": color[0],
                "g": color[1],
                "b": color[2],
                "a": color[3]
            },
            "health": enemy.health
        }
        data["enemies"].append(enemy_data)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    return True

def text_input_dialog(title, message):
    input_text = ""
    while not pyray.window_should_close():
        pyray.begin_drawing()
        pyray.draw_rectangle(0, 0, 400, 100, pyray.LIGHTGRAY)
        pyray.draw_text(title, 10, 10, 20, pyray.DARKGRAY)
        pyray.draw_text(message, 10, 40, 20, pyray.DARKGRAY)
        pyray.draw_text(input_text, 10, 70, 20, pyray.DARKGRAY)
        pyray.end_drawing()

        key = pyray.get_key_pressed()
        if key == pyray.KeyboardKey.KEY_ENTER:
            return input_text
        elif key == pyray.KeyboardKey.KEY_BACKSPACE:
            input_text = input_text[:-1]
        elif key >= 32 and key <= 126:
            input_text += chr(key)

def edit_block_dialog(block):
    width_input = str(block.width)
    height_input = str(block.height)
    x_input = str(int(block.x))
    y_input = str(int(block.y))
    while not pyray.window_should_close():
        pyray.begin_drawing()
        pyray.draw_rectangle(0, 0, 200, 150, pyray.LIGHTGRAY)
        pyray.draw_text("Edit Block", 10, 10, 20, pyray.DARKGRAY)
        pyray.draw_text("Width:", 10, 40, 20, pyray.DARKGRAY)
        pyray.draw_text(width_input, 100, 40, 20, pyray.DARKGRAY)
        pyray.draw_text("Height:", 10, 70, 20, pyray.DARKGRAY)
        pyray.draw_text(height_input, 100, 70, 20, pyray.DARKGRAY)
        pyray.draw_text("X:", 10, 100, 20, pyray.DARKGRAY)
        pyray.draw_text(x_input, 100, 100, 20, pyray.DARKGRAY)
        pyray.draw_text("Y:", 10, 130, 20, pyray.DARKGRAY)
        pyray.draw_text(y_input, 100, 130, 20, pyray.DARKGRAY)
        pyray.end_drawing()

        key = pyray.get_key_pressed()
        if key == pyray.KeyboardKey.KEY_ENTER:
            block.width = int(float(width_input))
            block.height = int(float(height_input))
            block.x = int(float(x_input))
            block.y = int(float(y_input))
            return
        elif key == pyray.KeyboardKey.KEY_BACKSPACE:
            if pyray.get_mouse_y() < 60:
                width_input = width_input[:-1]
            elif pyray.get_mouse_y() < 90:
                height_input = height_input[:-1]
            elif pyray.get_mouse_y() < 120:
                x_input = x_input[:-1]
            else:
                y_input = y_input[:-1]
        elif key >= 32 and key <= 126:
            if pyray.get_mouse_y() < 60:
                width_input += chr(key)
            elif pyray.get_mouse_y() < 90:
                height_input += chr(key)
            elif pyray.get_mouse_y() < 120:
                x_input += chr(key)
            else:
                y_input += chr(key)

def main():
    # Initialize the window
    width, height = 1366, 768
    pyray.init_window(width, height, "Map Drawer")
    pyray.set_target_fps(60)

    # Initialize the camera
    camera = pyray.Camera2D(pyray.Vector2(0, 0), pyray.Vector2(0, 0), 0.0, 1.0)

    # Menu to choose between loading an existing map or creating a new one
    maps = list_maps('maps')
    selected_map = None
    creating_new_map = False

    # Variable to track popup display time
    popup_display_time = 0
    popup_message = ""

    # Create buttons for each type of GameObject
    block_button = Button(10, 10, 150, 40, "Block", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
    speedboost_button = Button(10, 60, 150, 40, "SpeedBoostBlock", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
    jumpboost_button = Button(10, 110, 150, 40, "JumpBoostBlock", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
    player_button = Button(10, 160, 150, 40, "Player", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
    lavablock_button = Button(10, 210, 150, 40, "LavaBlock", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
    enemy_button = Button(10, 260, 150, 40, "Enemy", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)  # Add Enemy button

    current_block_type = "Block"

    scroll_offset = 0

    while not pyray.window_should_close():
        if selected_map is None and not creating_new_map:
            scroll_offset += pyray.get_mouse_wheel_move() * 20

            pyray.begin_drawing()
            pyray.clear_background(pyray.RAYWHITE)
            pyray.draw_text("Select Map or Create New", int(width / 2 - 150), 100, 40, pyray.DARKGRAY)

            for i, map_name in enumerate(maps):
                if pyray.gui_button(pyray.Rectangle(width / 2 - 100, height / 2 + i * 60 + scroll_offset, 200, 50),
                                    map_name):
                    selected_map = map_name

            if pyray.gui_button(pyray.Rectangle(width / 2 - 100, height / 2 + len(maps) * 60 + scroll_offset, 200, 50),
                                "Create New Map"):
                creating_new_map = True

            pyray.end_drawing()
        else:
            if creating_new_map:
                blocks = []
                enemies = []  # Initialize enemies list
                player = None
            else:
                map_data = load_map(os.path.join('maps', selected_map))
                blocks = map_data['blocks']
                enemies = map_data['enemies']  # Load enemies
                player_data = map_data['player']
                player = Player(player_data['width'], player_data['height'], player_data['x'], player_data['y'], pyray.Color(player_data['color']['r'], player_data['color']['g'], player_data['color']['b'], player_data['color']['a']), None)

            while not pyray.window_should_close():
                # Update buttons
                block_button.update()
                speedboost_button.update()
                jumpboost_button.update()
                player_button.update()
                lavablock_button.update()
                enemy_button.update()

                # Handle button clicks
                if block_button.is_clicked:
                    current_block_type = "Block"
                elif speedboost_button.is_clicked:
                    current_block_type = "SpeedBoostBlock"
                elif jumpboost_button.is_clicked:
                    current_block_type = "JumpBoostBlock"
                elif player_button.is_clicked:
                    current_block_type = "Player"
                elif lavablock_button.is_clicked:
                    current_block_type = "LavaBlock"
                elif enemy_button.is_clicked:  # Handle Enemy button click
                    current_block_type = "Enemy"
                else:

                    if pyray.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT):
                        mouse_position = pyray.get_screen_to_world_2d(pyray.get_mouse_position(), camera)
                        x, y = snap_to_grid(mouse_position.x, mouse_position.y)
                        if current_block_type == "Block":
                            blocks.append(Block(50, 50, x, y, pyray.BLUE))
                        elif current_block_type == "SpeedBoostBlock":
                            blocks.append(SpeedBoostBlock(50, 50, x, y, pyray.GREEN, 800))
                        elif current_block_type == "JumpBoostBlock":
                            blocks.append(JumpBoostBlock(50, 50, x, y, pyray.YELLOW, 800))
                        elif current_block_type == "Player":
                            player = Player(50, 50, x, y, pyray.RED, None)
                        elif current_block_type == "LavaBlock":
                            blocks.append(LavaBlock(50, 50, x, y, pyray.ORANGE))
                        elif current_block_type == "Enemy":
                            enemies.append(Enemy(50, 50, x, y, pyray.RED, 100))

                    if pyray.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_RIGHT):
                        mouse_position = pyray.get_screen_to_world_2d(pyray.get_mouse_position(), camera)
                        x, y = snap_to_grid(mouse_position.x, mouse_position.y)
                        blocks = [block for block in blocks if not (block.x == x and block.y == y)]
                        enemies = [enemy for enemy in enemies if not (enemy.x == x and enemy.y == y)]  # Remove enemies
                        if player and player.x == x and player.y == y:
                            player = None

                    if pyray.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_MIDDLE):
                        mouse_position = pyray.get_screen_to_world_2d(pyray.get_mouse_position(), camera)
                        x, y = snap_to_grid(mouse_position.x, mouse_position.y)
                        for block in blocks:
                            if block.x <= x < block.x + block.width and block.y <= y < block.y + block.height:
                                edit_block_dialog(block)
                                break

                # Handle save shortcuts
                if pyray.is_key_down(pyray.KeyboardKey.KEY_LEFT_CONTROL) and pyray.is_key_pressed(pyray.KeyboardKey.KEY_S):
                    if pyray.is_key_down(pyray.KeyboardKey.KEY_LEFT_SHIFT) or selected_map is None or creating_new_map:
                        # Save As
                        new_map_name = text_input_dialog("Save As", "Enter new map name:")
                        if new_map_name:
                            save_map(os.path.join('maps', new_map_name + '.json'), blocks, player, enemies)  # Save enemies
                            selected_map = new_map_name + '.json'
                            creating_new_map = False
                            popup_message = "Map saved successfully!"
                            popup_display_time = 2  # Display for 2 seconds
                    else:
                        # Save
                        save_map(os.path.join('maps', selected_map), blocks, player, enemies)  # Save enemies
                        popup_message = "Map saved successfully!"
                        popup_display_time = 2  # Display for 2 seconds

                # Update camera position
                if pyray.is_key_down(pyray.KeyboardKey.KEY_RIGHT):
                    camera.target.x += 10
                if pyray.is_key_down(pyray.KeyboardKey.KEY_LEFT):
                    camera.target.x -= 10
                if pyray.is_key_down(pyray.KeyboardKey.KEY_DOWN):
                    camera.target.y += 10
                if pyray.is_key_down(pyray.KeyboardKey.KEY_UP):
                    camera.target.y -= 10

                # Start drawing
                pyray.begin_drawing()
                pyray.clear_background(pyray.RAYWHITE)

                pyray.begin_mode_2d(camera)

                # Draw grid
                start_x = int(camera.target.x) // 50 * 50
                end_x = int(camera.target.x + width+50) // 50 * 50
                start_y = int(camera.target.y) // 50 * 50
                end_y = int(camera.target.y + height+50) // 50 * 50

                for i in range(start_x, end_x + 50, 50):
                    pyray.draw_line(i, start_y, i, end_y, pyray.LIGHTGRAY)
                for j in range(start_y, end_y + 50, 50):
                    pyray.draw_line(start_x, j, end_x, j, pyray.LIGHTGRAY)

                # Draw each block
                for block in blocks:
                    block.draw()

                # Draw each enemy
                for enemy in enemies:
                    enemy.draw()

                # Draw player
                if player:
                    player.draw(None)

                pyray.end_mode_2d()

                # Draw UI
                block_button.draw()
                speedboost_button.draw()
                jumpboost_button.draw()
                player_button.draw()
                lavablock_button.draw()
                enemy_button.draw()  # Draw Enemy button

                pyray.draw_text(f"Current Block Type: {current_block_type}", 10, 310, 20, pyray.DARKGRAY)

                # Display popup message if needed
                if popup_display_time > 0:
                    pyray.draw_text(popup_message, width // 2 - 100, height // 2, 20, pyray.GREEN)
                    popup_display_time -= pyray.get_frame_time()

                # End drawing
                pyray.end_drawing()

            # Close the window
            pyray.close_window()
            break

if __name__ == "__main__":
    main()