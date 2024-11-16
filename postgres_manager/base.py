import psycopg2

class PostgresManager:
    def __init__(self) -> None:
        self.client = PostgresManager.get_client()

    @staticmethod
    def get_client():
        client = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="pvs123"
        )
        return client

    def get_data(self):
        cursor = self.client.cursor()
        cursor.execute("SELECT * FROM employees")
        return cursor.fetchall()

