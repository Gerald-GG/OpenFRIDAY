import pyttsx3
import logging
import threading

class TTSEngine:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.engine = None
        self.init_engine()
        
    def init_engine(self):
        """Initialize the text-to-speech engine"""
        try:
            self.engine = pyttsx3.init()
            # Configure voice properties
            voices = self.engine.getProperty('voices')
            if voices:
                # Try to find a female voice (F.R.I.D.A.Y. should be female)
                for voice in voices:
                    if 'female' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
            # Set speech rate (slower for clarity)
            self.engine.setProperty('rate', 175)
            # Set volume
            self.engine.setProperty('volume', 0.9)
            self.logger.info("TTS Engine initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize TTS: {e}")
            self.engine = None
    
    def speak(self, text):
        """Speak text asynchronously"""
        if not self.engine:
            self.logger.warning("TTS not available")
            print(f"F.R.I.D.A.Y.: {text}")
            return
            
        def _speak():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                self.logger.error(f"TTS error: {e}")
                print(f"F.R.I.D.A.Y.: {text}")
        
        # Run in separate thread to avoid blocking
        thread = threading.Thread(target=_speak)
        thread.daemon = True
        thread.start()
    
    def stop(self):
        """Stop any current speech"""
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass
