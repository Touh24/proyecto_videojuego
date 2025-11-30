import pygame
import sys
from game import Game

def main():
    # Inicializar Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Crear y ejecutar juego (sin pasar la pantalla como parámetro)
    game = Game()
    game.run()
    
    # Salir
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()