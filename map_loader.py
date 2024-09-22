import json
import pyray
from block import Block
from speedboostblock import SpeedBoostBlock
from jumpboostblock import JumpBoostBlock


def load_map(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    blocks = []
    for item in data['blocks']:
        block_type = item['type']
        width = item['width']
        height = item['height']
        x = item['x']
        y = item['y']
        color = getattr(pyray, item['color'])

        if block_type == 'Block':
            blocks.append(Block(width, height, x, y, color))
        elif block_type == 'SpeedBoostBlock':
            speed = item['speed']
            blocks.append(SpeedBoostBlock(width, height, x, y, color, speed))
        elif block_type == 'JumpBoostBlock':
            jump = item['jump']
            blocks.append(JumpBoostBlock(width, height, x, y, color, jump))

    return blocks