"""
Test script to verify the application functionality.
"""
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from database.process_repository import ProcessRepository
from models.process import Process
from config import PROCESS_CONFIGS

def test_database_and_process():
    """Test database connection and process functionality."""
    print("=== Testing Database and Process Functionality ===\n")
    
    try:
        # Test database connection
        repo = ProcessRepository()
        print("✅ Database repository initialized successfully")
        
        # Test process 1 data retrieval
        print("\n--- Testing Process 1 Data Retrieval ---")
        data = repo.get_latest_process_data(1)
        
        if data:
            print("✅ Successfully retrieved data for process 1")
            print(f"Data keys: {list(data.keys())}")
            
            # Test ST time functionality
            print("\n--- Testing ST Time Functionality ---")
            process = Process(1, "", "process1_data", [], {})
            
            # Test with the actual data
            st_time = data.get('Process_1_ST')
            actual_time = data.get('Process_1_Actual_Time')
            
            print(f"ST Time from database: {st_time}")
            print(f"Actual Time from database: {actual_time}")
            
            if st_time and actual_time:
                is_within_limits = process.check_st_time(float(st_time), float(actual_time))
                print(f"Time within limits: {is_within_limits}")
                
                if not is_within_limits:
                    print("⚠️  Time deviation detected!")
                else:
                    print("✅ Time is within acceptable limits")
            else:
                print("⚠️  ST or Actual Time data not found in database")
                
        else:
            print("❌ No data found for process 1")
            
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_database_and_process() 