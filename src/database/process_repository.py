"""
Repository for process data operations.
"""
from typing import Optional, Dict, Any
from .connection import DatabaseConnection
from .config import TABLES

class ProcessRepository:
    """Handles database operations for process data."""
    
    def __init__(self):
        """Initialize the process repository."""
        self.db = DatabaseConnection()
    
    def get_latest_process_data(self, process_number: int) -> Optional[Dict[str, Any]]:
        """Get the latest data for a specific process.
        
        Args:
            process_number: Process number (1-6)
            
        Returns:
            Dictionary containing the latest process data or None if not found
        """
        table_name = TABLES[f'process_{process_number}']
        datetime_column = f'Process_{process_number}_DateTime'
        query = f"""
            SELECT *
            FROM {table_name}
            ORDER BY {datetime_column} DESC
            LIMIT 1
        """
        result = self.db.execute_query(query)
        return result[0] if result else None
    
    def get_process_data_by_datetime(self, process_number: int, datetime_str: str) -> Optional[Dict[str, Any]]:
        """Get process data for a specific datetime.
        
        Args:
            process_number: Process number (1-6)
            datetime_str: Datetime string in format 'YYYY-MM-DD HH:MM:SS'
            
        Returns:
            Dictionary containing the process data or None if not found
        """
        table_name = TABLES[f'process_{process_number}']
        datetime_column = f'Process_{process_number}_DateTime'
        query = f"""
            SELECT *
            FROM {table_name}
            WHERE {datetime_column} = %s
        """
        result = self.db.execute_query(query, (datetime_str,))
        return result[0] if result else None 