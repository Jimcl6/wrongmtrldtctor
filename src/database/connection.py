"""
Database connection manager.
"""
import mysql.connector
from mysql.connector import pooling
from typing import Optional, Dict, Any
from .config import DB_CONFIG

class DatabaseConnection:
    """Manages database connections using connection pooling."""
    
    _instance = None
    _pool = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the database connection pool."""
        if self._pool is None:
            try:
                self._pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name="mypool",
                    pool_size=5,
                    **DB_CONFIG
                )
                print("Database connection pool created successfully")
            except mysql.connector.Error as err:
                print(f"Error creating connection pool: {err}")
                raise
    
    def get_connection(self) -> Optional[mysql.connector.MySQLConnection]:
        """Get a connection from the pool.
        
        Returns:
            A database connection or None if connection fails
        """
        try:
            return self._pool.get_connection()
        except mysql.connector.Error as err:
            print(f"Error getting connection from pool: {err}")
            return None
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[list]:
        """Execute a query and return results.
        
        Args:
            query: SQL query to execute
            params: Query parameters
            
        Returns:
            Query results as a list of dictionaries or None if query fails
        """
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            if not conn:
                return None
                
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                conn.commit()
                return None
                
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            if conn:
                conn.rollback()
            return None
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close() 