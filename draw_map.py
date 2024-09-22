import pyray
import os
from map_loader import load_map, list_maps
from block import Block
from speedboostblock import SpeedBoostBlock
from jumpboostblock import JumpBoostBlock

# Define block types
BLOCK_TYPES = {
    "Block": Block,
    "SpeedBoostBlock": SpeedBoostBlock,
    "JumpBoostBlock": JumpBoostBlock
}

def snap_to_grid(x, y, grid_size=50):
    return (x // grid_size) * grid_size, (y // grid_size) * grid_size

def main():
    # Initialize the window
    width, height = 1366, 768
    pyray.init_window(width, height, "Map Drawer")
    pyray.set_target_fps(60)

    # Menu to choose between loading an existing map or creating a new one
    maps = list_maps('maps')
    selected_map = None
    creating_new_map = False

    while not pyray.window_should_close():
        if selected_map is None and not creating_new_map:
            pyray.begin_drawing()
            pyray.clear_background(pyray.RAYWHITE)
            pyray.draw_text("Select Map or Create New", int(width / 2 - 150), 100, 40, pyray.DARKGRAY)

            for i, map_name in enumerate(maps):
                if pyray.gui_button(pyray.Rectangle(width / 2 - 100, height / 2 + i * 60, 200, 50), map_name):
                    selected_map = map_name

            if pyray.gui_button(pyray.Rectangle(width / 2 - 100, height / 2 + len(maps) * 60, 200, 50), "Create New Map"):
                creating_new_map = True

            pyray.end_drawing()
        else:
            if creating_new_map:
                blocks = []
            else:
                blocks = load_map(os.path.join('maps', selected_map))

            # Current block type to place
            current_block_type = "Block"

            while not pyray.window_should_close():
                # Handle input
                if pyray.is_key_pressed(pyray.KeyboardKey.KEY_ONE):
                    current_block_type = "Block"
                elif pyray.is_key_pressed(pyray.KeyboardKey.KEY_TWO):
                    current_block_type = "SpeedBoostBlock"
                elif pyray.is_key_pressed(pyray.KeyboardKey.KEY_THREE):
                    current_block_type = "JumpBoostBlock"

                if pyray.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT):
                    mouse_position = pyray.get_mouse_position()
                    x, y = snap_to_grid(mouse_position.x, mouse_position.y)
                    if current_block_type == "Block":
                        blocks.append(Block(50, 50, x, y, pyray.BLUE))
                    elif current_block_type == "SpeedBoostBlock":
                        blocks.append(SpeedBoostBlock(50, 50, x, y, pyray.GREEN, 800))
                    elif current_block_type == "JumpBoostBlock":
                        blocks.append(JumpBoostBlock(50, 50, x, y, pyray.YELLOW, 800))

                # Start drawing
                pyray.begin_drawing()
                pyray.clear_background(pyray.RAYWHITE)

                # Draw grid
                for i in range(0, width, 50):
                    pyray.draw_line(i, 0, i, height, pyray.LIGHTGRAY)
                for j in range(0, height, 50):
                    pyray.draw_line(0, j, width, j, pyray.LIGHTGRAY)

                # Draw each block
                for block in blocks:
                    block.draw()

                # Draw UI
                pyray.draw_text("Press 1 for Block, 2 for SpeedBoostBlock, 3 for JumpBoostBlock", 10, 10, 20, pyray.DARKGRAY)
                pyray.draw_text(f"Current Block Type: {current_block_type}", 10, 40, 20, pyray.DARKGRAY)

                # End drawing
                pyray.end_drawing()

            # Close the window
            pyray.close_window()
            break

if __name__ == "__main__":
    main()