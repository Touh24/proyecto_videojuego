# config.py
import pygame

# Dimensiones de pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# COLORES BÁSICOS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
DARK_BLUE = (10, 10, 40)

# Colores para naves
COLORS = {
    'player1': BLUE,                 # Azul para jugador 1
    'player2': GREEN,                # Verde para jugador 2
    'enemy1': (255, 50, 50),         # Rojo para enemigo 1
    'enemy2': (255, 150, 50),        # Naranja para enemigo 2
    'enemy3': (255, 50, 150),        # Rosa para enemigo 3
    'bullet_player': YELLOW,         # Amarillo para balas jugador
    'bullet_enemy': ORANGE,          # Naranja para balas enemigo
    'background': DARK_BLUE,         # Fondo azul oscuro
    'ui_text': WHITE,                # Texto blanco
    'ui_bg': (0, 0, 0, 180),         # Fondo UI semi-transparente
    'health_bar': (50, 255, 50),     # Verde para barra de vida
    'health_bg': (255, 50, 50),      # Rojo para fondo barra de vida
    'highlight': YELLOW,             # Color destacado (amarillo)
    'progress_low': (255, 50, 50),   # Rojo para progreso bajo
    'progress_medium': (255, 200, 50), # Amarillo para progreso medio
    'progress_high': (50, 255, 50),  # Verde para progreso alto
    'division_line': (100, 100, 100, 100),  # Color línea divisoria
}

# Tamaños
SIZES = {
    'player': (30, 40),              # Ancho, Alto jugador
    'enemy': (25, 35),               # Ancho, Alto enemigo
    'bullet_player': (15, 6),        # Balas jugador (horizontal)
    'bullet_enemy': (8, 8),          # Balas enemigo (cuadrado)
}

# Velocidades
PLAYER_SPEED = 5
ENEMY_SPEED_MIN = 1
ENEMY_SPEED_MAX = 4
BULLET_SPEED = 7

# Juego
FPS = 60
PLAYER_LIVES = 3
ENEMY_SPAWN_RATE = 60               # Frames entre spawns
PLAYER_SHOOT_COOLDOWN = 20          # Frames entre disparos
ENEMY_SHOOT_COOLDOWN = 90           # Frames entre disparos enemigos

# POSICIÓN JUGADORES (en IZQUIERDA)
PLAYER1_START_X = 100                # Jugador 1 cerca del borde izquierdo
PLAYER2_START_X = 200                # Jugador 2 más a la derecha (izquierda)
PLAYER_START_Y = SCREEN_HEIGHT // 2  # Centro vertical

# Límites de movimiento para jugadores (mitad izquierda de pantalla)
PLAYER_MIN_X = 10                    # Límite izquierdo mínimo
PLAYER_MAX_X = SCREEN_WIDTH // 2     # Límite derecho (mitad pantalla)

# ENEMIGOS aparecen por la DERECHA
ENEMY_SPAWN_X = SCREEN_WIDTH + 50    # Fuera de pantalla por derecha
ENEMY_SPAWN_MIN_Y = 50               # Límite superior para aparición
ENEMY_SPAWN_MAX_Y = SCREEN_HEIGHT - 50  # Límite inferior para aparición

# Sistema de puntuación
POINTS_PER_ENEMY = 10
ENEMIES_PER_LEVEL = 10              # Enemigos para subir de nivel