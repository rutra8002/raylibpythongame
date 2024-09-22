import pyray
from map_loader import load_map
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
    # Load the map
    blocks = load_map('maps/map.json')

    # Initialize the window
    width, height = 1366, 768
    pyray.init_window(width, height, "Map Drawer")
    pyray.set_target_fps(60)

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

if __name__ == "__main__":
    main()