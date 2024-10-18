from .game import Game
g = Game()

def run_board():
    g.board.print_board()

def register_player():
    g.player1.make_move(1,2)

def receive_message():
    g.board.get_move()
