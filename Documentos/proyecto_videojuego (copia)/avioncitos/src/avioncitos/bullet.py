# bullet.py
import pygame
from config import *
from shapes import ShapeDrawer

class Bullet:
    def __init__(self, x, y, is_player=True, player_id=1):
        self.is_player = is_player
        self.player_id = player_id
        
        # Tamaño según tipo
        if is_player:
            self.width, self.height = SIZES['bullet_player']  # Horizontal
            self.speed = BULLET_SPEED  # Hacia la IZQUIERDA (negativo)
            self.damage = 1
        else:
            self.width, self.height = SIZES['bullet_enemy']  # Cuadrado
            self.speed = -BULLET_SPEED  # Hacia la DERECHA (positivo)
            self.damage = 1
        
        # Posición
        self.x = x
        self.y = y
        
        # Crear imagen
        self.image = ShapeDrawer.create_surface(self.width, self.height)
        ShapeDrawer.draw_bullet(self.image, is_player, self.player_id if is_player else 0)
        
        # Rectángulo para colisiones
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def update(self):
        """Actualiza posición de la bala - Movimiento HORIZONTAL"""
        self.x += self.speed  # Movimiento horizontal
        self.rect.center = (self.x, self.y)
    
    def draw(self, screen):
        """Dibuja la bala en pantalla"""
        screen.blit(self.image, self.rect)
    
    def is_off_screen(self):
        """Verifica si la bala salió de pantalla"""
        if self.is_player:
            return self.rect.right < 0  # Izquierda de la pantalla
        else:
            return self.rect.left > SCREEN_WIDTH  # Derecha de la pantalla