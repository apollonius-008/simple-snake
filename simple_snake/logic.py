import random

def pos_after_move(pos: dict, move: str):
    if move == 'up':
        return {'x': pos['x'], 'y': pos['y'] + 1}
    elif move == 'down':
        return {'x': pos['x'], 'y': pos['y'] - 1}
    elif move == 'left':
        return {'x': pos['x'] - 1, 'y': pos['y']}
    elif move == 'right':
        return {'x': pos['x'] + 1, 'y': pos['y']}
    else:
        return None

def pos_is_in_boundary(pos: dict, board_width, board_height):
    return pos['x'] < board_width and pos['x'] >= 0 and pos['y'] < board_height and pos['y'] >= 0

def avoid_walls(snake_head, board_width, board_height, possible_moves):
    for i in range(len(possible_moves) - 1, -1, -1):
        move = possible_moves[i]
        new_pos = pos_after_move(snake_head, move)
        if not pos_is_in_boundary(new_pos, board_width, board_height):
            possible_moves.pop(i)
    return possible_moves

def get_opposite_move(move):
    if move == 'up':
        return 'down'
    elif move == 'down':
        return 'up'
    elif move == 'left':
        return 'right'
    elif move == 'right':
        return 'left'
    else:
        print(f"get_opposite_move(move) :: Invalid Move. move={move}")

def avoid_snakes_neck(last_move, possible_move):
    if last_move == None:
        return possible_move
    else:
        op_move = get_opposite_move(last_move)
        possible_move.remove(op_move)
        return possible_move

class Player:

    def __init__(self, data):
        self.my_snake = data['you']
        self.board = data['board']
        self.last_move = None

    def update(self, data):
        self.my_snake = data['you']
        self.board = data['board']
    
    def get_move(self):
        possible_moves = ['up', 'down', 'left', 'right']
        possible_moves = self.all_moves(possible_moves)
        if len(possible_moves) == 0:
            return self.last_move
        else:
            move = random.choice(possible_moves)
            self.last_move = move
            return move

    def all_moves(self, possible_moves):
        possible_moves = self.avoid_neck(possible_moves)
        possible_moves = self.avoid_walls(possible_moves)
        return possible_moves

    def avoid_walls(self, possible_moves):
        return avoid_walls(self.my_snake['head'], self.board['width'], self.board['height'], possible_moves)
    
    def avoid_neck(self, possible_moves):
        return avoid_snakes_neck(self.last_move, possible_moves)
    
