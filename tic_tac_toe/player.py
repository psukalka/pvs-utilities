import json
from redis_manager import RedisManager

# Producer
class Player():
    def __init__(self, id) -> None:
        self.client = RedisManager.get_client()
        self.channel = 'tic-tac-toe'
        self.id = id
        self.marker = 'O' if id % 2 == 0 else 'X'

    def make_move(self, x, y):
        message = {
            'player': self.id,
            'marker': self.marker,
            'x': x,
            'y': y
        }
        self.client.publish(self.channel, json.dumps(message))
