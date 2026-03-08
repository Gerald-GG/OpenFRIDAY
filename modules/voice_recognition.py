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
        
        # More sensitive settings
        self.recognizer.energy_threshold = 300  # Lower = more sensitive
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8  # Shorter pause detection
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5
        
        self.listening = False
        self.thread = None
        
        # Multiple wake word variations
        self.wake_words = [
            "hey friday",
            "hey f.r.i.d.a.y.",
            "friday",
            "hey there friday",
            "okay friday"
        ]
        
        try:
            self.microphone = sr.Microphone()
            # Adjust for ambient noise
            with self.microphone as source:
                print("🎤 Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                print(f"🎤 Energy threshold set to: {self.recognizer.energy_threshold}")
        except Exception as e:
            self.logger.error(f"Failed to initialize microphone: {e}")
            print(f"❌ Microphone error: {e}")
            self.microphone = None
        
        self.logger.info("Voice listener initialized")
        print("🎤 Voice listener ready - waiting for 'Hey F.R.I.D.A.Y.'")
        
        # Start listening thread
        self.start()
    
    def listen_loop(self):
        """Main listening loop"""
        if not self.microphone:
            self.logger.error("No microphone available")
            return
            
        while self.listening:
            try:
                with self.microphone as source:
                    self.logger.debug("Listening for wake word...")
                    print(".", end="", flush=True)  # Tiny indicator that we're listening
                    
                    # Listen for audio
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                    print("\n🎤 Processing audio...")
                    
                # Try to recognize speech
                try:
                    text = self.recognizer.recognize_google(audio).lower()
                    print(f"📝 Recognized: '{text}'")
                    
                    # Check for any wake word
                    wake_word_detected = False
                    command = text
                    
                    for wake_word in self.wake_words:
                        if wake_word in text:
                            wake_word_detected = True
                            # Remove wake word from command
                            command = text.replace(wake_word, '').strip()
                            print(f"🔵 Wake word '{wake_word}' detected!")
                            break
                    
                    # Also treat as command if no wake word but we're in "always listening" mode
                    # For now, let's enable this for testing
                    if not wake_word_detected:
                        # For testing, also respond to common commands without wake word
                        test_commands = ["time", "status", "sensors", "joke", "hello", "hi"]
                        if any(cmd in text for cmd in test_commands):
                            print(f"🔵 Direct command detected (no wake word)!")
                            wake_word_detected = True
                            command = text
                    
                    if wake_word_detected and command:
                        print(f"🎯 Command: '{command}'")
                        self.callback(command)
                    elif wake_word_detected and not command:
                        print(f"🎯 Just wake word")
                        self.callback("Yes, I'm listening?")
                    
                except sr.UnknownValueError:
                    # Couldn't understand - ignore silently
                    pass
                except sr.RequestError as e:
                    self.logger.error(f"Speech recognition error: {e}")
                    print(f"\n❌ Recognition error: {e}")
                    
            except sr.WaitTimeoutError:
                # No speech detected - normal, just continue
                pass
            except Exception as e:
                self.logger.error(f"Error in listen loop: {e}")
                print(f"\n❌ Loop error: {e}")
                time.sleep(1)
    
    def start(self):
        """Start listening thread"""
        if not self.listening and self.microphone:
            self.listening = True
            self.thread = threading.Thread(target=self.listen_loop)
            self.thread.daemon = True
            self.thread.start()
            self.logger.info("Voice listener started")
            print("🎤 Listening for wake word...")
    
    def stop(self):
        """Stop listening"""
        self.listening = False
        if self.thread:
            self.thread.join(timeout=2)
        self.logger.info("Voice listener stopped")
        print("🎤 Voice listener stopped")
