"""
Test script to verify database connection and table structure.
"""
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from utils.database import db_manager
from config import PROCESS_CONFIGS

def test_database_connection():
    """Test the database connection."""
    print("Testing database connection...")
    
    if db_manager.test_connection():
        print("✅ Database connection successful!")
        return True
    else:
        print("❌ Database connection failed!")
        return False

def test_table_structure():
    """Test table structure for all processes."""
    print("\nTesting table structure...")
    
    for process_num, config in PROCESS_CONFIGS.items():
        table_name = config['table_name']
        print(f"\nProcess {process_num} - Table: {table_name}")
        
        # Get table info
        table_info = db_manager.get_table_info(table_name)
        if table_info is not None and not table_info.empty:
            print(f"✅ Table {table_name} exists with {len(table_info)} columns")
            print("Columns:")
            for _, row in table_info.iterrows():
                print(f"  - {row['COLUMN_NAME']} ({row['DATA_TYPE']})")
        else:
            print(f"❌ Table {table_name} not found or inaccessible")

def test_data_retrieval():
    """Test data retrieval from all process tables."""
    print("\nTesting data retrieval...")
    
    for process_num, config in PROCESS_CONFIGS.items():
        table_name = config['table_name']
        print(f"\nProcess {process_num} - Table: {table_name}")
        
        # Get latest data
        data = db_manager.get_latest_process_data(table_name, process_num)
        if data is not None and not data.empty:
            print(f"✅ Retrieved {len(data)} record(s) from {table_name}")
            print("Sample data:")
            print(data.head())
        else:
            print(f"❌ No data found in {table_name}")

def main():
    """Run all tests."""
    print("=== Database Connection Test ===\n")
    
    # Test connection
    if not test_database_connection():
        print("\n❌ Cannot proceed without database connection!")
        return
    
    # Test table structure
    test_table_structure()
    
    # Test data retrieval
    test_data_retrieval()
    
    print("\n=== Test Complete ===")
    
    # Clean up
    db_manager.disconnect()

if __name__ == "__main__":
    main() 