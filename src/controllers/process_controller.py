"""
Controller for monitoring and managing manufacturing processes.
"""
import os
import time
import threading
import pandas as pd
from typing import Dict, Optional
import JobOrderManager as JOManager
from ..models.process import Process
from ..utils.sound import SoundManager
from ..utils.database import db_manager

class ProcessController:
    """Controls and monitors manufacturing processes."""
    
    def __init__(self, processes: Dict[int, Process], sound_manager: SoundManager):
        """Initialize the process controller.
        
        Args:
            processes: Dictionary mapping process numbers to Process objects
            sound_manager: SoundManager instance for audio feedback
        """
        self.processes = processes
        self.sound_manager = sound_manager
        self.running = True
        self.is_speaking = False
        self.monitor_threads = {}
        self.correct_state_timers = {}
        
        # Initialize database connection
        if not db_manager.test_connection():
            print("Warning: Database connection failed. Process monitoring may not work properly.")
        
    def start_monitoring(self):
        """Start monitoring all processes."""
        print("Starting process monitoring...")
        for process_num, process in self.processes.items():
            thread = threading.Thread(
                target=self._monitor_process,
                args=(process,),
                daemon=True
            )
            thread.start()
            self.monitor_threads[process_num] = thread
            
    def stop_monitoring(self):
        """Stop monitoring all processes."""
        self.running = False
        for thread in self.monitor_threads.values():
            thread.join()
        db_manager.disconnect()
        
    def _monitor_process(self, process: Process):
        """Monitor a single process for material errors using database."""
        print(f"Monitoring process {process.process_number} from table: {process.table_name}")
        
        while self.running:
            try:
                # Only update dots if in loading state
                if process.is_loading:
                    process.update_loading_text()
                
                # Get latest data from database
                df = db_manager.get_latest_process_data(process.table_name, process.process_number)
                
                if df is not None and not df.empty:
                    # Check if this is a new record
                    current_record_id = df.index[0] if not df.empty else None
                    
                    if current_record_id != process._last_record_id:
                        print(f"New data detected in process {process.process_number}")
                        self._handle_new_data(process, df)
                        process._last_record_id = current_record_id
                else:
                    print(f"No data found for process {process.process_number}")
                    
            except Exception as e:
                print(f"Error monitoring process {process.process_number}: {e}")
                
            time.sleep(1)
                
    def _handle_new_data(self, process: Process, df: pd.DataFrame):
        """Handle new data from database for a process."""
        error_detected = False
        
        try:
            # Get the repaired action value
            repaired_action_col = f"Process_{process.process_number}_Repaired_Action"
            if repaired_action_col in df.columns:
                repaired_action = df[repaired_action_col].values[0]
                print(f"Process {process.process_number} Repaired Action: {repaired_action}")
                
                if repaired_action == "-":
                    print(f"Checking job orders for process {process.process_number}")
                    JOManager.check_job_orders()
                    JOManager.find_materials()
                    
                    # Get model code
                    model_code_col = f"Process_{process.process_number}_Model_Code"
                    if model_code_col in df.columns:
                        model_code = df[model_code_col].values[0]
                        print(f"Process {process.process_number} Model Code: {model_code}")
                        
                        if model_code in process.model_codes:
                            material_name_mp3 = ''
                            for material_name, column_name in process.material_checks.items():
                                if column_name in df.columns:
                                    material_code = df[column_name].values[0]
                                    if not any(material_code == valid_code for valid_code in JOManager.job_order_materials):
                                        if material_name == 'Casing Blk':
                                            material_name_mp3 = 'CSB'
                                        error_detected = True
                                        error_msg = f"Wrong Material Used In Process {process.process_number}"
                                        sound_title = f"Process{process.process_number}Wrong{material_name_mp3.replace(' ', '')}"
                                        process.set_error(error_msg)
                                        print(f"Error detected in process {process.process_number}: {error_msg}")
                                        self._play_error_sound(process, sound_title)
                                        break
                                        
                        if not error_detected:
                            print(f"All materials correct for process {process.process_number}")
                            process.reset_state()
                            self._show_correct_temporary(process)
                            
        except Exception as e:
            print(f"Error checking materials for process {process.process_number}: {e}")
            process.show_no_material()
        
    def _play_error_sound(self, process: Process, sound_title: str):
        """Play error sound for a process."""
        while process.has_error() and self.running:
            if not self.is_speaking:
                self.is_speaking = True
                self.sound_manager.play_mp3(sound_title)
                print(f"Playing sound: {sound_title}")
            time.sleep(2)
        self.is_speaking = False
        
    def _show_correct_temporary(self, process: Process):
        """Show correct status temporarily."""
        # Cancel any existing timer for this process
        if process.process_number in self.correct_state_timers:
            self.correct_state_timers[process.process_number].cancel()
            
        # Show correct state
        process.show_correct()
        
        # Create new timer to reset state
        timer = threading.Timer(5.0, process.reset_label)
        timer.start()
        self.correct_state_timers[process.process_number] = timer