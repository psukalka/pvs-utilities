from cassandra.cluster import Cluster
from datetime import datetime
from uuid import uuid4


class CassandraManager:
    def __init__(self) -> None:
        self.client = CassandraManager.get_connection()
        self.session = self.get_session()

    @staticmethod
    def get_connection():
        cluster = Cluster(['localhost'])
        return cluster
    
    def get_session(self):
        return self.client.connect('my_app')

    def insert_users(self):
        insert_user_stmt = self.session.prepare("""
            INSERT INTO users (user_id, username, email, created_at, last_login, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        """)
        user_ids = list()
        print("Inserting users...")
        for i in range(1000):
            user_id = uuid4()
            user_ids.append(user_id)
            
            # Prepare user data
            username = f"user_{i+1}"
            email = f"user_{i+1}@example.com"
            created_at = datetime.now()
            last_login = datetime.now()
            is_active = True

            # Execute the prepared statement
            self.session.execute(insert_user_stmt, [
                user_id,
                username,
                email,
                created_at,
                last_login,
                is_active
            ])
            
            if (i + 1) % 100 == 0:
                print(f"Inserted {i + 1} users")