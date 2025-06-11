"""
Sound utilities for playing audio feedback.
"""
import os
import pygame
import pyttsx3
from typing import Optional

class SoundManager:
    """Manages sound playback for the application."""
    
    def __init__(self, sound_path: str):
        """Initialize the sound manager.
        
        Args:
            sound_path: Base path for sound files
        """
        self.sound_path = sound_path
        self.engine: Optional[pyttsx3.Engine] = None
        pygame.init()
        
    def play_mp3(self, sound_title: str):
        """Play an MP3 file.
        
        Args:
            sound_title: Name of the sound file without extension
        """
        path = os.path.join(self.sound_path, f"{sound_title}.mp3")
        
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
    def stop_mp3(self):
        """Stop currently playing MP3."""
        pygame.mixer.music.stop()
        
    def speak_text(self, text: str, rate: int = 100):
        """Speak text using text-to-speech.
        
        Args:
            text: Text to speak
            rate: Speech rate (default 100)
        """
        if not self.engine:
            self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.say(text)
        self.engine.runAndWait() 