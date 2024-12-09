from pymemcache.client import base

class MemcachedManager:
    def __init__(self, host='localhost', port=11211):
        self.client = base.Client((host, port))

    def set(self, key, value, expire=0):
        """Store data in Memcached."""
        self.client.set(key, value, expire=expire)

    def get(self, key):
        """Retrieve data from Memcached."""
        return self.client.get(key)

# Example usage:
# manager = MemcachedManager()
# manager.set('key', 'value')
# print(manager.get('key'))