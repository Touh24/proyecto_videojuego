# player.py
import pygame
from config import *
from shapes import ShapeDrawer

class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        
        # Tamaño
        self.width, self.height = SIZES['player']
        
        # Posición inicial - IZQUIERDA de la pantalla
        if player_id == 1:
            self.x = 100  # Izquierda de la pantalla
            self.color = COLORS['player1']
        else:
            self.x = 200  # Izquierda de la pantalla (separado del jugador 1)
            self.color = COLORS['player2']
        
        self.y = PLAYER_START_Y
        self.speed = PLAYER_SPEED
        
        # Crear imagen del jugador (triángulo apuntando hacia la DERECHA)
        self.image = ShapeDrawer.create_surface(self.width, self.height)
        ShapeDrawer.draw_player(self.image, player_id, "right")  # Cambiado a "right"
        
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        # Estado
        self.lives = PLAYER_LIVES
        self.score = 0
        self.shoot_cooldown = 0
        self.is_alive = True
        self.invincible = 0
    
    def update(self, keys=None):
        """Actualiza posición y estado del jugador"""
        if not self.is_alive:
            return
        
        # Reducir cooldowns
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        if self.invincible > 0:
            self.invincible -= 1
        
        # Movimiento según jugador - LIMITADO AL LADO IZQUIERDO
        if self.player_id == 1:
            # Jugador 1 - Flechas
            if keys[pygame.K_LEFT] and self.rect.left > 10:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH // 2:
                self.rect.x += self.speed
            if keys[pygame.K_UP] and self.rect.top > 10:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT - 10:
                self.rect.y += self.speed
        else:
            # Jugador 2 - WASD
            if keys[pygame.K_a] and self.rect.left > 10:
                self.rect.x -= self.speed
            if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH // 2:
                self.rect.x += self.speed
            if keys[pygame.K_w] and self.rect.top > 10:
                self.rect.y -= self.speed
            if keys[pygame.K_s] and self.rect.bottom < SCREEN_HEIGHT - 10:
                self.rect.y += self.speed
    
    def draw(self, screen):
        """Dibuja al jugador en pantalla"""
        if not self.is_alive:
            return
        
        # Efecto de invencibilidad (parpadeo)
        if self.invincible > 0 and self.invincible % 10 < 5:
            return
        
        screen.blit(self.image, self.rect)
        
        # Dibujar nombre debajo
        font = pygame.font.Font(None, 20)
        name = f"J{self.player_id}"
        text = font.render(name, True, self.color)
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.bottom + 15))
        screen.blit(text, text_rect)
    
    def shoot(self):
        """Intenta disparar una bala hacia la DERECHA"""
        if self.shoot_cooldown == 0 and self.is_alive:
            self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
            from bullet import Bullet
            # Disparar desde el lado derecho del jugador
            return Bullet(self.rect.right, self.rect.centery, True, self.player_id)
        return None
    
    def take_damage(self):
        """El jugador recibe daño"""
        if self.invincible > 0:
            return False
        
        self.lives -= 1
        self.invincible = 60
        
        if self.lives <= 0:
            self.is_alive = False
        
        return True