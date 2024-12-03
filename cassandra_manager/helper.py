from base import CassandraManager
from datetime import datetime
from uuid import uuid4
import random

class CassandraHelper():
    def __init__(self) -> None:
        self.manager = CassandraManager()
        self.client = self.manager.client
        self.session = self.manager.session

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
    
    def get_users(self):
        query = "SELECT * FROM USERS";
        rows = self.session.execute(query)
        for row in rows:
            print(row.user_id, row.username, row.email, row.created_at)

    def get_user_ids(self):
        query = "SELECT user_id FROM users"
        rows = self.session.execute(query)
        user_ids = list()
        for row in rows:
            user_ids.append(row.user_id)
        return user_ids

    def insert_posts(self):
        print("Inserting posts...")
        # Sample tags for random selection
        tag_options = ['technology', 'programming', 'cassandra', 'python', 'database', 
                    'nosql', 'development', 'coding', 'data', 'software']
        
        insert_post_stmt = self.session.prepare("""
            INSERT INTO posts (post_id, user_id, title, content, created_at, updated_at, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """)
        
        user_ids = self.get_user_ids()
        for i in range(1000):
            # Prepare post data
            post_id = uuid4()
            user_id = random.choice(user_ids)  # Randomly assign post to a user
            title = f"Post Title {i+1}"
            content = f"This is the content for post {i+1}. It contains some sample text that demonstrates a typical blog post. Generated at {datetime.now()}"
            created_at = datetime.now()
            updated_at = datetime.now()
            
            # Randomly select 1-3 tags for each post
            tags = set(random.sample(tag_options, random.randint(1, 3)))

            # Execute the prepared statement
            self.session.execute(insert_post_stmt, [
                post_id,
                user_id,
                title,
                content,
                created_at,
                updated_at,
                tags
            ])
            
            if (i + 1) % 100 == 0:
                print(f"Inserted {i + 1} posts")

    def get_posts(self):
        query = "SELECT * FROM posts"
        rows = self.session.execute(query)
        for row in rows:
            print(row.user_id, row.post_id, row.title)