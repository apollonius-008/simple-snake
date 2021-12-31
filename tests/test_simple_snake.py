from simple_snake import __version__
from ..simple_snake.logic import Player
import os
import json


def test_version():
    assert __version__ == '0.1.0'

def get_all_test_files():
    path = "tests"
    all_test_files = []
    for x in os.listdir(path):
        if x.endswith('.json'):
            all_test_files.append(x)
    return all_test_files

def test_from_files():
    all_test_files = get_all_test_files()
    for fname in all_test_files:
        with open(f"tests\\{fname}", 'r') as file:
            games = json.load(file)
            for data in games:
                if data['turn'] == 0:
                    player = Player(data)
                    possible_moves = ['up', 'down', 'left', 'right']
                    possible_moves = player.all_moves(possible_moves)

                    assert possible_moves == data['expected'], f"actual={possible_moves}, expected={data['expected']}"

