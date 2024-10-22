import json
import threading
from redis_manager import RedisManager

# Consumer
class Board():
    def __init__(self) -> None:
        self.pubsub = RedisManager.get_pubsub()
        self.pubsub.subscribe('tic-tac-toe')
        self.board = self.prepare_board()

    def prepare_board(self):
        matrix = list()
        for _ in range(3):
            row = [-1] * 3
            matrix.append(row)
        return matrix

    def print_board(self):
        for row in self.board:
            row_view = "|" + "|".join(str(m) for m in row) + "|"
            print(row_view)
            print("-" * 9)
    
    def update_board(self, message):
        player = message['player']
        marker = message['marker']
        x = message['x']
        y = message['y']
        
        if self.board[y][x] == -1:
            self.board[y][x] = marker
            print(f"Player {player} placed {marker} at position ({x}, {y})")
            self.print_board()
        else:
            print(f"Invalid move: Position ({x}, {y}) is already occupied")

    def handle_message(self, message):
        data = message['data'].decode('utf-8')
        if data:
            move = json.loads(data)
            self.update_board(move)

    def start_listening(self):
        def listen():
            for message in self.pubsub.listen():
                if message['type'] == 'message':
                    self.handle_message(message)

        thread = threading.Thread(target=listen, daemon=True)
        thread.start()
