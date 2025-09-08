import sqlite3
import os
from contextlib import contextmanager

class Database:
    def __init__(self, db_path="shelfheng.db"):
        self.db_path = db_path
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # This makes rows behave like dictionaries
        try:
            yield conn
        finally:
            conn.close()
    
    def execute(self, query, *params):
        """Execute a query and return results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            # For SELECT queries, return results
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                # For INSERT/UPDATE/DELETE, commit and return cursor
                conn.commit()
                return cursor

# Create a global database instance
db = Database()
