import redis

class RedisManager():
    @staticmethod
    def get_client():
        pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        client = redis.Redis(connection_pool=pool)
        return client

    def add_data(data):
        client = RedisManager.get_client()
        client.set(data)

    def get_data():
        client = RedisManager.get_client()
        keys = client.keys('*')
        for k in keys:
            print(k)
