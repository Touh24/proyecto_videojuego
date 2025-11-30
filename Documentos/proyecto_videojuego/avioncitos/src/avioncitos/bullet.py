import pygame
from config import *

class Bullet:
    def __init__(self, rect, player_num=1):
        self.rect = rect
        self.speed = BULLET_SPEED
        self.player_num = player_num
        self.color = BULLET_COLOR if player_num == 1 else BULLET2_COLOR
    
    def update(self):
        """Mueve la bala hacia la derecha (ambos jugadores)"""
        self.rect.x += self.speed
        return self.rect.left > SCREEN_WIDTH  # Devuelve True si sale de la pantalla
    
    def draw(self, screen):
        """Dibuja la bala"""
        pygame.draw.rect(screen, self.color, self.rect)