import pygame
import os

# Configuración general
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Configuración del jugador
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 30
PLAYER_SPEED = 5
PLAYER1_START_X = 50
PLAYER2_START_X = 700
PLAYER_COLOR = GREEN
PLAYER2_COLOR = CYAN

# Configuración de enemigos
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 30
ENEMY_SPEED_BASE = 2
ENEMY_SPEED_INCREMENT = 1
ENEMY_SPAWN_RATE = 60  # frames entre spawns
ENEMY_COLOR = RED

# Configuración de balas
BULLET_WIDTH = 10
BULLET_HEIGHT = 5
BULLET_SPEED = 10
BULLET_COLOR = YELLOW
BULLET2_COLOR = BLUE

# Configuración de juego
INITIAL_LIVES = 3
POINTS_PER_ENEMY = 10
ENEMIES_PER_LEVEL = 10
MAX_LEVEL = 3

# Modos de juego (eliminamos CONFIGURACIÓN)
GAME_MODES = ["SOLO", "MULTIJUGADOR"]

# Rutas de archivos
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "..", "assets")
HIGHSCORES_FILE = "highscores.json"