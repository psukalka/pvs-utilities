from redis_manager import RedisManager

# Consumer
class Board():
    def __init__(self) -> None:
        self.pubsub = RedisManager.get_pubsub()
        self.pubsub.subscribe('tic-tac-toe')
        self.board = self.prepare_board()

    def prepare_board(self):
        matrix = list()
        for i in range(3):
            row = []
            for j in range(3):
                row.append(-1)
            matrix.append(row)
        return matrix

    def print_board(self):
        for row in self.board:
            row_view = f"|"
            for m in row:
                row_view = f"{row_view}{m}|"
            print(row_view)
            print("-"*9)
    
    def get_move(self):
        message = self.pubsub.get_message()
        print(message)
