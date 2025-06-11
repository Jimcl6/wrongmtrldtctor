"""
Process model class.
"""
from typing import List, Dict
import tkinter as tk
from datetime import datetime

class Process:
    """Represents a single manufacturing process."""
    
    def __init__(self, process_number: int, csv_path: str, model_codes: List[str], material_checks: Dict[str, str]):
        """Initialize process."""
        self.process_number = process_number
        self.csv_path = csv_path
        self.model_codes = model_codes
        self.material_checks = material_checks
        
        # UI elements - will be set by UI
        self.text_label = None
        self.stop_button = None
        self.error_msg = None
        self.log_widget = None
        
        # State
        self._has_error = False
        self._error_message = ""
        self.is_loading = True
        self._expected_value = None
        self._is_correct = False
        
    def set_error(self, message: str, expected_value: str = None, actual_value: str = None):
        """Set error state with message and expected value."""
        self._has_error = True
        self._error_message = message
        self._expected_value = expected_value
        self.is_loading = False
        self._is_correct = False
        
        if self.error_msg:
            self.error_msg.config(
                text=f"{message}\nExpected: {expected_value}" if expected_value else message,
                fg="red"
            )
            self.stop_button.config(bg="red")
            
        self.log_error(message, expected_value, actual_value)
            
    def reset_state(self):
        """Reset error state."""
        self._has_error = False
        self._error_message = ""
        self._expected_value = None
        self.is_loading = True
        self._is_correct = False
        
        if self.error_msg:
            self.error_msg.config(text="Loading", fg="black")
            self.stop_button.config(bg="orange")
            
    def has_error(self) -> bool:
        """Check if process is in error state."""
        return self._has_error
        
    def get_error_message(self) -> str:
        """Get current error message."""
        return self._error_message

    def update_loading_text(self):
        """Update loading text only if in loading state and not in correct state."""
        if self.is_loading and not self._is_correct and self.error_msg:
            current_text = self.error_msg.cget("text")
            if current_text == "Loading...":
                self.error_msg.config(text="Loading")
            else:
                self.error_msg.config(text=current_text + ".")

    def log_error(self, message: str, expected_value: str = None, actual_value: str = None):
        """Add error message to log widget."""
        if self.log_widget:
            self.log_widget.config(state=tk.NORMAL)
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"\n[{timestamp}] {message}"
            if actual_value:
                log_entry += f"\n    Actual: {actual_value}"
            if expected_value:
                log_entry += f"\n    Expected: {expected_value}"
            self.log_widget.insert(tk.END, log_entry)
            self.log_widget.see(tk.END)  # Auto-scroll to bottom
            self.log_widget.config(state=tk.DISABLED)

    def show_no_material(self):
        """Show no material detected state."""
        if self.text_label:
            self.text_label.config(text=f"Process {self.process_number}", fg="black")
            if self.error_msg:
                self.error_msg.config(text="No Material Detected", fg="orange")
            self.log_error("No Material Detected")
            
    def show_correct(self):
        """Show correct state temporarily."""
        self._is_correct = True
        self.is_loading = False
        if self.text_label:
            self.text_label.config(text=f"Process {self.process_number} Correct", fg="darkgreen")
            if self.error_msg:
                self.error_msg.config(text="All Materials Correct", fg="darkgreen")
            self.log_error("All Materials Correct")
            
    def reset_label(self):
        """Reset the process label to default state."""
        self._is_correct = False
        self.is_loading = True
        if self.text_label:
            self.text_label.config(text=f"Process {self.process_number}", fg="black")
            if self.error_msg:
                self.error_msg.config(text="Loading", fg="black") 