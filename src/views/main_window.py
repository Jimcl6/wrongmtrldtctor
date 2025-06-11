import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from typing import Dict
from ..models.process import Process

class MainWindow:
    def __init__(self, processes: Dict[int, Process]):
        """Initialize the main window with modern styling."""
        self.root = ctk.CTk()
        self.root.title('Wrong Material Detector')
        self.root.geometry('1480x600+50+50')
        
        # Set the appearance mode and default color theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Configure grid weights
        self.root.grid_columnconfigure((0, 1, 2), weight=1)
        self.root.grid_rowconfigure((1, 2, 3, 4), weight=1)
        
        # Create header frame
        self.create_header_frame()
        
        # Create process frames
        self.create_process_frames(processes)
        
        # Create master stop button
        self.create_master_stop_button()
        
    def create_header_frame(self):
        """Create the header with title."""
        header_frame = ctk.CTkFrame(self.root, corner_radius=10)
        header_frame.grid(row=0, column=0, columnspan=3, padx=20, pady=(20,10), sticky="ew")
        
        title = ctk.CTkLabel(
            header_frame, 
            text="Wrong Material Detector",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=10)
        
    def create_process_frames(self, processes: Dict[int, Process]):
        """Create frames for each process."""
        for i, (process_num, process) in enumerate(processes.items()):
            # Calculate grid position
            row = (i // 3) * 2 + 1
            col = i % 3
            
            # Create process frame
            process_frame = ctk.CTkFrame(self.root, corner_radius=15)
            process_frame.grid(row=row, column=col, padx=20, pady=10, sticky="nsew")
            
            # Process label
            process.text_label = ctk.CTkLabel(
                process_frame,
                text=f"Process {process_num}",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            process.text_label.pack(pady=(15,5))
            
            # Stop button
            process.stop_button = ctk.CTkButton(
                process_frame,
                text="STOP",
                font=ctk.CTkFont(size=16),
                width=120,
                height=32,
                fg_color="orange",
                hover_color="#FF6B00",
                command=lambda p=process: self.stop_process(p)
            )
            process.stop_button.pack(pady=10)
            
            # Error message
            process.error_msg = ctk.CTkLabel(
                process_frame,
                text=process.error_msg_text,
                font=ctk.CTkFont(size=14)
            )
            process.error_msg.pack(pady=(5,15))
            
    def create_master_stop_button(self):
        """Create the master stop button."""
        master_stop_frame = ctk.CTkFrame(self.root, corner_radius=10)
        master_stop_frame.grid(row=5, column=0, columnspan=3, padx=20, pady=20, sticky="ew")
        
        self.master_stop_button = ctk.CTkButton(
            master_stop_frame,
            text="STOP ALL",
            font=ctk.CTkFont(size=20, weight="bold"),
            width=200,
            height=45,
            fg_color="red",
            hover_color="#CC0000",
            command=self.stop_all_processes
        )
        self.master_stop_button.pack(pady=15)
        
    def stop_process(self, process: Process):
        """Stop a single process."""
        process.reset_state()
        
    def stop_all_processes(self):
        """Stop all processes."""
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkButton) and child != self.master_stop_button:
                        process = child.process if hasattr(child, 'process') else None
                        if process:
                            self.stop_process(process)
        
    def run(self):
        """Start the main event loop."""
        self.root.mainloop()
        
    def on_closing(self):
        """Handle window closing."""
        self.root.destroy() 