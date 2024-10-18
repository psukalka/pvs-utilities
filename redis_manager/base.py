import redis

class RedisManager():

    def __init__(self) -> None:
        self.client = RedisManager.get_client()

    @staticmethod
    def get_client():
        pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        client = redis.Redis(connection_pool=pool)
        return client
    
    @staticmethod
    def get_pubsub():
        client = RedisManager.get_client()
        return client.pubsub()

    def add_data(self, data):
        for k, v in data.items():
            self.client.set(k, v)

    def get_data(self):
        keys = self.client.keys('*')
        for k in keys:
            print(k)

    def add_bulk_data(self):
        emps = list()
        for i in range(1000):
            emps.append({f'emp{i}': f'Employee {i}'})
        for emp in emps:
            self.add_data(emp)