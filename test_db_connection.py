"""
Test script to verify database connection and data retrieval.
"""
from src.database.process_repository import ProcessRepository
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_database_connection():
    """Test database connection and data retrieval."""
    try:
        # Initialize repository
        repo = ProcessRepository()
        
        # Test process 1 data retrieval
        logger.info("Testing data retrieval for process 1...")
        data = repo.get_latest_process_data(1)
        
        if data:
            logger.info("Successfully retrieved data:")
            for key, value in data.items():
                logger.info(f"{key}: {value}")
        else:
            logger.warning("No data found for process 1")
            
    except Exception as e:
        logger.error(f"Error during database test: {str(e)}")

if __name__ == "__main__":
    test_database_connection() 