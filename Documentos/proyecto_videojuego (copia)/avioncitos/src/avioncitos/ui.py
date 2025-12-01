import pygame
from config import *

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 18)
    
    def draw_text(self, text, font, color, x, y, centered=False):
        """Dibuja texto en la pantalla"""
        text_surface = font.render(text, True, color)
        if centered:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
        return text_rect
    
    def draw_start_screen(self, high_scores, selected_mode=0):
        """Dibuja la pantalla de inicio con selección de modo"""
        self.screen.fill(BLACK)
        
        # Título
        self.draw_text("SPACIAL SOLDIER", self.font_large, WHITE, 
                      SCREEN_WIDTH // 2, 100, centered=True)
        
        # Selección de modo
        self.draw_text("SELECCIONA MODO:", self.font_medium, YELLOW,
                      SCREEN_WIDTH // 2, 180, centered=True)
        
        # Modos de juego
        mode_positions = [240, 290]  # Solo SOLO y MULTIJUGADOR
        for i, mode in enumerate(GAME_MODES):
            color = GREEN if i == selected_mode else WHITE
            self.draw_text(mode, self.font_medium, color,
                          SCREEN_WIDTH // 2, mode_positions[i], centered=True)
        
        # High Scores
        self.draw_text("MEJORES PUNTAJES:", self.font_small, YELLOW,
                      SCREEN_WIDTH // 2, 350, centered=True)
        
        # Mostrar solo los 3 mejores puntajes
        score_positions = [380, 405, 430]
        for i, score in enumerate(high_scores[:3]):
            score_text = f"{i+1}. {score['name']} - {score['score']}"
            self.draw_text(score_text, self.font_small, WHITE,
                          SCREEN_WIDTH // 2, score_positions[i], centered=True)
        
        # Controles
        controls_start_y = 480
        
        # Línea 1: Controles jugador 1
        self.draw_text("Jugador 1:", self.font_tiny, GREEN, 
                      SCREEN_WIDTH // 2, controls_start_y, centered=True)
        self.draw_text("Flechas: Mover | Espacio: Disparar", self.font_tiny, WHITE,
                      SCREEN_WIDTH // 2, controls_start_y + 20, centered=True)
        
        # Línea 2: Controles jugador 2
        self.draw_text("Jugador 2 (Multijugador):", self.font_tiny, CYAN,
                      SCREEN_WIDTH // 2, controls_start_y + 45, centered=True)
        self.draw_text("W/S: Mover | Enter: Disparar", self.font_tiny, WHITE,
                      SCREEN_WIDTH // 2, controls_start_y + 65, centered=True)
        
        # Línea 3: Controles generales
        self.draw_text("ESC: Salir", self.font_tiny, MAGENTA,
                      SCREEN_WIDTH // 2, controls_start_y + 90, centered=True)
        
        pygame.display.flip()
    
    def draw_game_over(self, score, high_scores, is_high_score=False, multiplayer=False, player1_score=0, player2_score=0):
        """Dibuja la pantalla de Game Over"""
        self.screen.fill(BLACK)
        
        # Título
        self.draw_text("GAME OVER", self.font_large, RED,
                      SCREEN_WIDTH // 2, 100, centered=True)
        
        if multiplayer:
            # Mostrar puntajes de ambos jugadores
            self.draw_text(f"Jugador 1: {player1_score}", self.font_medium, GREEN,
                          SCREEN_WIDTH // 2, 180, centered=True)
            self.draw_text(f"Jugador 2: {player2_score}", self.font_medium, CYAN,
                          SCREEN_WIDTH // 2, 220, centered=True)
            
            # Ganador
            if player1_score > player2_score:
                winner_text = "JUGADOR 1 GANA!"
                color = GREEN
            elif player2_score > player1_score:
                winner_text = "JUGADOR 2 GANA!"
                color = CYAN
            else:
                winner_text = "EMPATE!"
                color = YELLOW
            
            self.draw_text(winner_text, self.font_medium, color,
                          SCREEN_WIDTH // 2, 270, centered=True)
            
        else:
            # Modo solo
            self.draw_text(f"Puntaje: {score}", self.font_medium, WHITE,
                          SCREEN_WIDTH // 2, 180, centered=True)
            
            if is_high_score:
                self.draw_text("NUEVO HIGH SCORE!", self.font_medium, YELLOW,
                              SCREEN_WIDTH // 2, 220, centered=True)
            
            # High Scores (solo en modo solo)
            self.draw_text("MEJORES PUNTAJES:", self.font_medium, YELLOW,
                          SCREEN_WIDTH // 2, 280, centered=True)
            
            score_positions = [310, 340, 370]
            for i, hs in enumerate(high_scores[:3]):
                score_text = f"{i+1}. {hs['name']} - {hs['score']}"
                self.draw_text(score_text, self.font_small, WHITE,
                              SCREEN_WIDTH // 2, score_positions[i], centered=True)
        
        # Instrucciones
        self.draw_text("ENTER: Volver al menu", self.font_small, GREEN,
                      SCREEN_WIDTH // 2, 450, centered=True)
        self.draw_text("ESC: Salir", self.font_small, RED,
                      SCREEN_WIDTH // 2, 480, centered=True)
        
        pygame.display.flip()
    
    def draw_game_ui(self, score, lives, level, multiplayer=False, player2_score=0, player2_lives=0, split_screen=False):
        """Dibuja la UI durante el juego"""
        if split_screen and multiplayer:
            # En modo split screen
            screen_height_half = SCREEN_HEIGHT // 2
            
            # Jugador 1 (parte superior)
            self.draw_text(f"P1: {score}", self.font_small, GREEN, 10, 10)
            self.draw_text(f"Vidas: {lives}", self.font_small, GREEN, 10, 30)
            self.draw_text(f"Nivel: {level}", self.font_small, WHITE, SCREEN_WIDTH // 2 - 30, 10)
            
            # Jugador 2 (parte inferior)
            self.draw_text(f"P2: {player2_score}", self.font_small, CYAN, 10, screen_height_half + 10)
            self.draw_text(f"Vidas: {player2_lives}", self.font_small, CYAN, 10, screen_height_half + 30)
        else:
            # UI normal
            self.draw_text(f"Puntaje: {score}", self.font_small, GREEN, 10, 10)
            self.draw_text(f"Vidas: {lives}", self.font_small, GREEN, 10, 30)
            self.draw_text(f"Nivel: {level}", self.font_small, WHITE, SCREEN_WIDTH - 100, 10)
            
            # Jugador 2 (solo en multijugador)
            if multiplayer:
                self.draw_text(f"P2: {player2_score}", self.font_small, CYAN, SCREEN_WIDTH - 100, 30)
                self.draw_text(f"Vidas P2: {player2_lives}", self.font_small, CYAN, SCREEN_WIDTH - 100, 50)
    
    def get_player_name(self):
        """Obtiene el nombre del jugador para el high score"""
        name = ""
        input_active = True
        
        while input_active:
            self.screen.fill(BLACK)
            
            self.draw_text("NUEVO HIGH SCORE!", self.font_large, YELLOW,
                          SCREEN_WIDTH // 2, 150, centered=True)
            self.draw_text("Ingresa tu nombre (3 letras):", self.font_medium, WHITE,
                          SCREEN_WIDTH // 2, 220, centered=True)
            self.draw_text(name + "_", self.font_medium, GREEN,
                          SCREEN_WIDTH // 2, 270, centered=True)
            self.draw_text("ENTER: Continuar", self.font_small, WHITE,
                          SCREEN_WIDTH // 2, 320, centered=True)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "AAA"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.unicode.isalnum() and len(name) < 3:
                        name += event.unicode.upper()
        
        return name if name else "AAA"