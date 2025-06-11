"""
Database configuration settings.
"""
from typing import Dict, Any
import os

# Database connection settings
DB_CONFIG: Dict[str, Any] = {
    'host': os.getenv('DB_HOST', '192.168.2.148'),  # Your MariaDB server address
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER', 'hpi.python'),
    'password': os.getenv('DB_PASSWORD', 'hpi.python'),
    'database': os.getenv('DB_NAME', 'fc_1_data_db'),
    'charset': 'utf8mb4',
    'connect_timeout': 10
}

# Table names for each process
TABLES = {
    'process_1': 'process1_data',
    'process_2': 'process2_data',
    'process_3': 'process3_data',
    'process_4': 'process4_data',
    'process_5': 'process5_data',
    'process_6': 'process6_data'
} 