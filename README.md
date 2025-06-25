# Wrong Material Detector

A Python application designed to detect and manage wrong materials in an industrial process environment. The application integrates with PLC systems, provides real-time monitoring, and includes sound alerts for material detection events.

## Recent Updates

### SQL Database Integration
The application has been updated to read process data from a MySQL database instead of CSV files:
- **Database**: MySQL on `192.168.2.148`
- **Database Name**: `fc_1_data_db`
- **Tables**: `process1_data`, `process2_data`, `process3_data`, `process4_data`, `process5_data`, `process6_data`
- **Job Order Manager**: Still reads from CSV files as before

### Column Naming Convention
Database columns follow the pattern: `Process_{N}_{Column_Name}` (underscores instead of spaces)
- Example: `Process_1_Regular_Contractual` (instead of `Process 1 Regular/Contractual`)

## Project Structure

```
├── main.py                 # Main entry point of the application
├── requirements.txt        # Python package dependencies
├── setup.py               # Package setup configuration
├── imports.py             # Common import statements
├── JobOrderManager.py     # Manages job orders and their processing (CSV-based)
├── DateTimeManager.py     # Handles date and time operations
├── test_db_connection.py  # Database connection test script
├── Sounds/                # Directory containing sound files for alerts
├── src/                   # Source code directory
│   ├── config.py         # Application configuration settings
│   ├── __init__.py       # Package initialization
│   ├── views/            # UI view components
│   ├── utils/            # Utility functions and helpers
│   │   ├── sound.py      # Sound management utilities
│   │   └── database.py   # Database connection and querying
│   ├── models/           # Data models and business logic
│   ├── ui/               # User interface components
│   └── controllers/      # Application controllers
```

## Key Components

### Main Application Files

- `main.py`: The entry point of the application that initializes all components and starts the UI
- `JobOrderManager.py`: Handles job order processing and management (CSV-based)
- `DateTimeManager.py`: Provides date and time management functionality
- `imports.py`: Centralizes common import statements
- `test_db_connection.py`: Tests database connection and table structure

### Source Code (`src/`)

- `config.py`: Contains application-wide configuration settings including database connection
- `views/`: Contains UI view components for different screens
- `utils/`: Utility functions and helper classes
  - `sound.py`: Sound playback and text-to-speech functionality
  - `database.py`: MySQL database connection and querying utilities
- `models/`: Data models representing business entities
- `ui/`: User interface components and layouts
- `controllers/`: Application controllers managing business logic

### Resources

- `Sounds/`: Directory containing sound files used for alerts and notifications

## Features

- Real-time material detection from SQL database
- PLC system integration
- Sound alerts for material detection events
- Job order management (CSV-based)
- User-friendly interface
- Process monitoring and control
- Database connection management

## Setup and Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure the application settings in `src/config.py`:
   - Database connection details
   - Process configurations
   - Sound paths
   - Serial port settings

3. Test the database connection:
   ```bash
   python test_db_connection.py
   ```

4. Run the application:
   ```bash
   python main.py
   ```

## Dependencies

See `requirements.txt` for a complete list of Python package dependencies, including:
- `pymysql`: MySQL database connection
- `pandas`: Data manipulation
- `pygame`: Audio playback
- `pyttsx3`: Text-to-speech
- `pyserial`: Serial communication

## Configuration

The application can be configured through `src/config.py`, which includes settings for:

- Database connection parameters
- Process configurations
- Sound paths
- Serial port settings
- Other application parameters

## Database Schema

Each process table (`process1_data` through `process6_data`) contains columns following the naming convention:
- `Process_{N}_Regular_Contractual`
- `Process_{N}_Repaired_Action`
- `Process_{N}_Model_Code`
- Material check columns (specific to each process)

## License

[Add your license information here]
