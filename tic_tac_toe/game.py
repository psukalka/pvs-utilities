from .board import Board
from .player import Player
import time

class Game:
    def __init__(self):
        self.board = Board()
        self.players = []
        self.started = False

    def play(self):
        print("Welcome to tic tac toe")
        self.board.start_listening()
        
        # When a player joins, add them to the players list
        player_id = len(self.players)
        player = Player(player_id)
        self.players.append(player)
        print(f"Player {player_id} joined the game")

        if len(self.players) == 2:
            self.started = True
            self.start_game()
        else:
            print(f"Waiting for another player to join. {2 - len(self.players)} players needed")

        print("Waiting for another player to join...")
        while not self.started:
            time.sleep(1)
            print(".", end="", flush=True)

        self.start_game()

    def start_game(self):
        print("Game started")


if __name__ == "__main__":
    game = Game()
    game.play()
