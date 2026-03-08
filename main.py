#!/usr/bin/env python3
"""
OpenF.R.I.D.A.Y. - Main Entry Point
Iron Man AI Assistant (Laptop Test Version)
"""

import yaml
import logging
import sys
from modules.voice_recognition import VoiceListener
from modules.ai_processor import AIProcessor
from modules.tts_engine import TTSEngine
from modules.hud_display import HUDDisplay
from modules.system_monitor import SystemMonitor
from modules.sensor_simulator import SensorSimulator

class OpenFRIDAY:
    def __init__(self, config_path='config.yaml'):
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Setup logging
        logging.basicConfig(
            level=getattr(logging, self.config['system']['log_level']),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize modules
        self.logger.info("Initializing OpenF.R.I.D.A.Y. systems...")
        self.tts = TTSEngine(self.config['voice'])
        self.ai = AIProcessor(self.config['ai'])
        self.voice = VoiceListener(self.config['voice'], self.handle_command)
        self.hud = HUDDisplay(self.config['hud'])
        self.monitor = SystemMonitor()
        self.sensors = SensorSimulator()
        
        self.running = False
        self.logger.info("All systems nominal. F.R.I.D.A.Y. ready.")
    
    def handle_command(self, text):
        """Process voice commands"""
        self.logger.info(f"Command received: {text}")
        
        # Update HUD with what was heard
        self.hud.update_subtitle(f"Heard: {text}")
        
        # Check for system commands first
        if "shutdown" in text.lower() and "friday" in text.lower():
            self.tts.speak("Initiating shutdown sequence. Goodbye.")
            self.running = False
            return
        
        # Get system status
        if "status" in text.lower() or "systems" in text.lower():
            status = self.monitor.get_status()
            response = f"All systems nominal. CPU at {status['cpu_percent']} percent. Memory at {status['memory_percent']} percent."
            self.tts.speak(response)
            self.hud.update_status(status)
            return
        
        # Get sensor data
        if "sensors" in text.lower():
            sensor_data = self.sensors.get_all()
            response = f"Motion detected: {sensor_data['motion']}. Temperature: {sensor_data['temperature']} degrees."
            self.tts.speak(response)
            return
        
        # Default: use AI for response
        response = self.ai.process(text)
        self.tts.speak(response)
        self.hud.update_subtitle(f"F.R.I.D.A.Y.: {response}")
    
    def run(self):
        """Main loop"""
        self.tts.speak("F.R.I.D.A.Y. online. Awaiting your command.")
        self.running = True
        
        # Start HUD in a separate thread
        self.hud.start()
        
        try:
            while self.running:
                # Update HUD with system info
                self.hud.update_status(self.monitor.get_status())
                self.hud.update_sensors(self.sensors.get_all())
                
                # Check for keyboard quit (ESC key)
                import keyboard
                if keyboard.is_pressed('esc'):
                    self.logger.info("ESC pressed, shutting down...")
                    break
                
                # Voice listener runs in its own thread
                # Just keep main thread alive
                import time
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt received")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Clean shutdown"""
        self.logger.info("Shutting down F.R.I.D.A.Y.")
        self.tts.speak("F.R.I.D.A.Y. shutting down.")
        self.hud.stop()
        self.voice.stop()
        sys.exit(0)

if __name__ == "__main__":
    friday = OpenFRIDAY()
    friday.run()