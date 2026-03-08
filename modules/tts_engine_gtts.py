import logging
import threading
import os
import random
import tempfile
from gtts import gTTS
import pygame
import time

class TTSEngine:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.voice_character = os.getenv('FRIDAY_VOICE', 'friday')
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        
        print(f"🔊 Voice character: {self.voice_character.upper()} (using gTTS)")
        self.logger.info(f"TTS Engine initialized with gTTS")
    
    def speak(self, text):
        """Speak text using Google TTS"""
        print(f"{self.voice_character.upper()}: {text}")
        
        def _speak():
            try:
                # Create a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
                    temp_filename = f.name
                
                # Generate speech
                tts = gTTS(text=text, lang='en', slow=False)
                tts.save(temp_filename)
                
                # Play the audio
                pygame.mixer.music.load(temp_filename)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                # Clean up
                pygame.mixer.music.unload()
                try:
                    os.unlink(temp_filename)
                except:
                    pass
                    
            except Exception as e:
                self.logger.error(f"gTTS error: {e}")
        
        # Run in separate thread
        thread = threading.Thread(target=_speak)
        thread.daemon = True
        thread.start()
    
    def stop(self):
        """Stop any current speech"""
        try:
            pygame.mixer.music.stop()
        except:
            pass
