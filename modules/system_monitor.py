import psutil
import logging
import platform

class SystemMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_status(self):
        """Get current system status"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Temperature (if available)
            temp = self._get_cpu_temperature()
            
            # Battery (if available)
            battery = self._get_battery_status()
            
            status = {
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'temperature': temp,
                'battery': battery
            }
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error getting system status: {e}")
            return {
                'cpu_percent': 0,
                'memory_percent': 0,
                'temperature': 0,
                'battery': 100
            }
    
    def _get_cpu_temperature(self):
        """Get CPU temperature (platform specific)"""
        try:
            if platform.system() == 'Linux':
                # Try to read from thermal zone
                with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                    temp = int(f.read()) / 1000.0
                    return round(temp, 1)
        except:
            pass
        return 45  # Default mock temperature
    
    def _get_battery_status(self):
        """Get battery percentage"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                return round(battery.percent)
        except:
            pass
        return 100  # Default if no battery
