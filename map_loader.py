import json
import os
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
        color_data = item['color']
        color = pyray.Color(color_data['r'], color_data['g'], color_data['b'], color_data['a'])

        if block_type == 'Block':
            blocks.append(Block(width, height, x, y, color))
        elif block_type == 'SpeedBoostBlock':
            speed = item['speed']
            blocks.append(SpeedBoostBlock(width, height, x, y, color, speed))
        elif block_type == 'JumpBoostBlock':
            jump = item['jump']
            blocks.append(JumpBoostBlock(width, height, x, y, color, jump))

    player_data = data['player']

    return {
        'blocks': blocks,
        'player': player_data
    }

def list_maps(directory):
    return [f for f in os.listdir(directory) if f.endswith('.json')]