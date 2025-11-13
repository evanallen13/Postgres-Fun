import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv() 

class POSTGRES_HOST:
    
    def __init__(self):
        self.conn = psycopg2.connect(
                dbname=os.getenv("PGDATABASE"),
                user=os.getenv("PGUSER"),
                password=os.getenv("PGPASSWORD"),
                host=os.getenv("PGHOST"),
                port=os.getenv("PGPORT")
            )
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.conn.cursor()

    def init_db(self):
        """Initialize database with pgvector and a documents table"""
        try:
            self.cur.execute(f"""
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    content TEXT
                );
            """)
            print("✅ Database initialized successfully!")
        except Exception as e:
            print("❌ Error initializing database:", e)
    
    def insert_document(self, content):
        """Insert a document and its embedding"""
        print("Inserting document:", content)
        try:
            self.cur.execute(
                "INSERT INTO documents (content) VALUES (%s);",
                (content,)
            )
        except Exception as e:
            print("❌ Error inserting document:", e)

    def delete_documents(self):
        """Delete all documents from the table"""
        try:
            self.cur.execute("DELETE FROM documents;")
            print("✅ All documents deleted successfully!")
        except Exception as e:
            print("❌ Error deleting documents:", e)
            
    def get_documents(self):
        """Retrieve all documents from the table"""
        try:
            self.cur.execute("SELECT * FROM documents;")
            result = self.cur.fetchall()
            print("✅ Documents retrieved successfully!")
            return result
        except Exception as e:
            print("❌ Error retrieving documents:", e)
