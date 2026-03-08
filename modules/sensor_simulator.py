import random
import logging
import time

class SensorSimulator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.last_motion_time = time.time()
        
    def get_all(self):
        """Get all simulated sensor data"""
        return {
            'motion': self._get_motion(),
            'gyro': self._get_gyro(),
            'gps': self._get_gps(),
            'camera': self._get_camera()
        }
    
    def _get_motion(self):
        """Simulate motion detection"""
        # Randomly detect motion (10% chance)
        if random.random() < 0.1:
            self.last_motion_time = time.time()
            return "ACTIVE"
        elif time.time() - self.last_motion_time < 2:
            return "ACTIVE"
        else:
            return "IDLE"
    
    def _get_gyro(self):
        """Simulate gyro/IMU data"""
        # Most of the time stable, occasionally moving
        if random.random() < 0.05:
            return "MOVING"
        return "STABLE"
    
    def _get_gps(self):
        """Simulate GPS status"""
        # Usually locked, occasionally searching
        if random.random() < 0.02:
            return "SEARCHING"
        return "LOCKED"
    
    def _get_camera(self):
        """Simulate camera status"""
        # Randomly switch between modes
        r = random.random()
        if r < 0.1:
            return "ACTIVE"
        elif r < 0.15:
            return "FOCUSING"
        else:
            return "STANDBY"
    
    def get_motion(self):
        """Get just motion data"""
        return self._get_motion()
    
    def get_gyro(self):
        """Get just gyro data"""
        return self._get_gyro()
    
    def get_gps(self):
        """Get just GPS data"""
        return self._get_gps()
    
    def get_camera(self):
        """Get just camera data"""
        return self._get_camera()
