import pygame
import random
from config import *

class Enemy:
    def __init__(self, level=1):
        self.speed = ENEMY_SPEED_BASE + (level - 1) * ENEMY_SPEED_INCREMENT
        self.rect = pygame.Rect(
            SCREEN_WIDTH,
            random.randint(0, SCREEN_HEIGHT - ENEMY_HEIGHT),
            ENEMY_WIDTH,
            ENEMY_HEIGHT
        )
        self.color = RED
    
    def update(self):
        """Mueve el enemigo hacia la izquierda"""
        self.rect.x -= self.speed
        return self.rect.right < 0  # Devuelve True si sale de la pantalla
    
    def draw(self, screen):
        """Dibuja el enemigo"""
        pygame.draw.rect(screen, self.color, self.rect)
        # Dibujar las alas
        pygame.draw.polygon(screen, self.color, [
            (self.rect.left, self.rect.top),
            (self.rect.left - 10, self.rect.centery),
            (self.rect.left, self.rect.bottom)
        ])
    
    def collides_with(self, rect):
        """Verifica colisión con otro rectángulo"""
        return self.rect.colliderect(rect)