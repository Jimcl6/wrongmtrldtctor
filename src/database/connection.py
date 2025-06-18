"""
Database connection manager.
"""
import mysql.connector
from mysql.connector import pooling
from typing import Optional, Dict, Any
from .config import DB_CONFIG
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
                logger.info(f"Attempting to connect to database at {DB_CONFIG['host']}:{DB_CONFIG['port']}")
                self._pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name="mypool",
                    pool_size=5,
                    **DB_CONFIG
                )
                logger.info("Database connection pool created successfully")
            except mysql.connector.Error as err:
                logger.error(f"Error creating connection pool: {err}")
                raise
    
    def get_connection(self) -> Optional[mysql.connector.MySQLConnection]:
        """Get a connection from the pool.
        
        Returns:
            A database connection or None if connection fails
        """
        try:
            conn = self._pool.get_connection()
            logger.debug("Successfully obtained database connection from pool")
            return conn
        except mysql.connector.Error as err:
            logger.error(f"Error getting connection from pool: {err}")
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
            logger.debug(f"Executing query: {query}")
            if params:
                logger.debug(f"Query parameters: {params}")
                
            conn = self.get_connection()
            if not conn:
                logger.error("Failed to get database connection")
                return None
                
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
                logger.debug(f"Query returned {len(result)} rows")
                return result
            else:
                conn.commit()
                logger.debug("Non-SELECT query executed successfully")
                return None
                
        except mysql.connector.Error as err:
            logger.error(f"Error executing query: {err}")
            if conn:
                conn.rollback()
            return None
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                logger.debug("Database connection closed") 