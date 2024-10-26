import json
import os
import pyray
from blocks.block import Block
from blocks.speedboostblock import SpeedBoostBlock
from blocks.jumpboostblock import JumpBoostBlock
from blocks.lavablock import LavaBlock
from enemy import Enemy  # Import Enemy

def load_map(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    blocks = []
    enemies = []
    for item in data['blocks']:
        block_type = item['type']
        height = item['height']
        width = item['width']
        x = item['x']
        y = item['y']
        color_data = item['color']
        color = pyray.Color(color_data['r'], color_data['g'], color_data['b'], color_data['a'])

        if block_type == 'Block':
            blocks.append(Block(height, width, x, y, color))
        elif block_type == 'SpeedBoostBlock':
            speed = item['speed']
            blocks.append(SpeedBoostBlock(height, width, x, y, color, speed))
        elif block_type == 'JumpBoostBlock':
            jump = item['jump']
            blocks.append(JumpBoostBlock(height, width, x, y, color, jump))
        elif block_type == 'LavaBlock':
            blocks.append(LavaBlock(height, width, x, y, color))

    for item in data.get('enemies', []):
        height = item['height']
        width = item['width']
        x = item['x']
        y = item['y']
        color_data = item['color']
        color = pyray.Color(color_data['r'], color_data['g'], color_data['b'], color_data['a'])
        health = item['health']
        enemies.append(Enemy(height, width, x, y, color, health))

    player_data = data['player']
    inventory_data = player_data.get('inventory', [])
    player_data['inventory'] = inventory_data

    return {
        'blocks': blocks,
        'enemies': enemies,
        'player': player_data
    }

def list_maps(directory):
    return [f for f in os.listdir(directory) if f.endswith('.json')]