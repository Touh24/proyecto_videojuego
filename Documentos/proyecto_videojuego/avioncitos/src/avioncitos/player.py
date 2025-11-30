import pygame
from config import *

class Player:
    def __init__(self, player_num=1):
        self.player_num = player_num
        if player_num == 1:
            self.rect = pygame.Rect(PLAYER1_START_X, SCREEN_HEIGHT // 4, PLAYER_WIDTH, PLAYER_HEIGHT)
            self.color = PLAYER_COLOR
        else:
            # Jugador 2 también en lado izquierdo pero en mitad inferior
            self.rect = pygame.Rect(PLAYER1_START_X, SCREEN_HEIGHT * 3 // 4, PLAYER_WIDTH, PLAYER_HEIGHT)
            self.color = PLAYER2_COLOR
        
        self.speed = PLAYER_SPEED
        self.lives = INITIAL_LIVES
        self.score = 0
    
    def move(self, direction):
        """Mueve al jugador (arriba/abajo)"""
        if direction == "up" and self.rect.top > 0:
            self.rect.y -= self.speed
        elif direction == "down" and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
    
    def shoot(self):
        """Crea una nueva bala"""
        # Ambos jugadores disparan hacia la derecha
        bullet_rect = pygame.Rect(
            self.rect.right,
            self.rect.centery - BULLET_HEIGHT // 2,
            BULLET_WIDTH,
            BULLET_HEIGHT
        )
        return bullet_rect
    
    def take_damage(self):
        """Reduce una vida"""
        self.lives -= 1
        return self.lives <= 0
    
    def draw(self, screen):
        """Dibuja al jugador"""
        pygame.draw.rect(screen, self.color, self.rect)
        # Dibujar el cañón (ambos apuntan a la derecha)
        pygame.draw.rect(screen, self.color, 
                        (self.rect.right - 10, self.rect.centery - 5, 15, 10))
    
    def reset(self):
        """Reinicia el jugador a su estado inicial"""
        if self.player_num == 1:
            self.rect.y = SCREEN_HEIGHT // 4  # Mitad superior
        else:
            self.rect.y = SCREEN_HEIGHT * 3 // 4  # Mitad inferior
        self.lives = INITIAL_LIVES
        self.score = 0