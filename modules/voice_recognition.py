import speech_recognition as sr
import threading
import logging
import time

class VoiceListener:
    def __init__(self, config, callback):
        self.config = config
        self.callback = callback
        self.logger = logging.getLogger(__name__)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False
        self.thread = None
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        
        self.logger.info("Voice listener initialized")
        
        # Start listening thread
        self.start()
    
    def listen_loop(self):
        """Main listening loop"""
        while self.listening:
            try:
                with self.microphone as source:
                    self.logger.debug("Listening for wake word...")
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # Try to recognize speech
                try:
                    text = self.recognizer.recognize_google(audio).lower()
                    self.logger.debug(f"Heard: {text}")
                    
                    # Check for wake word
                    if self.config['wake_word'] in text:
                        self.logger.info("Wake word detected!")
                        # Remove wake word from command
                        command = text.replace(self.config['wake_word'], '').strip()
                        if command:
                            self.callback(command)
                        else:
                            self.callback("Yes, I'm listening?")
                    
                except sr.UnknownValueError:
                    pass  # Didn't understand
                except sr.RequestError as e:
                    self.logger.error(f"Speech recognition error: {e}")
                    
            except sr.WaitTimeoutError:
                pass  # No speech detected
            except Exception as e:
                self.logger.error(f"Error in listen loop: {e}")
                time.sleep(1)
    
    def start(self):
        """Start listening thread"""
        if not self.listening:
            self.listening = True
            self.thread = threading.Thread(target=self.listen_loop)
            self.thread.daemon = True
            self.thread.start()
            self.logger.info("Voice listener started")
    
    def stop(self):
        """Stop listening"""
        self.listening = False
        if self.thread:
            self.thread.join(timeout=2)
        self.logger.info("Voice listener stopped")