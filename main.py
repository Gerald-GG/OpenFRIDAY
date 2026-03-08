#!/usr/bin/env python3
"""
OpenF.R.I.D.A.Y. - Main Entry Point
Iron Man AI Assistant (Laptop Test Version)
"""

import yaml
import logging
import sys
import os
import time
from pathlib import Path

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    env_file = Path('.env')
    if env_file.exists():
        load_dotenv()
        print("📁 Loaded environment variables from .env file")
    else:
        print("📁 No .env file found, using system environment variables")
except ImportError:
    print("📁 python-dotenv not installed, using system environment variables only")

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
        
        print("\n" + "="*50)
        print("🔵 OpenF.R.I.D.A.Y. - Initializing Systems")
        print("="*50)
        
        # Initialize modules
        self.logger.info("Initializing OpenF.R.I.D.A.Y. systems...")
        
        print("⚡ Initializing Text-to-Speech...")
        self.tts = TTSEngine(self.config['voice'])
        
        print("🧠 Initializing AI Processor...")
        self.ai = AIProcessor(self.config['ai'])
        
        print("🎤 Initializing Voice Recognition...")
        self.voice = VoiceListener(self.config['voice'], self.handle_command)
        
        print("📺 Initializing HUD Display...")
        self.hud = HUDDisplay(self.config['hud'])
        
        print("📊 Initializing System Monitor...")
        self.monitor = SystemMonitor()
        
        print("📡 Initializing Sensor Simulator...")
        self.sensors = SensorSimulator()
        
        self.running = False
        self.logger.info("All systems nominal. F.R.I.D.A.Y. ready.")
        print("="*50 + "\n")
    
    def handle_command(self, text):
        """Process voice commands"""
        self.logger.info(f"Command received: {text}")
        print(f"\n🎤 You said: {text}")
        
        # Update HUD with what was heard
        self.hud.update_heard(text)
        
        text_lower = text.lower()
        
        # ===== SYSTEM COMMANDS =====
        if "shutdown" in text_lower and "friday" in text_lower:
            response = "Initiating shutdown sequence. Goodbye."
            print(f"🔵 F.R.I.D.A.Y.: {response}")
            self.tts.speak(response)
            self.running = False
            return
        
        # ===== SYSTEM STATUS =====
        # Only handle pure system status queries, not device status
        if ("status" in text_lower or "systems" in text_lower) and "device" not in text_lower and "smart" not in text_lower:
            status = self.monitor.get_status()
            response = f"All systems nominal. CPU at {status['cpu_percent']} percent. Memory at {status['memory_percent']} percent."
            print(f"🔵 F.R.I.D.A.Y.: {response}")
            self.tts.speak(response)
            self.hud.update_status(status)
            return
        
        # ===== SENSOR DATA =====
        if "sensors" in text_lower:
            sensor_data = self.sensors.get_all()
            response = f"Motion is {sensor_data['motion'].lower()}. Gyro is {sensor_data['gyro'].lower()}. GPS is {sensor_data['gps'].lower()}. Camera is on {sensor_data['camera'].lower()}."
            print(f"🔵 F.R.I.D.A.Y.: {response}")
            self.tts.speak(response)
            return
        
        # ===== ALL OTHER COMMANDS GO TO AI PROCESSOR =====
        # This includes weather, news, smart home, jokes, etc.
        response = self.ai.process(text)
        print(f"🔵 F.R.I.D.A.Y.: {response}")
        self.tts.speak(response)
        self.hud.update_subtitle(response)
    
    def run(self):
        """Main loop"""
        welcome = "F.R.I.D.A.Y. online. Awaiting your command."
        print(f"🔵 {welcome}")
        self.tts.speak(welcome)
        self.running = True
        
        # Start HUD in a separate thread
        self.hud.start()
        
        try:
            print("\n" + "-"*50)
            print("🎯 System Ready! Just speak naturally:")
            print("   • 'What's the weather?'")
            print("   • 'Read me the news'")
            print("   • 'Turn on the lights'")
            print("   • 'Set thermostat to 72'")
            print("   • 'What's my device status?'")
            print("   • 'Tell me a joke'")
            print("   • 'What time is it?'")
            print("   • 'Shutdown F.R.I.D.A.Y.'")
            print("-"*50 + "\n")
            print("💡 Press Ctrl+C in this terminal to exit")
            print("")
            
            while self.running:
                # Update HUD with system info every second
                self.hud.update_status(self.monitor.get_status())
                self.hud.update_sensors(self.sensors.get_all())
                
                # Simple counter to show system is alive
                for i in range(10):
                    if not self.running:
                        break
                    time.sleep(0.1)
                
        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt received")
            print("\n⚠️ Interrupted - shutting down...")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            print(f"\n❌ Error: {e}")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Clean shutdown"""
        print("\n" + "="*50)
        print("🔵 Shutting down F.R.I.D.A.Y. systems...")
        self.logger.info("Shutting down F.R.I.D.A.Y.")
        
        # Stop all modules
        if hasattr(self, 'hud'):
            self.hud.stop()
        
        if hasattr(self, 'voice'):
            self.voice.stop()
        
        if hasattr(self, 'tts'):
            self.tts.stop()
        
        print("✅ Shutdown complete. Goodbye!")
        print("="*50)
        sys.exit(0)

if __name__ == "__main__":
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        print("🐛 Debug mode enabled")
    
    # Create and run F.R.I.D.A.Y.
    friday = OpenFRIDAY()
    friday.run()
