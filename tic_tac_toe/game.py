from .board import Board
from .player import Player

class Game():
    def __init__(self) -> None:
        self.board = Board()
        self.player1 = Player(0)
        self.player2 = Player(1)

    def play(self):
        print("Welcome to tic tac toe")
