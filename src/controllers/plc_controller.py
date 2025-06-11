"""
Controller for PLC communication.
"""
import threading
import serial
from typing import Dict
from ..models.process import Process

class PLCController:
    """Controls communication with PLC/ESP8266 via serial port."""
    
    def __init__(self, port: str, baudrate: int, processes: Dict[int, Process]):
        """Initialize PLC controller.
        
        Args:
            port: Serial port for PLC/ESP8266 communication
            baudrate: Serial communication baudrate
            processes: Dictionary mapping process numbers to Process objects
        """
        self.port = port
        self.baudrate = baudrate
        self.processes = processes
        self.running = True
        self.serial = None
        
    def start(self):
        """Start the PLC controller and serial communication."""
        try:
            self.serial = serial.Serial(self.port, self.baudrate)
            print(f"Connected to ESP8266 on {self.port} at {self.baudrate} baud")
            threading.Thread(target=self._monitor_processes, daemon=True).start()
        except serial.SerialException as e:
            print(f"Failed to connect to ESP8266: {e}")
            self.running = False
        
    def stop(self):
        """Stop the PLC controller and close serial connection."""
        self.running = False
        if self.serial and self.serial.is_open:
            self.serial.write(b'L')  # Set low signal before closing
            self.serial.close()
            print("Closed ESP8266 connection")
        
    def is_running(self) -> bool:
        """Check if the PLC controller is running."""
        return self.running and self.serial and self.serial.is_open
        
    def _monitor_processes(self):
        """Monitor processes and control ESP8266 signals."""
        while self.running and self.serial and self.serial.is_open:
            try:
                # Check if any process has an error
                has_error = any(process.has_error() for process in self.processes.values())
                
                # Send appropriate signal to ESP8266
                if has_error:
                    self.serial.write(b'H')
                else:
                    self.serial.write(b'L')
                    
                # Small delay to prevent flooding the serial port
                threading.Event().wait(0.1)
                    
            except serial.SerialException as e:
                print(f"Serial communication error: {e}")
                self.running = False
                break
                
    def _handle_plc_data(self, data: str):
        """Handle data received from PLC.
        
        Args:
            data: Data string received from PLC
        """
        try:
            # Example format: "process_number,status"
            process_num, status = data.split(',')
            process_num = int(process_num)
            
            if process_num in self.processes:
                process = self.processes[process_num]
                if status == "ERROR":
                    process.set_error("Error detected by PLC")
                elif status == "OK":
                    process.reset_state()
        except (ValueError, IndexError) as e:
            print(f"Invalid data format from PLC: {e}") 