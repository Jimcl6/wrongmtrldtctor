"""
Database utilities for MySQL connection and querying.
"""
import pymysql
import pandas as pd
from typing import Optional, Dict, Any
from ..config import DB_CONFIG
import logging

class DatabaseManager:
    """Manages database connections and queries for the application."""
    
    def __init__(self):
        """Initialize the database manager."""
        self.db_config = DB_CONFIG
        self.connection = None
        self.logger = logging.getLogger(__name__)
            
    def connect(self) -> bool:
        """Establish connection to the database.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.connection = pymysql.connect(**self.db_config)
            self.logger.info("Successfully connected to database")
            return True
        except pymysql.Error as e:
            self.logger.error(f"Failed to connect to database: {e}")
            return False
            
    def disconnect(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.logger.info("Database connection closed")
            
    def is_connected(self) -> bool:
        """Check if database connection is active.
        
        Returns:
            bool: True if connected, False otherwise
        """
        return self.connection is not None and self.connection.open
        
    def execute_query(self, query: str, params: Optional[tuple] = None) -> Optional[pd.DataFrame]:
        """Execute a SQL query and return results as DataFrame.
        
        Args:
            query: SQL query string
            params: Optional parameters for the query
            
        Returns:
            DataFrame with query results or None if error
        """
        if not self.is_connected():
            if not self.connect():
                return None
                
        try:
            if params:
                df = pd.read_sql(query, self.connection, params=params)
            else:
                df = pd.read_sql(query, self.connection)
            return df
        except (pymysql.Error, pd.io.sql.DatabaseError) as e:
            self.logger.error(f"Query execution failed: {e}")
            # Try to reconnect in case the connection was lost
            self.disconnect()
            if self.connect():
                try:
                    df = pd.read_sql(query, self.connection, params=params)
                    return df
                except (pymysql.Error, pd.io.sql.DatabaseError) as e2:
                    self.logger.error(f"Query execution failed on retry: {e2}")
                    return None
            return None
            
    def get_latest_process_data(self, table_name: str, process_number: int) -> Optional[pd.DataFrame]:
        """Get the latest record from a process table.
        
        Args:
            table_name: Name of the process table
            process_number: Process number for filtering
            
        Returns:
            DataFrame with the latest record or None if error
        """
        # Build the query to get the latest record for MySQL
        query = f"""
        SELECT *
        FROM `{table_name}`
        WHERE `Process_{process_number}_Regular_Contractual` LIKE '%REG%'
        ORDER BY `ID` DESC
        LIMIT 1
        """
        
        # If no ID column, try with timestamp or just get the last record
        fallback_query = f"""
        SELECT *
        FROM `{table_name}`
        WHERE `Process_{process_number}_Regular_Contractual` LIKE '%REG%'
        LIMIT 1
        """
        
        result = self.execute_query(query)
        if result is None or result.empty:
            # Try fallback query
            self.logger.warning(f"Could not find 'ID' column or data in {table_name}. Trying fallback query.")
            result = self.execute_query(fallback_query)
            
        return result
        
    def test_connection(self) -> bool:
        """Test the database connection with a simple query.
        
        Returns:
            bool: True if test successful, False otherwise
        """
        try:
            test_query = "SELECT 1 as test"
            result = self.execute_query(test_query)
            return result is not None and not result.empty
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False
            
    def get_table_info(self, table_name: str) -> Optional[pd.DataFrame]:
        """Get information about table structure.
        
        Args:
            table_name: Name of the table
            
        Returns:
            DataFrame with column information or None if error
        """
        query = f"""
        SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table_name}'
        ORDER BY ORDINAL_POSITION
        """
        return self.execute_query(query)

# Global database manager instance
db_manager = DatabaseManager() 