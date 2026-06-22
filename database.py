import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

class Database():
    def __init__(self):
        self.host_name=os.getenv('DATABASE_HOST')
        self.db_name=os.getenv('DATABASE_NAME')
        self.user=os.getenv('DATABASE_USER')
        self.password=os.getenv('DATABASE_PWD')
        self.conn=None
        self.cursor=None
        
    def make_db_connection(self):
        self.conn=psycopg.connect(f"dbname={self.db_name} user ={self.user} password= {self.password}")
        self.cursor=self.conn.cursor()
        self.make_schema()
    
    def end_db_connection(self):
        self.cursor.close()
        self.conn.close()
        self.conn = None
        self.cursor = None
    
    def make_schema(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY , username VARCHAR(255) UNIQUE NOT NULL , password VARCHAR(255) NOT NULL)")