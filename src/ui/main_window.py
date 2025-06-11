"""
Main application window.
"""
import tkinter as tk
from tkinter import ttk
from typing import Dict, Callable
from ..models.process import Process
from ..config import UI_CONFIG

class MainWindow:
    """Main application window."""
    
    def __init__(self, processes: Dict[int, Process], on_stop: Callable[[], None]):
        """Initialize main window."""
        self.processes = processes
        self.on_stop = on_stop
        self.root = tk.Tk()
        self._setup_window()
        self._create_widgets()
        
    def _setup_window(self):
        """Configure the main window."""
        self.root.title('Wrong Material Detector')
        self.root.geometry('1480x800+50+50')  # Increased height for logs
        
        # Fix DPI scaling on Windows
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass
            
        # Configure columns
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
            
    def _create_widgets(self):
        """Create and layout all widgets."""
        # Title
        title_text = tk.Label(
            self.root,
            text="Wrong Material Detector",
            font=("Arial", 16, "bold")
        )
        title_text.grid(column=0, row=0, pady=(10, 20), columnspan=3)

        # Create frames for each process
        for i in range(1, 7):
            process = self.processes[i]
            frame = ttk.LabelFrame(self.root, text=f"Process {i}")
            frame.grid(row=(i-1)//3, column=(i-1)%3, padx=10, pady=10, sticky="nsew")
            
            # Process title
            process.text_label = tk.Label(
                frame,
                text=f"Process {i}",
                font=("Arial", 12, "bold")
            )
            process.text_label.pack(pady=(5, 5))
            
            # Stop button
            process.stop_button = tk.Button(
                frame,
                text='STOP',
                font=("Arial", 12, "bold"),
                command=lambda p=process: self._on_stop_button(p),
                width=15,
                height=1
            )
            process.stop_button.pack(pady=(5, 5))
            process.stop_button.config(bg="orange", fg="black")
            
            # Status label
            process.error_msg = tk.Label(
                frame,
                text="Loading",
                font=("Arial", 12,'bold'),
                wraplength=200
            )
            process.error_msg.pack(pady=(5, 5))
            
            # Log widget
            log_frame = ttk.LabelFrame(frame, text="Error Log")
            log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            process.log_widget = tk.Text(
                log_frame,
                height=8,
                width=30,
                font=("Consolas", 9),
                wrap=tk.WORD,
                state=tk.DISABLED
            )
            process.log_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Add scrollbar to log
            scrollbar = ttk.Scrollbar(process.log_widget, command=process.log_widget.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            process.log_widget.config(yscrollcommand=scrollbar.set)
        
    def _on_stop_button(self, process: Process):
        """Handle stop button click."""
        process.reset_state()
        
    def run(self):
        """Start the main event loop."""
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()
        
    def _on_close(self):
        """Handle window close event."""
        self.on_stop()
        self.root.destroy()