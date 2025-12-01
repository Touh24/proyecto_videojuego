# main.py
import pygame
import sys
from game import Game

def main():
    # Inicializar Pygame
    pygame.init()
    
    # Crear y ejecutar juego
    game = Game()
    game.run()
    
    # Salir
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()