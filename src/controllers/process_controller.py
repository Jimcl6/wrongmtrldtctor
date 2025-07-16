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
from ..database.process_repository import ProcessRepository

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
        self.process_repository = ProcessRepository()
        self.last_processed_datetime = {process_num: None for process_num in processes.keys()}
        
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
        
    def _monitor_process(self, process: Process):
        """Monitor a single process for material errors using database."""
        print(f"Monitoring process {process.process_number}")
        
        while self.running:
            try:
                # Only update dots if in loading state
                if process.is_loading:
                    process.update_loading_text()
                
                # Get latest data from database
                latest_data = self.process_repository.get_latest_process_data(process.process_number)
                
                if latest_data:
                    datetime_column = f'Process_{process.process_number}_DateTime'
                    current_datetime = latest_data[datetime_column]
                    
                    # Check if we've processed this data before
                    if current_datetime != self.last_processed_datetime[process.process_number]:
                        print(f"New data detected for process {process.process_number} at {current_datetime}")
                        self._handle_new_data(process, latest_data)
                        self.last_processed_datetime[process.process_number] = current_datetime
                else:
                    print(f"No data found for process {process.process_number}")
                    
            except Exception as e:
                print(f"Error monitoring process {process.process_number}: {e}")
                
            time.sleep(1)
                
    def _handle_new_data(self, process: Process, data: dict):
        """Handle new data from database for a process."""
        error_detected = False
        
        try:
            # Get the repaired action value
            repaired_action_col = f"Process_{process.process_number}_Repaired_Action"
            if repaired_action_col in data:
                repaired_action = data[repaired_action_col]
                print(f"Process {process.process_number} Repaired Action: {repaired_action}")
                
                if repaired_action == "-":
                    print(f"Checking job orders for process {process.process_number}")
                    JOManager.check_job_orders()
                    JOManager.find_materials()
                    
                    # Get model code
                    model_code_col = f"Process_{process.process_number}_Model_Code"
                    if model_code_col in data:
                        model_code = data[model_code_col]
                        print(f"Process {process.process_number} Model Code: {model_code}")
                        
                        # Check ST time if columns exist
                        st_column = f"Process_{process.process_number}_ST"
                        actual_time_column = f"Process_{process.process_number}_Actual_Time"
                        
                        if st_column in data and actual_time_column in data:
                            st_time = float(data[st_column]) if data[st_column] else None
                            actual_time = float(data[actual_time_column]) if data[actual_time_column] else None
                            
                            print(f"ST Time: {st_time}, Actual Time: {actual_time}")
                            
                            if not process.check_st_time(st_time, actual_time):
                                error_detected = True
                                error_msg = f"Time Deviation in Process {process.process_number}"
                                sound_title = f"Process{process.process_number}TimeDeviation"
                                process.set_st_error(error_msg)
                                print(f"Time deviation detected in process {process.process_number}")
                                self._play_error_sound(process, sound_title)
                        
                        if model_code in process.model_codes and not error_detected:
                            material_name_mp3 = ''
                            for material_name, column_name in process.material_checks.items():
                                if column_name in data:
                                    material_code = data[column_name]
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