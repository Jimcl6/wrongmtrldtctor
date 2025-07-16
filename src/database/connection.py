"""
Database connection manager.
"""
import pymysql
from typing import Optional, Dict, Any
from .config import DB_CONFIG
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Manages database connections using connection pooling."""
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the database connection."""
        if self._connection is None:
            try:
                logger.info(f"Attempting to connect to database at {DB_CONFIG['host']}:{DB_CONFIG.get('port', 3306)}")
                self._connection = pymysql.connect(**DB_CONFIG)
                logger.info("Database connection created successfully")
            except pymysql.Error as err:
                logger.error(f"Error creating connection: {err}")
                raise
    
    def get_connection(self) -> Optional[pymysql.Connection]:
        """Get the database connection.
        
        Returns:
            A database connection or None if connection fails
        """
        try:
            if self._connection and self._connection.open:
                return self._connection
            else:
                # Reconnect if connection is closed
                self._connection = pymysql.connect(**DB_CONFIG)
                return self._connection
        except pymysql.Error as err:
            logger.error(f"Error getting connection: {err}")
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
                
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
                logger.debug(f"Query returned {len(result)} rows")
                return result
            else:
                conn.commit()
                logger.debug("Non-SELECT query executed successfully")
                return None
                
        except pymysql.Error as err:
            logger.error(f"Error executing query: {err}")
            if conn:
                conn.rollback()
            return None
            
        finally:
            if cursor:
                cursor.close()
    
    def close(self):
        """Close the database connection."""
        if self._connection and self._connection.open:
            self._connection.close()
            self._connection = None
            logger.info("Database connection closed") 