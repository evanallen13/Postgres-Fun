import psycopg2
import os 

class POSTGRES_HOST:
    HOST = ""
    PORT = ""
    USER = ""
    PASSWORD = ""
    DB_NAME = ""
    
    def __init__(self):
        self.conn = psycopg2.connect(
                dbname=DB_NAME,
                user=USER,
                password=PASSWORD,
                host=POSTGRES_HOST.HOST,
                port=POSTGRES_HOST.PORT
            )
        self.cursor = self.conn.cursor()
        
        
