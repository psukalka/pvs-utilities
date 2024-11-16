import psycopg2
import random
import string

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

    def get_data(self, query=None):
        """
        Sample queries:
        SELECT * FROM employees WHERE id < 100 ORDER BY age;
        """
        if query is None:
            query = "SELECT * FROM employees"
        cursor = self.client.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def add_data(self):
        # Insert random 1000 records into employees table
        # Age should be between 20 and 60
        # Name should be between 3 to 10 characters
        cursor = self.client.cursor()
        for i in range(1000):
            name = ''.join(random.choices(string.ascii_letters, k=random.randint(3, 10)))
            age = random.randint(20, 60)
            cursor.execute("INSERT INTO employees (name, age) VALUES (%s, %s)", (name, age))
        self.client.commit()
        cursor.close()

