# Wrong Material Detector

A Python application designed to detect and manage wrong materials in an industrial process environment. The application integrates with PLC systems, provides real-time monitoring, and includes sound alerts for material detection events.

## Project Structure

```
├── main.py                 # Main entry point of the application
├── requirements.txt        # Python package dependencies
├── setup.py               # Package setup configuration
├── imports.py             # Common import statements
├── JobOrderManager.py     # Manages job orders and their processing
├── DateTimeManager.py     # Handles date and time operations
├── Sounds/                # Directory containing sound files for alerts
├── src/                   # Source code directory
│   ├── config.py         # Application configuration settings
│   ├── __init__.py       # Package initialization
│   ├── views/            # UI view components
│   ├── utils/            # Utility functions and helpers
│   ├── models/           # Data models and business logic
│   ├── ui/               # User interface components
│   ├── database/         # Database related code
│   └── controllers/      # Application controllers
```

## Key Components

### Main Application Files

- `main.py`: The entry point of the application that initializes all components and starts the UI
- `JobOrderManager.py`: Handles job order processing and management
- `DateTimeManager.py`: Provides date and time management functionality
- `imports.py`: Centralizes common import statements

### Source Code (`src/`)

- `config.py`: Contains application-wide configuration settings
- `views/`: Contains UI view components for different screens
- `utils/`: Utility functions and helper classes
- `models/`: Data models representing business entities
- `ui/`: User interface components and layouts
- `database/`: Database interaction and management code
- `controllers/`: Application controllers managing business logic

### Resources

- `Sounds/`: Directory containing sound files used for alerts and notifications

## Features

- Real-time material detection
- PLC system integration
- Sound alerts for material detection events
- Job order management
- User-friendly interface
- Process monitoring and control

## Setup and Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure the application settings in `src/config.py`
3. Run the application:
   ```bash
   python main.py
   ```

## Dependencies

See `requirements.txt` for a complete list of Python package dependencies.

## Configuration

The application can be configured through `src/config.py`, which includes settings for:

- Process configurations
- Sound paths
- Serial port settings
- Other application parameters

## License

[Add your license information here]
