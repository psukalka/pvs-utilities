import json
from pymemcache.client import base

class MemcachedManager:
    def __init__(self, host='localhost', port=11211):
        self.client = base.Client((host, port), serializer=self.json_serializer,
                                  deserializer=self.json_deserializer)

    def set(self, key, value, expire=0):
        """Store data in Memcached."""
        self.client.set(key, value, expire=expire)

    def get(self, key):
        """Retrieve data from Memcached."""
        return self.client.get(key)
    
    def json_serializer(self, key, value):
        if type(value) == str:
            return value, 1
        return json.dumps(value), 2
    
    def json_deserializer(self, key, value, flag):
        if flag == 1:
            return value.decode('utf-8')
        elif flag == 2:
            return json.loads(value.decode('utf-8'))
        raise Exception(f"Unknown Serialization format")

# Example usage:
# manager = MemcachedManager()
# manager.set('key', 'value')
# print(manager.get('key'))