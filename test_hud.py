#!/usr/bin/env python3
"""
Simple HUD test for F.R.I.D.A.Y.
"""

import pygame
import sys
import time

def test_hud():
    print("Starting HUD test...")
    
    # Initialize pygame
    pygame.init()
    
    # Set up display (800x480 is typical for small HUDs)
    screen = pygame.display.set_mode((800, 480))
    pygame.display.set_caption("F.R.I.D.A.Y. HUD Test")
    
    # Colors (Iron Man theme)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    ARC_REACTOR_BLUE = (0, 255, 255)
    IRON_MAN_RED = (255, 50, 50)
    HUD_GREEN = (50, 255, 50)
    HUD_ORANGE = (255, 165, 0)
    
    # Fonts
    font_large = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 24)
    
    clock = pygame.time.Clock()
    running = True
    start_time = time.time()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Clear screen with black (transparent-looking)
        screen.fill(BLACK)
        
        # Draw targeting reticle (center)
        center_x, center_y = 400, 240
        pygame.draw.circle(screen, ARC_REACTOR_BLUE, (center_x, center_y), 20, 2)
        pygame.draw.line(screen, ARC_REACTOR_BLUE, (center_x - 30, center_y), (center_x - 10, center_y), 2)
        pygame.draw.line(screen, ARC_REACTOR_BLUE, (center_x + 10, center_y), (center_x + 30, center_y), 2)
        pygame.draw.line(screen, ARC_REACTOR_BLUE, (center_x, center_y - 30), (center_x, center_y - 10), 2)
        pygame.draw.line(screen, ARC_REACTOR_BLUE, (center_x, center_y + 10), (center_x, center_y + 30), 2)
        
        # Draw arc reactor style circle (top-left)
        pygame.draw.circle(screen, ARC_REACTOR_BLUE, (100, 100), 30, 3)
        pygame.draw.circle(screen, WHITE, (100, 100), 20, 1)
        
        # System status (top)
        status_text = font_large.render("F.R.I.D.A.Y. ONLINE", True, HUD_GREEN)
        screen.blit(status_text, (50, 20))
        
        # Time (top-right)
        elapsed = int(time.time() - start_time)
        time_text = font_medium.render(f"TIME: {elapsed:03d}", True, HUD_ORANGE)
        screen.blit(time_text, (650, 30))
        
        # System stats (left side)
        stats = [
            ("CPU", "45%", HUD_GREEN),
            ("MEM", "32%", HUD_GREEN),
            ("TEMP", "38°C", HUD_ORANGE),
            ("PWR", "98%", ARC_REACTOR_BLUE)
        ]
        
        y_offset = 150
        for label, value, color in stats:
            label_surf = font_small.render(label, True, WHITE)
            value_surf = font_medium.render(value, True, color)
            screen.blit(label_surf, (30, y_offset))
            screen.blit(value_surf, (30, y_offset + 20))
            y_offset += 60
        
        # Sensor data (right side)
        sensors = [
            ("MOTION", "ACTIVE", HUD_GREEN),
            ("GYRO", "STABLE", HUD_GREEN),
            ("GPS", "LOCKED", ARC_REACTOR_BLUE),
            ("CAM", "STANDBY", HUD_ORANGE)
        ]
        
        y_offset = 150
        for label, value, color in sensors:
            label_surf = font_small.render(label, True, WHITE)
            value_surf = font_medium.render(value, True, color)
            screen.blit(label_surf, (650, y_offset))
            screen.blit(value_surf, (650, y_offset + 20))
            y_offset += 60
        
        # Bottom status line (like F.R.I.D.A.Y. would speak)
        bottom_text = font_medium.render("> AWAITING COMMAND...", True, ARC_REACTOR_BLUE)
        screen.blit(bottom_text, (50, 400))
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("HUD test complete")

if __name__ == "__main__":
    test_hud()
