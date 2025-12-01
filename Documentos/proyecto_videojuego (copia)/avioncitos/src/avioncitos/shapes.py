# shapes.py
import pygame
import math
from config import COLORS, SIZES, WHITE

class ShapeDrawer:
    @staticmethod
    def create_surface(width, height):
        """Crea una superficie transparente"""
        return pygame.Surface((width, height), pygame.SRCALPHA)
    
    @staticmethod
    def draw_player(surface, player_id, direction="right"):
        """Dibuja nave jugador apuntando hacia la DERECHA"""
        width, height = SIZES['player']
        
        # Color según jugador
        if player_id == 1:
            color = COLORS['player1']
            detail_color = (150, 200, 255)
        else:
            color = COLORS['player2']
            detail_color = (150, 255, 200)
        
        # Triángulo apuntando hacia la DERECHA
        # PUNTA en DERECHA, BASE en IZQUIERDA
        points = [
            (width - 10, height // 2),   # Punta DERECHA
            (5, 10),                     # Superior IZQUIERDA  
            (5, height - 10)             # Inferior IZQUIERDA
        ]
        
        # Cuerpo principal
        pygame.draw.polygon(surface, color, points)
        
        # Borde blanco
        pygame.draw.polygon(surface, WHITE, points, 2)
        
        # Motor en la parte trasera (izquierda, base del triángulo)
        pygame.draw.circle(surface, detail_color, 
                         (10, height // 2), 5)
        
        return surface
    
    @staticmethod
    def draw_enemy(surface, enemy_type, direction="left"):
        """Dibuja nave enemiga apuntando hacia la IZQUIERDA"""
        width, height = SIZES['enemy']
        
        # Color según tipo
        if enemy_type == 1:
            color = COLORS['enemy1']
            detail_color = (255, 150, 150)
        elif enemy_type == 2:
            color = COLORS['enemy2']
            detail_color = (255, 200, 150)
        else:
            color = COLORS['enemy3']
            detail_color = (255, 150, 200)
        
        # Triángulo apuntando hacia la IZQUIERDA
        # PUNTA en IZQUIERDA, BASE en DERECHA
        points = [
            (10, height // 2),           # Punta IZQUIERDA
            (width - 5, 10),             # Superior DERECHA
            (width - 5, height - 10)     # Inferior DERECHA
        ]
        
        # Cuerpo
        pygame.draw.polygon(surface, color, points)
        
        # Borde
        pygame.draw.polygon(surface, detail_color, points, 2)
        
        # Ojos en el centro (más hacia la derecha, cerca de la base)
        eye_x = width * 2 // 3  # Más a la derecha
        
        if enemy_type == 1:
            pygame.draw.circle(surface, (255, 255, 200),
                             (eye_x, height // 2), 4)
        elif enemy_type == 2:
            pygame.draw.circle(surface, (255, 255, 200),
                             (eye_x - 3, height // 2), 3)
            pygame.draw.circle(surface, (255, 255, 200),
                             (eye_x + 3, height // 2), 3)
        else:
            pygame.draw.circle(surface, (255, 200, 200),
                             (eye_x, height // 2), 6)
            pygame.draw.circle(surface, WHITE,
                             (eye_x, height // 2), 2)
        
        return surface
    
    @staticmethod
    def draw_bullet(surface, is_player=True, player_id=1):
        """Dibuja una bala horizontal"""
        if is_player:
            width, height = SIZES['bullet_player']
            if player_id == 1:
                color = COLORS['player1']
            else:
                color = COLORS['player2']
            
            # Bala del JUGADOR (va hacia la DERECHA)
            pygame.draw.rect(surface, color, (0, 0, width, height))
            
            # Punta brillante en la DERECHA (porque va hacia derecha)
            pygame.draw.rect(surface, (255, 255, 200),
                            (width - width//3, 0, width//3, height))
            
            # Estela a la IZQUIERDA (porque viene del jugador en la izquierda)
            for i in range(3):
                x_pos = -(i * 3) - 2
                alpha = 150 - (i * 50)
                trail_color = (color[0], color[1], color[2], alpha)
                temp_surf = pygame.Surface((2, height), pygame.SRCALPHA)
                temp_surf.fill(trail_color)
                surface.blit(temp_surf, (x_pos, 0))
        else:
            # Bala del ENEMIGO (va hacia la IZQUIERDA)
            width, height = SIZES['bullet_enemy']
            color = COLORS['bullet_enemy']
            
            pygame.draw.rect(surface, color, (0, 0, width, height))
            
            # Punta brillante en la IZQUIERDA (porque va hacia izquierda)
            pygame.draw.rect(surface, (255, 220, 180),
                            (0, 0, width//3, height))
            
            # Estela a la DERECHA (porque viene del enemigo en la derecha)
            for i in range(3):
                x_pos = width + (i * 3)
                alpha = 150 - (i * 50)
                trail_color = (color[0], color[1], color[2], alpha)
                temp_surf = pygame.Surface((2, height), pygame.SRCALPHA)
                temp_surf.fill(trail_color)
                surface.blit(temp_surf, (x_pos, 0))
        
        return surface
    
    @staticmethod
    def draw_particle(surface, x, y, color, size=3):
        """Dibuja una partícula simple"""
        pygame.draw.circle(surface, color, (x, y), size)
        return surface
    
    @staticmethod
    def draw_health_bar(surface, x, y, width, height, health, max_health):
        """Dibuja una barra de vida"""
        # Fondo rojo
        pygame.draw.rect(surface, COLORS['health_bg'], 
                        (x, y, width, height))
        
        # Vida verde
        health_width = int((health / max_health) * width)
        pygame.draw.rect(surface, COLORS['health_bar'],
                        (x, y, health_width, height))
        
        # Borde blanco
        pygame.draw.rect(surface, WHITE, (x, y, width, height), 1)
        
        return surface
    
    @staticmethod
    def draw_division_line(surface, screen_width, screen_height, is_multiplayer):
        """Dibuja línea divisoria HORIZONTAL solo en multijugador"""
        if not is_multiplayer:
            return
        
        # Línea horizontal en el centro
        line_y = screen_height // 2
        
        # Línea principal
        pygame.draw.line(surface, COLORS['division_line'],
                        (0, line_y), (screen_width, line_y), 2)
        
        # Texto "J1" arriba, "J2" abajo
        font = pygame.font.Font(None, 24)
        
        # Jugador 1 arriba
        j1_text = font.render("JUGADOR 1", True, COLORS['player1'])
        j1_rect = j1_text.get_rect(center=(screen_width // 2, line_y - 20))
        surface.blit(j1_text, j1_rect)
        
        # Jugador 2 abajo
        j2_text = font.render("JUGADOR 2", True, COLORS['player2'])
        j2_rect = j2_text.get_rect(center=(screen_width // 2, line_y + 20))
        surface.blit(j2_text, j2_rect)