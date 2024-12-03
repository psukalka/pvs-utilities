from cassandra.cluster import Cluster


class CassandraManager:
    def __init__(self) -> None:
        self.client = CassandraManager.get_connection()
        self.session = self.get_session()

    @staticmethod
    def get_connection():
        cluster = Cluster(['localhost'], port=9042)
        return cluster
    
    def get_session(self):
        return self.client.connect('my_app')