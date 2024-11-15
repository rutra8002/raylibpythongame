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
                {"type": item.__class__.__name__, "damage": item.damage, "range": item.range, "ammo": item.ammo, "speed": item.speed} if isinstance(item, Gun) else
                {"type": item.__class__.__name__, "damage": item.damage, "range": item.range, "ammo": item.ammo, "speed": item.speed} if isinstance(item, DesertEagle) else
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

def edit_inventory_dialog(player):
    inventory_items = [item.__class__.__name__ for item in player.inventory.items]

    add_grappling_gun_button = Button(10, 370, 200, 40, "Add Grappling Gun", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
    add_gun_button = Button(220, 370, 200, 40, "Add Gun", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
    add_desert_eagle_button = Button(430, 370, 200, 40, "Add Desert Eagle", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)

    while not pyray.window_should_close():
        pyray.begin_drawing()
        pyray.clear_background(pyray.LIGHTGRAY)
        pyray.draw_text("Edit Inventory", 10, 10, 20, pyray.DARKGRAY)

        for i, item_name in enumerate(inventory_items):
            item_button = Button(10, 40 + i * 30, 200, 30, item_name, 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
            item_button.update()
            item_button.draw()
            if item_button.is_clicked:
                edit_weapon_dialog(player, i, inventory_items)

        add_grappling_gun_button.update()
        add_gun_button.update()
        add_desert_eagle_button.update()

        add_grappling_gun_button.draw()
        add_gun_button.draw()
        add_desert_eagle_button.draw()

        pyray.end_drawing()

        if add_grappling_gun_button.is_clicked:
            player.inventory.add_item(GrapplingGun(500, 100))
            inventory_items.append("GrapplingGun")
        elif add_gun_button.is_clicked:
            player.inventory.add_item(Gun(10, 300, 1000, 150, None))
            inventory_items.append("Gun")
        elif add_desert_eagle_button.is_clicked:
            player.inventory.add_item(DesertEagle(None))
            inventory_items.append("DesertEagle")

def edit_weapon_dialog(player, item_index, inventory_items):
    weapon = player.inventory.items[item_index]
    back_button = Button(10, 420, 200, 40, "Back", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
    delete_button = Button(220, 420, 200, 40, "Delete", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)

    # Define buttons for modifying weapon parameters
    if isinstance(weapon, GrapplingGun):
        range_plus_button = Button(250, 40, 30, 30, "+", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
        range_minus_button = Button(290, 40, 30, 30, "-", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
        speed_plus_button = Button(250, 70, 30, 30, "+", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
        speed_minus_button = Button(290, 70, 30, 30, "-", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
        ammo_plus_button = Button(250, 100, 30, 30, "+", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
        ammo_minus_button = Button(290, 100, 30, 30, "-", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
    elif isinstance(weapon, Gun):
        damage_plus_button = Button(250, 40, 30, 30, "+", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
        damage_minus_button = Button(290, 40, 30, 30, "-", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
        range_plus_button = Button(250, 70, 30, 30, "+", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
        range_minus_button = Button(290, 70, 30, 30, "-", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
        ammo_plus_button = Button(250, 100, 30, 30, "+", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
        ammo_minus_button = Button(290, 100, 30, 30, "-", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
        speed_plus_button = Button(250, 130, 30, 30, "+", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
        speed_minus_button = Button(290, 130, 30, 30, "-", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)

    while not pyray.window_should_close():
        pyray.begin_drawing()
        pyray.clear_background(pyray.LIGHTGRAY)
        pyray.draw_text(f"Edit {weapon.__class__.__name__}", 10, 10, 20, pyray.DARKGRAY)

        # Display weapon parameters and allow editing
        if isinstance(weapon, GrapplingGun):
            pyray.draw_text(f"Range: {weapon.range}", 10, 40, 20, pyray.DARKGRAY)
            pyray.draw_text(f"Speed: {weapon.speed}", 10, 70, 20, pyray.DARKGRAY)
            pyray.draw_text(f"Ammo: {weapon.ammo}", 10, 100, 20, pyray.DARKGRAY)
            range_plus_button.draw()
            range_minus_button.draw()
            speed_plus_button.draw()
            speed_minus_button.draw()
            ammo_plus_button.draw()
            ammo_minus_button.draw()
        elif isinstance(weapon, Gun):
            pyray.draw_text(f"Damage: {weapon.damage}", 10, 40, 20, pyray.DARKGRAY)
            pyray.draw_text(f"Range: {weapon.range}", 10, 70, 20, pyray.DARKGRAY)
            pyray.draw_text(f"Ammo: {weapon.ammo}", 10, 100, 20, pyray.DARKGRAY)
            pyray.draw_text(f"Speed: {weapon.speed}", 10, 130, 20, pyray.DARKGRAY)
            damage_plus_button.draw()
            damage_minus_button.draw()
            range_plus_button.draw()
            range_minus_button.draw()
            ammo_plus_button.draw()
            ammo_minus_button.draw()
            speed_plus_button.draw()
            speed_minus_button.draw()

        range_plus_button.update()
        range_minus_button.update()
        if isinstance(weapon, GrapplingGun):
            speed_plus_button.update()
            speed_minus_button.update()
        ammo_plus_button.update()
        ammo_minus_button.update()
        if isinstance(weapon, Gun):
            damage_plus_button.update()
            damage_minus_button.update()
            speed_plus_button.update()
            speed_minus_button.update()

        back_button.draw()
        delete_button.draw()

        pyray.end_drawing()

        back_button.update()
        delete_button.update()

        if back_button.is_clicked:
            return
        elif delete_button.is_clicked:
            player.inventory.remove_item(weapon)
            inventory_items.pop(item_index)
            return

        # Handle parameter button clicks
        if isinstance(weapon, GrapplingGun):
            if range_plus_button.is_clicked:
                weapon.range += 10
            elif range_minus_button.is_clicked:
                weapon.range -= 10
            elif speed_plus_button.is_clicked:
                weapon.speed += 10
            elif speed_minus_button.is_clicked:
                weapon.speed -= 10
            elif ammo_plus_button.is_clicked:
                weapon.ammo += 1
            elif ammo_minus_button.is_clicked:
                weapon.ammo -= 1
        elif isinstance(weapon, Gun):
            if damage_plus_button.is_clicked:
                weapon.damage += 10
            elif damage_minus_button.is_clicked:
                weapon.damage -= 10
            elif range_plus_button.is_clicked:
                weapon.range += 10
            elif range_minus_button.is_clicked:
                weapon.range -= 10
            elif ammo_plus_button.is_clicked:
                weapon.ammo += 1
            elif ammo_minus_button.is_clicked:
                weapon.ammo -= 1
            elif speed_plus_button.is_clicked:
                weapon.speed += 50
            elif speed_minus_button.is_clicked:
                weapon.speed -= 50

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

def initialize_window(width, height):
    pyray.init_window(width, height, "Map Drawer")
    pyray.set_target_fps(60)
    return pyray.Camera2D(pyray.Vector2(0, 0), pyray.Vector2(0, 0), 0.0, 1.0)

def handle_main_menu(width, height, maps):
    scroll_offset = 0
    selected_map = None
    creating_new_map = False

    while not pyray.window_should_close():
        scroll_offset += pyray.get_mouse_wheel_move() * 20

        pyray.begin_drawing()
        pyray.clear_background(pyray.RAYWHITE)
        pyray.draw_text("Select Map or Create New", int(width / 2 - 150), 100, 40, pyray.DARKGRAY)

        for i, map_name in enumerate(maps):
            if pyray.gui_button(pyray.Rectangle(width / 2 - 100, height / 2 + i * 60 + scroll_offset, 200, 50), map_name):
                selected_map = map_name

        if pyray.gui_button(pyray.Rectangle(width / 2 - 100, height / 2 + len(maps) * 60 + scroll_offset, 200, 50), "Create New Map"):
            creating_new_map = True

        pyray.end_drawing()

        if selected_map or creating_new_map:
            break

    return selected_map, creating_new_map

def load_or_create_map(selected_map, creating_new_map):
    if creating_new_map:
        blocks = []
        enemies = []
        player = Player(50, 50, 0, 0, pyray.RED, None)
    else:
        map_data = load_map(os.path.join('maps', selected_map))
        blocks = map_data['blocks']
        enemies = map_data['enemies']
        player_data = map_data['player']
        player = Player(
            player_data['width'], player_data['height'], player_data['x'], player_data['y'],
            pyray.Color(player_data['color']['r'], player_data['color']['g'], player_data['color']['b'], player_data['color']['a']),
            None,
            inventory_data=player_data.get('inventory', [])
        )
    return blocks, enemies, player

def handle_user_input(blocks, enemies, player, current_block_type, camera, buttons):
    mouse_position = pyray.get_mouse_position()
    mouse_over_button = any(button.is_hovered for button in buttons)

    if not mouse_over_button:
        if pyray.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT):
            world_mouse_position = pyray.get_screen_to_world_2d(mouse_position, camera)
            x, y = snap_to_grid(world_mouse_position.x, world_mouse_position.y)
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
            world_mouse_position = pyray.get_screen_to_world_2d(mouse_position, camera)
            x, y = snap_to_grid(world_mouse_position.x, world_mouse_position.y)
            blocks = [block for block in blocks if
                      not (block.x <= x < block.x + block.width and block.y <= y < block.y + block.height)]
            enemies = [enemy for enemy in enemies if
                       not (enemy.x <= x < enemy.x + enemy.width and enemy.y <= y < enemy.y + enemy.height)]
            if player and player.x <= x < player.x + player.width and player.y <= y < player.y + player.height:
                player = None

        if pyray.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_MIDDLE):
            world_mouse_position = pyray.get_screen_to_world_2d(mouse_position, camera)
            x, y = snap_to_grid(world_mouse_position.x, world_mouse_position.y)
            for block in blocks:
                if block.x <= x < block.x + block.width and block.y <= y < block.y + block.height:
                    edit_block_dialog(block)
                    break
            if player and player.x <= x < player.x + player.width and player.y <= y < player.y + player.height:
                edit_inventory_dialog(player)

    return blocks, enemies, player

def update_camera(camera):
    if pyray.is_key_down(pyray.KeyboardKey.KEY_RIGHT):
        camera.target.x += 10
    if pyray.is_key_down(pyray.KeyboardKey.KEY_LEFT):
        camera.target.x -= 10
    if pyray.is_key_down(pyray.KeyboardKey.KEY_DOWN):
        camera.target.y += 10
    if pyray.is_key_down(pyray.KeyboardKey.KEY_UP):
        camera.target.y -= 10

def draw_ui(block_button, speedboost_button, jumpboost_button, player_button, lavablock_button, enemy_button, current_block_type, width, height, popup_message, popup_display_time):
    block_button.draw()
    speedboost_button.draw()
    jumpboost_button.draw()
    player_button.draw()
    lavablock_button.draw()
    enemy_button.draw()
    pyray.draw_text(f"Current Block Type: {current_block_type}", 10, 310, 20, pyray.DARKGRAY)

    if popup_display_time > 0:
        pyray.draw_text(popup_message, width // 2 - 100, height // 2, 20, pyray.GREEN)
        popup_display_time -= pyray.get_frame_time()

def main():
    width, height = 1366, 768
    camera = initialize_window(width, height)
    maps = list_maps('maps')
    selected_map, creating_new_map = handle_main_menu(width, height, maps)
    blocks, enemies, player = load_or_create_map(selected_map, creating_new_map)

    block_button = Button(10, 10, 150, 40, "Block", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
    speedboost_button = Button(10, 60, 150, 40, "SpeedBoostBlock", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
    jumpboost_button = Button(10, 110, 150, 40, "JumpBoostBlock", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
    player_button = Button(10, 160, 150, 40, "Player", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
    lavablock_button = Button(10, 210, 150, 40, "LavaBlock", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)
    enemy_button = Button(10, 260, 150, 40, "Enemy", 20, pyray.BLACK, pyray.LIGHTGRAY, pyray.GRAY, pyray.DARKGRAY)

    current_block_type = "Block"
    popup_display_time = 0
    popup_message = ""

    while not pyray.window_should_close():
        block_button.update()
        speedboost_button.update()
        jumpboost_button.update()
        player_button.update()
        lavablock_button.update()
        enemy_button.update()

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
        elif enemy_button.is_clicked:
            current_block_type = "Enemy"

        blocks, enemies, player = handle_user_input(blocks, enemies, player, current_block_type, camera,
                                                    [block_button, speedboost_button, jumpboost_button, player_button,
                                                     lavablock_button, enemy_button])

        if pyray.is_key_down(pyray.KeyboardKey.KEY_LEFT_CONTROL) and pyray.is_key_pressed(pyray.KeyboardKey.KEY_S):
            if pyray.is_key_down(pyray.KeyboardKey.KEY_LEFT_SHIFT) or selected_map is None or creating_new_map:
                new_map_name = text_input_dialog("Save As", "Enter new map name:")
                if new_map_name:
                    save_map(os.path.join('maps', new_map_name + '.json'), blocks, player, enemies)
                    selected_map = new_map_name + '.json'
                    creating_new_map = False
                    popup_message = "Map saved successfully!"
                    popup_display_time = 2
            else:
                save_map(os.path.join('maps', selected_map), blocks, player, enemies)
                popup_message = "Map saved successfully!"
                popup_display_time = 2

        update_camera(camera)

        pyray.begin_drawing()
        pyray.clear_background(pyray.RAYWHITE)
        pyray.begin_mode_2d(camera)

        start_x = int(camera.target.x) // 50 * 50
        end_x = int(camera.target.x + width + 50) // 50 * 50
        start_y = int(camera.target.y) // 50 * 50
        end_y = int(camera.target.y + height + 50) // 50 * 50

        for i in range(start_x, end_x + 50, 50):
            pyray.draw_line(i, start_y, i, end_y, pyray.LIGHTGRAY)
        for j in range(start_y, end_y + 50, 50):
            pyray.draw_line(start_x, j, end_x, j, pyray.LIGHTGRAY)

        for block in blocks:
            block.draw()

        for enemy in enemies:
            enemy.draw()

        if player:
            player.draw(None)

        pyray.end_mode_2d()
        draw_ui(block_button, speedboost_button, jumpboost_button, player_button, lavablock_button, enemy_button, current_block_type, width, height, popup_message, popup_display_time)
        pyray.end_drawing()

    pyray.close_window()

if __name__ == "__main__":
    main()