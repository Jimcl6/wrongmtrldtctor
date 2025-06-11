"""
Main entry point for the Wrong Material Detector application.
"""
from src.ui.main_window import MainWindow
from src.models.process import Process
from src.controllers.process_controller import ProcessController
from src.controllers.plc_controller import PLCController
from src.utils.sound import SoundManager
from src.config import PROCESS_CONFIGS, SOUND_PATH, SERIAL_PORT, SERIAL_BAUD
from ctypes import windll

def main():
    """Initialize and start the application."""
    windll.shcore.SetProcessDpiAwareness(1)
    
    # Create process instances
    processes = {
        num: Process(num, config['csv_path'], config['model_codes'], config['material_checks'])
        for num, config in PROCESS_CONFIGS.items()
    }
    
    # Initialize controllers
    sound_manager = SoundManager(SOUND_PATH)
    process_controller = ProcessController(processes, sound_manager)
    plc_controller = PLCController(SERIAL_PORT, SERIAL_BAUD, processes)
    
    # Start controllers
    plc_controller.start()
    process_controller.start_monitoring()
    
    # Create and start UI
    def on_stop():
        process_controller.stop_monitoring()
        plc_controller.stop()
        
    window = MainWindow(processes, on_stop)
    window.run()

if __name__ == '__main__':
    main() 