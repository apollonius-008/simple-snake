import logging
import os

from flask import Flask
from flask import request
from logic import Player

app = Flask(__name__)
players = {}

@app.get("/")
def handle_info():
    """
    This function is called when you register your Battlesnake on play.battlesnake.com
    """
    print("INFO")
    return {
        "apiversion": "1",
        "author": "apollonius-008",
        "color": "#fcc051",
        "head": "evil",
        "tail": "curled", 
    }


@app.post("/start")
def handle_start():
    """
    This function is called everytime your snake is entered into a game.
    request.json contains information about the game that's about to be played.
    """
    data = request.get_json()
    print(f"{data['game']['id']} START")
    players[data['game']['id']] = Player(data)
    return "ok"


@app.post("/move")
def handle_move():
    """
    This function is called on every turn of a game. It's how your snake decides where to move.
    Valid moves are "up", "down", "left", or "right".
    """
    data = request.get_json()
    if data['turn'] == 0:
        players[data['game']['id']] = Player(data)
        move = players[data['game']['id']].get_move()
    else:
        players[data['game']['id']].update(data)
        move = players[data['game']['id']].get_move()
    print(f"{data['game']['id']} MOVE {move}")
    return {"move": move}


@app.post("/end")
def end():
    """
    This function is called when a game your snake was in ends.
    It's purely for informational purposes, you don't have to make any decisions here.
    """
    data = request.get_json()
    del players[data['game']['id']]
    print(f"{data['game']['id']} END")
    return "ok"


if __name__ == "__main__":
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    print("Starting Battlesnake Server...")
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=True)