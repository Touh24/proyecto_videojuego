# enemy.py
import pygame
import random
import math
from config import *
from shapes import ShapeDrawer

class Enemy:
    def __init__(self, enemy_type=1, level=1):
        self.enemy_type = enemy_type
        self.level = level
        
        # Características según tipo
        if enemy_type == 1:
            self.color = COLORS['enemy1']
            self.speed = random.uniform(ENEMY_SPEED_MIN, ENEMY_SPEED_MIN + 1)
            self.health = 1
            self.points = POINTS_PER_ENEMY
        elif enemy_type == 2:
            self.color = COLORS['enemy2']
            self.speed = random.uniform(ENEMY_SPEED_MIN + 0.5, ENEMY_SPEED_MAX - 1)
            self.health = 2
            self.points = POINTS_PER_ENEMY * 1.5
        else:
            self.color = COLORS['enemy3']
            self.speed = random.uniform(ENEMY_SPEED_MAX - 1, ENEMY_SPEED_MAX)
            self.health = 3
            self.points = POINTS_PER_ENEMY * 2
        
        # Tamaño
        self.width, self.height = SIZES['enemy']
        
        # POSICIÓN FIJA - LADO DERECHO de la pantalla
        self.x = SCREEN_WIDTH + 50  # Fuera de pantalla por la derecha
        self.y = random.randint(ENEMY_SPAWN_MIN_Y, ENEMY_SPAWN_MAX_Y)
        
        # Crear imagen del enemigo (triángulo apuntando hacia la IZQUIERDA)
        self.image = ShapeDrawer.create_surface(self.width, self.height)
        ShapeDrawer.draw_enemy(self.image, enemy_type, "left")  # Cambiado a "left"
        
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        # Estado
        self.shoot_cooldown = random.randint(0, ENEMY_SHOOT_COOLDOWN)
        self.is_alive = True
        self.oscillation = random.uniform(0, 3.14)
        self.oscillation_speed = random.uniform(0.05, 0.15)
        self.direction = -1  # Se mueve hacia la IZQUIERDA (hacia los jugadores)
    
    def update(self):
        """Actualiza posición del enemigo - Se mueve hacia la IZQUIERDA"""
        if not self.is_alive:
            return
        
        # Movimiento hacia la IZQUIERDA
        self.x += self.speed * self.direction
        self.rect.center = (self.x, self.y)
        
        # Movimiento vertical oscilante
        if self.enemy_type > 1:
            self.oscillation += self.oscillation_speed
            self.y += math.sin(self.oscillation) * 1.5
            self.rect.centery = int(self.y)
        
        # Actualizar cooldown de disparo
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def draw(self, screen):
        """Dibuja el enemigo en pantalla"""
        if self.is_alive:
            screen.blit(self.image, self.rect)
            
            # Mostrar salud para enemigos con más de 1 vida
            if self.health > 1:
                bar_width = 30
                bar_height = 4
                bar_x = self.rect.centerx - bar_width // 2
                bar_y = self.rect.bottom + 5
                ShapeDrawer.draw_health_bar(screen, bar_x, bar_y, 
                                          bar_width, bar_height,
                                          self.health, 
                                          3 if self.enemy_type == 3 else 2)
            
            # Mostrar tipo del enemigo
            type_text = str(self.enemy_type)
            font = pygame.font.Font(None, 16)
            type_surface = font.render(type_text, True, WHITE)
            type_rect = type_surface.get_rect(center=(self.rect.centerx, self.rect.top - 10))
            screen.blit(type_surface, type_rect)
    
    def shoot(self):
        """El enemigo dispara una bala hacia la IZQUIERDA"""
        if self.shoot_cooldown == 0 and self.is_alive:
            self.shoot_cooldown = ENEMY_SHOOT_COOLDOWN + random.randint(-30, 30)
            from bullet import Bullet
            # Disparar desde el lado izquierdo del enemigo
            return Bullet(self.rect.left, self.rect.centery, False)
        return None
    
    def take_damage(self, damage=1):
        """El enemigo recibe daño"""
        self.health -= damage
        
        if self.health <= 0:
            self.is_alive = False
            return int(self.points)
        
        return 0
    
    def is_off_screen(self):
        """Verifica si el enemigo salió de pantalla por la IZQUIERDA"""
        return self.rect.right < 0  # Cambiado: sale por la izquierda