import pygame
import threading
import logging
import time

class HUDDisplay:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.running = False
        self.screen = None
        self.clock = None
        self.thread = None
        
        # Data to display
        self.status = {
            'cpu_percent': 0,
            'memory_percent': 0,
            'temperature': 0,
            'battery': 100
        }
        self.sensors = {
            'motion': 'IDLE',
            'gyro': 'STABLE',
            'gps': 'LOCKED',
            'camera': 'STANDBY'
        }
        self.subtitle = "> AWAITING COMMAND..."
        self.heard_text = ""
        
        # Colors (Iron Man theme)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.ARC_BLUE = (0, 255, 255)
        self.IRON_RED = (255, 50, 50)
        self.HUD_GREEN = (50, 255, 50)
        self.HUD_ORANGE = (255, 165, 0)
        
    def start(self):
        """Start HUD in a separate thread"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_hud)
            self.thread.daemon = True
            self.thread.start()
            self.logger.info("HUD started")
    
    def stop(self):
        """Stop HUD"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        pygame.quit()
        self.logger.info("HUD stopped")
    
    def _run_hud(self):
        """Main HUD loop (runs in thread)"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.config['width'], self.config['height']))
        pygame.display.set_caption("F.R.I.D.A.Y. HUD")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            
            self._draw_hud()
            pygame.display.flip()
            self.clock.tick(30)
        
        pygame.quit()
    
    def _draw_hud(self):
        """Draw all HUD elements"""
        self.screen.fill(self.BLACK)
        
        # Draw targeting reticle (center)
        center_x = self.config['width'] // 2
        center_y = self.config['height'] // 2
        pygame.draw.circle(self.screen, self.ARC_BLUE, (center_x, center_y), 20, 2)
        pygame.draw.line(self.screen, self.ARC_BLUE, (center_x - 30, center_y), (center_x - 10, center_y), 2)
        pygame.draw.line(self.screen, self.ARC_BLUE, (center_x + 10, center_y), (center_x + 30, center_y), 2)
        pygame.draw.line(self.screen, self.ARC_BLUE, (center_x, center_y - 30), (center_x, center_y - 10), 2)
        pygame.draw.line(self.screen, self.ARC_BLUE, (center_x, center_y + 10), (center_x, center_y + 30), 2)
        
        # Draw arc reactor (top-left)
        pygame.draw.circle(self.screen, self.ARC_BLUE, (100, 100), 30, 3)
        pygame.draw.circle(self.screen, self.WHITE, (100, 100), 20, 1)
        
        # System status (top)
        status_text = self.font_large.render("F.R.I.D.A.Y. ONLINE", True, self.HUD_GREEN)
        self.screen.blit(status_text, (50, 20))
        
        # Time (top-right)
        current_time = time.strftime("%H:%M:%S")
        time_text = self.font_medium.render(current_time, True, self.HUD_ORANGE)
        self.screen.blit(time_text, (650, 30))
        
        # System stats (left side)
        stats = [
            ("CPU", f"{self.status['cpu_percent']}%", self.HUD_GREEN),
            ("MEM", f"{self.status['memory_percent']}%", self.HUD_GREEN),
            ("TEMP", f"{self.status['temperature']}°C", self.HUD_ORANGE),
            ("PWR", f"{self.status['battery']}%", self.ARC_BLUE)
        ]
        
        y_offset = 150
        for label, value, color in stats:
            label_surf = self.font_small.render(label, True, self.WHITE)
            value_surf = self.font_medium.render(value, True, color)
            self.screen.blit(label_surf, (30, y_offset))
            self.screen.blit(value_surf, (30, y_offset + 20))
            y_offset += 60
        
        # Sensor data (right side)
        sensors = [
            ("MOTION", self.sensors['motion'], self.HUD_GREEN if self.sensors['motion'] == 'ACTIVE' else self.HUD_ORANGE),
            ("GYRO", self.sensors['gyro'], self.HUD_GREEN),
            ("GPS", self.sensors['gps'], self.ARC_BLUE),
            ("CAM", self.sensors['camera'], self.HUD_ORANGE if self.sensors['camera'] == 'STANDBY' else self.HUD_GREEN)
        ]
        
        y_offset = 150
        for label, value, color in sensors:
            label_surf = self.font_small.render(label, True, self.WHITE)
            value_surf = self.font_medium.render(value, True, color)
            self.screen.blit(label_surf, (650, y_offset))
            self.screen.blit(value_surf, (650, y_offset + 20))
            y_offset += 60
        
        # What F.R.I.D.A.Y. heard (bottom, left)
        if self.heard_text:
            heard_surf = self.font_small.render(f"Heard: {self.heard_text}", True, self.ARC_BLUE)
            self.screen.blit(heard_surf, (50, 350))
        
        # Bottom status line (F.R.I.D.A.Y. response)
        bottom_text = self.font_medium.render(self.subtitle, True, self.ARC_BLUE)
        self.screen.blit(bottom_text, (50, 400))
    
    def update_status(self, status_data):
        """Update system status display"""
        self.status.update(status_data)
    
    def update_sensors(self, sensor_data):
        """Update sensor display"""
        self.sensors.update(sensor_data)
    
    def update_subtitle(self, text):
        """Update the subtitle text"""
        self.subtitle = f"> {text[:50]}..."
        if len(text) < 50:
            self.subtitle = f"> {text}"
    
    def update_heard(self, text):
        """Update what was heard"""
        self.heard_text = text[:40]  # Truncate long text
