"""
Repository for process data operations.
"""
from typing import Optional, Dict, Any
from .connection import DatabaseConnection
from .config import TABLES
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ProcessRepository:
    """Handles database operations for process data."""
    
    def __init__(self):
        """Initialize the process repository."""
        self.db = DatabaseConnection()
        logger.info("ProcessRepository initialized")
    
    def get_latest_process_data(self, process_number: int) -> Optional[Dict[str, Any]]:
        """Get the latest data for a specific process.
        
        Args:
            process_number: Process number (1-6)
            
        Returns:
            Dictionary containing the latest process data or None if not found
        """
        table_name = TABLES[f'process_{process_number}']
        datetime_column = f'Process_{process_number}_DateTime'
        
        logger.debug(f"Fetching latest data for process {process_number} from table {table_name}")
        
        query = f"""
            SELECT *
            FROM {table_name}
            ORDER BY {datetime_column} DESC
            LIMIT 1
        """
        
        try:
            result = self.db.execute_query(query)
            if result:
                logger.debug(f"Found data for process {process_number}: {result[0]}")
                return result[0]
            else:
                logger.warning(f"No data found for process {process_number}")
                return None
        except Exception as e:
            logger.error(f"Error fetching data for process {process_number}: {str(e)}")
            return None
    
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
        
        logger.debug(f"Fetching data for process {process_number} at {datetime_str}")
        
        query = f"""
            SELECT *
            FROM {table_name}
            WHERE {datetime_column} = %s
        """
        
        try:
            result = self.db.execute_query(query, (datetime_str,))
            if result:
                logger.debug(f"Found data for process {process_number} at {datetime_str}: {result[0]}")
                return result[0]
            else:
                logger.warning(f"No data found for process {process_number} at {datetime_str}")
                return None
        except Exception as e:
            logger.error(f"Error fetching data for process {process_number} at {datetime_str}: {str(e)}")
            return None 