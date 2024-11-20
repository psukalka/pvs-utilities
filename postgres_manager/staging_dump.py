from postgres_manager.base import PostgresManager
import subprocess

class Dumper():
    def __init__(self) -> None:
        self.connection = PostgresManager()

    def get_user_related_tables(self):
        """Get all tables with FK to users_userprofile"""
        query = """
        SELECT DISTINCT tc.table_name
        FROM 
            information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage ccu
                ON ccu.constraint_name = tc.constraint_name
        WHERE 
            tc.constraint_type = 'FOREIGN KEY' 
            AND ccu.table_name = 'users_userprofile';
        """
        with self.connection as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return [row[0] for row in cur.fetchall()]

    def get_all_tables(self):
        """Get all tables in the database"""
        query = """
        SELECT tablename 
        FROM pg_tables 
        WHERE schemaname = 'public';
        """
        with self.connection as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return [row[0] for row in cur.fetchall()]

    def create_staging_dump(self):
        USER_LIMIT = 1000
        OUTPUT_FILE = "staging_dump.sql"
        
        # Get table classifications
        user_tables = set(self.get_user_related_tables())
        all_tables = set(self.get_all_tables())
        non_user_tables = all_tables - user_tables
        
        # First dump schema
        subprocess.run([
            "pg_dump",
            "-s",
            "your_database",
            "-f", OUTPUT_FILE
        ])
        
        # Dump non-user tables (full data)
        for table in non_user_tables:
            subprocess.run([
                "pg_dump",
                "-a",
                "-t", table,
                "your_database",
                "-f", f"temp_{table}.sql"
            ])
        
        # Dump limited user data
        with self.connection as conn:
            with conn.cursor() as cur:
                # Get sample user IDs
                cur.execute(f"SELECT id FROM users_userprofile LIMIT {USER_LIMIT}")
                user_ids = [str(row[0]) for row in cur.fetchall()]
        
        # Dump users table with limited data
        user_ids_str = ",".join(user_ids)
        subprocess.run([
            "pg_dump",
            "-a",
            "-t", "users_userprofile",
            "--where", f"id IN ({user_ids_str})",
            "your_database",
            "-f", "temp_users.sql"
        ])
        
        # Dump related user tables
        for table in user_tables:
            subprocess.run([
                "pg_dump",
                "-a",
                "-t", table,
                "--where", f"user_id IN ({user_ids_str})",
                "your_database",
                "-f", f"temp_{table}.sql"
            ])
        
        # Combine all files
        with open(OUTPUT_FILE, 'a') as outfile:
            for table in all_tables:
                with open(f"temp_{table}.sql") as infile:
                    outfile.write(infile.read())
                subprocess.run(["rm", f"temp_{table}.sql"])

if __name__ == "__main__":
    dumper = Dumper()
    dumper.create_staging_dump()