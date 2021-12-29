import random
from typing import Deque

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

def create_empty_board(board_width, board_height):
    board = []
    for i in range(board_height):
        dummy = []
        for j in range(board_width):
            dummy.append(0)
        board.append(dummy)
    return board

def avoid_snakes_neck(last_move, possible_move):
    if last_move == None:
        return possible_move
    else:
        op_move = get_opposite_move(last_move)
        possible_move.remove(op_move)
        return possible_move

def set_board_state(board, pos, state):
    board[pos['y']][pos['x']] = state

def get_board_state(board, pos):
    return board[pos['y']][pos['x']]

class Player:

    def __init__(self, data):
        self.my_snake = data['you']
        self.board = Board(data['board'])
        self.last_move = None

    def update(self, data):
        self.my_snake = data['you']
        self.board.update(data['board'])
    
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
        return avoid_walls(self.my_snake['head'], self.board.width, self.board.height, possible_moves)
    
    def avoid_neck(self, possible_moves):
        return avoid_snakes_neck(self.last_move, possible_moves)

class Board:

    def __init__(self, board):
        self.width = board['width']
        self.height = board['height']
        
        self.foods = board['food']
        self.create_food_board(board)

        self.snakes = {}
        for snake in board['snakes']:
            self.snakes[snake['id']] = snake
        self.create_snake_board(board)

    def create_food_board(self, board):
        self.food_board = create_empty_board(self.width, self.height)
        for food in self.foods:
            set_board_state(self.food_board, food, 1)

    def create_snake_board(self, board):
        self.snake_board = create_empty_board(self.width, self.height)
        for snake in board['snakes']:
            for part in snake['body']:
                set_board_state(self.snake_board, part, snake['id'])

    def is_pos_snake(self, pos):
        return type(get_board_state(self.snake_board, pos)) == str

    def is_pos_food(self, pos):
        return get_board_state(self.food_board, pos) == 1

    def update(self, board):
        self.update_snakes(board)
        self.update_food(board)

    def update_food(self, board):
        for food in self.foods:
            set_board_state(self.food_board, food, 0)
        self.foods = board['food']
        for food in self.foods:
            set_board_state(self.food_board, food, 1)
    
    def update_food_eating_status(self, board):
        for snake_id in self.snakes:
            head = self.snakes[snake_id]['head']
            if self.is_pos_food(head):
                self.snakes[snake_id]['ate'] = True
            else:
                self.snakes[snake_id]['ate'] = False

    def update_snakes(self, board):
        deleted_snakes = self.deleted_snakes(board)
        for snake_id in deleted_snakes:
            for part in self.snakes[snake_id]['body']:
                set_board_state(self.snake_board, part, 0)
        
        for snake in board['snakes']:
            if self.snakes[snake['id']]['body'][-1] != snake['body'][-1]:
                set_board_state(self.snake_board, self.snakes[snake['id']]['body'][-1], 0)
            set_board_state(self.snake_board, snake['head'], snake['id'])

        self.snakes = {}
        for snake in board['snakes']:
            self.snakes[snake['id']] = snake

        self.update_food_eating_status(board)

    def deleted_snakes(self, board):
        deleted_snakes = []
        for snake_id in self.snakes:
            for snake in board['snakes']:
                if snake['id'] == snake_id:
                    break
            else:
                deleted_snakes.append(snake_id)
        return deleted_snakes