# game.py - VERSIÓN COMPLETA CON AUDIO Y TÍTULO CORREGIDO
import pygame
import random
import math
from config import *
from player import Player
from enemy import Enemy
from bullet import Bullet
from shapes import ShapeDrawer
from highscores import HighScores
from audio import AudioManager  # IMPORTAR AudioManager

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("SPACIAL SOLDIER - Juego Retro")
        
        # Sistema de audio
        self.audio = AudioManager()
        self.audio.play_music(loop=-1)  # -1 para loop infinito
        
        # Sistema de records
        self.high_scores = HighScores()
        
        # Estado del juego
        self.running = True
        self.game_state = "menu"  # menu, playing_solo, playing_multi, game_over, enter_name
        self.score = 0
        self.level = 1
        self.enemies_killed = 0
        self.paused = False
        
        # Jugadores
        self.player = Player(1)
        self.player2 = None
        
        # Grupos de objetos
        self.enemies = []
        self.bullets = []
        self.particles = []
        self.explosions = []
        
        # Tiempo y contadores
        self.enemy_spawn_timer = 0
        self.game_over_timer = 0
        
        # Menú - Opciones y selección
        self.menu_options = ["Un Jugador", "Multijugador", "Ver Records", "Salir"]
        self.selected_option = 0  # Índice de opción seleccionada
        
        # Entrada de nombre para nuevo record
        self.player_name = ""
        self.name_cursor_pos = 0
        self.name_cursor_blink = 0
        self.is_new_record = False
        
        # Fuentes
        self.font_large = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 18)
    
    def handle_events(self):
        """Maneja los eventos del juego"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                # Menú principal
                if self.game_state == "menu":
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                        self.audio.play_sound('shoot')
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                        self.audio.play_sound('shoot')
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.audio.play_sound('enemy_shoot')
                        self.execute_menu_option()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                    
                    # Controles de audio en el menú
                    if event.key == pygame.K_m:
                        # Toggle música
                        self.audio.toggle_music()
                        self.audio.play_sound('hit')
                    elif event.key == pygame.K_s:
                        # Toggle efectos
                        self.audio.toggle_sound()
                        self.audio.play_sound('hit')
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        # Subir volumen música
                        new_vol = min(1.0, self.audio.music_volume + 0.1)
                        self.audio.set_music_volume(new_vol)
                    elif event.key == pygame.K_MINUS:
                        # Bajar volumen música
                        new_vol = max(0.0, self.audio.music_volume - 0.1)
                        self.audio.set_music_volume(new_vol)
                
                # Durante el juego
                elif self.game_state in ["playing_solo", "playing_multi"]:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "menu"
                        self.reset_game()
                        self.reset_menu_selection()
                        self.audio.play_sound('enemy_shoot')
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused
                        self.audio.play_sound('hit')
                    elif event.key == pygame.K_SPACE:
                        if not self.paused:
                            bullet = self.player.shoot()
                            if bullet:
                                self.bullets.append(bullet)
                                self.audio.play_sound('shoot')
                    elif event.key == pygame.K_RETURN and self.player2:
                        if not self.paused:
                            bullet = self.player2.shoot()
                            if bullet:
                                self.bullets.append(bullet)
                                self.audio.play_sound('shoot')
                    
                    # Controles de audio durante el juego
                    if event.key == pygame.K_m:
                        # Toggle música
                        self.audio.toggle_music()
                        self.audio.play_sound('hit')
                    elif event.key == pygame.K_s:
                        # Toggle efectos
                        self.audio.toggle_sound()
                        self.audio.play_sound('hit')
                
                # Game Over
                elif self.game_state == "game_over":
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if self.is_new_record:
                            self.game_state = "enter_name"
                        else:
                            self.game_state = "menu"
                            self.reset_game()
                            self.reset_menu_selection()
                        self.audio.play_sound('enemy_shoot')
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = "menu"
                        self.reset_game()
                        self.reset_menu_selection()
                        self.audio.play_sound('enemy_shoot')
                
                # Entrada de nombre para record
                elif self.game_state == "enter_name":
                    if event.key == pygame.K_RETURN:
                        # Guardar record si hay nombre
                        if len(self.player_name) > 0:
                            self.high_scores.add_score(self.player_name, self.score)
                        
                        # Volver al menú
                        self.game_state = "menu"
                        self.reset_game()
                        self.reset_menu_selection()
                        self.player_name = ""
                        self.audio.play_sound('enemy_shoot')
                    
                    elif event.key == pygame.K_ESCAPE:
                        # Saltar entrada de nombre
                        self.game_state = "menu"
                        self.reset_game()
                        self.reset_menu_selection()
                        self.player_name = ""
                        self.audio.play_sound('enemy_shoot')
                    
                    elif event.key == pygame.K_BACKSPACE:
                        # Borrar última letra
                        if len(self.player_name) > 0:
                            self.player_name = self.player_name[:-1]
                            self.audio.play_sound('hit')
                    
                    elif event.unicode.isalpha() and len(event.unicode) == 1:
                        # Agregar letra (máximo 3)
                        if len(self.player_name) < 3:
                            self.player_name += event.unicode.upper()
                            self.audio.play_sound('shoot')
    
    def execute_menu_option(self):
        """Ejecuta la opción seleccionada en el menú"""
        if self.selected_option == 0:  # Un Jugador
            self.start_solo_game()
        elif self.selected_option == 1:  # Multijugador
            self.start_multi_game()
        elif self.selected_option == 2:  # Ver Records
            self.game_state = "view_records"
        elif self.selected_option == 3:  # Salir
            self.running = False
    
    def reset_menu_selection(self):
        """Reinicia la selección del menú a la primera opción"""
        self.selected_option = 0
    
    def start_solo_game(self):
        """Inicia juego de un jugador"""
        self.reset_game()
        self.game_state = "playing_solo"
        self.player2 = None
        self.audio.play_sound('enemy_shoot')
    
    def start_multi_game(self):
        """Inicia juego multijugador con posiciones específicas"""
        self.reset_game()
        self.game_state = "playing_multi"
        self.player2 = Player(2)
        self.audio.play_sound('enemy_shoot')
        
        # Posicionar jugadores en sus zonas (multijugador)
        self.player.rect.centery = SCREEN_HEIGHT // 4  # Jugador 1 arriba
        self.player2.rect.centery = 3 * SCREEN_HEIGHT // 4  # Jugador 2 abajo
    
    def reset_game(self):
        """Reinicia el estado del juego"""
        self.score = 0
        self.level = 1
        self.enemies_killed = 0
        self.paused = False
        self.is_new_record = False
        
        self.player = Player(1)
        if self.player2:
            self.player2 = Player(2)
        
        self.enemies = []
        self.bullets = []
        self.particles = []
        self.explosions = []
        
        self.enemy_spawn_timer = 0
        self.game_over_timer = 0
    
    def update(self):
        """Actualiza la lógica del juego"""
        if self.paused or self.game_state in ["menu", "game_over", "enter_name", "view_records"]:
            # Actualizar cursor de parpadeo para entrada de nombre
            if self.game_state == "enter_name":
                self.name_cursor_blink = (self.name_cursor_blink + 1) % 60
            return
            
        keys = pygame.key.get_pressed()
        
        if self.game_state in ["playing_solo", "playing_multi"]:
            # Actualizar jugadores con restricción de zona
            self.player.update(keys)
            
            # En multijugador: jugador 1 arriba, jugador 2 abajo
            if self.player2:
                # Jugador 1 solo en mitad superior
                if self.player.rect.centery > SCREEN_HEIGHT // 2:
                    self.player.rect.centery = SCREEN_HEIGHT // 2 - 20
                
                # Jugador 2 solo en mitad inferior
                self.player2.update(keys)
                if self.player2.rect.centery < SCREEN_HEIGHT // 2:
                    self.player2.rect.centery = SCREEN_HEIGHT // 2 + 20
            
            # Spawn de enemigos según nivel
            self.enemy_spawn_timer += 1
            spawn_rate = max(30, 60 - (self.level * 10))  # Más rápido en niveles altos
            if self.enemy_spawn_timer >= spawn_rate:
                self.enemy_spawn_timer = 0
                self.spawn_enemy()
            
            # Actualizar enemigos
            for enemy in self.enemies[:]:
                enemy.update()
                
                # Disparar enemigos
                if random.random() < 0.005:  # 0.5% de probabilidad por frame
                    bullet = enemy.shoot()
                    if bullet:
                        self.bullets.append(bullet)
                        self.audio.play_sound('enemy_shoot')
                
                # Eliminar enemigos fuera de pantalla (por la derecha)
                if enemy.is_off_screen():
                    self.enemies.remove(enemy)
            
            # Actualizar balas
            for bullet in self.bullets[:]:
                bullet.update()
                
                # Colisiones balas jugador -> enemigos
                if bullet.is_player:
                    for enemy in self.enemies[:]:
                        if bullet.rect.colliderect(enemy.rect) and enemy.is_alive:
                            points_earned = enemy.take_damage()
                            if points_earned > 0:
                                # Enemigo eliminado
                                self.score += points_earned
                                self.enemies_killed += 1
                                self.create_explosion(enemy.rect.centerx, enemy.rect.centery, "enemy")
                                self.enemies.remove(enemy)
                                self.audio.play_sound('explosion')
                            else:
                                # Solo daño
                                self.audio.play_sound('hit')
                            
                            self.bullets.remove(bullet)
                            break
                
                # Colisiones balas enemigo -> jugadores
                else:
                    if bullet.rect.colliderect(self.player.rect) and self.player.is_alive:
                        if self.player.take_damage():
                            self.create_explosion(self.player.rect.centerx, self.player.rect.centery, "player")
                            self.audio.play_sound('hit')
                        self.bullets.remove(bullet)
                    
                    elif self.player2 and bullet.rect.colliderect(self.player2.rect) and self.player2.is_alive:
                        if self.player2.take_damage():
                            self.create_explosion(self.player2.rect.centerx, self.player2.rect.centery, "player")
                            self.audio.play_sound('hit')
                        self.bullets.remove(bullet)
                
                # Eliminar balas fuera de pantalla
                if bullet.is_off_screen():
                    self.bullets.remove(bullet)
            
            # Colisiones jugadores -> enemigos
            for enemy in self.enemies[:]:
                if (self.player.rect.colliderect(enemy.rect) and self.player.is_alive and 
                    self.player.invincible == 0):
                    if self.player.take_damage():
                        self.create_explosion(self.player.rect.centerx, self.player.rect.centery, "player")
                        self.audio.play_sound('hit')
                    points_earned = enemy.take_damage()
                    if points_earned > 0:
                        self.score += points_earned
                        self.enemies_killed += 1
                        self.create_explosion(enemy.rect.centerx, enemy.rect.centery, "enemy")
                        self.enemies.remove(enemy)
                        self.audio.play_sound('explosion')
                
                if (self.player2 and self.player2.rect.colliderect(enemy.rect) and 
                    self.player2.is_alive and self.player2.invincible == 0):
                    if self.player2.take_damage():
                        self.create_explosion(self.player2.rect.centerx, self.player2.rect.centery, "player")
                        self.audio.play_sound('hit')
                    points_earned = enemy.take_damage()
                    if points_earned > 0:
                        self.score += points_earned
                        self.enemies_killed += 1
                        self.create_explosion(enemy.rect.centerx, enemy.rect.centery, "enemy")
                        self.enemies.remove(enemy)
                        self.audio.play_sound('explosion')
            
            # Actualizar partículas
            for particle in self.particles[:]:
                particle['y'] += particle['speed_y']
                particle['x'] += particle['speed_x']
                particle['life'] -= 1
                particle['size'] = max(0, particle['size'] - 0.1)
                
                if particle['life'] <= 0:
                    self.particles.remove(particle)
            
            # Actualizar explosiones
            for explosion in self.explosions[:]:
                explosion['timer'] -= 1
                explosion['size'] += explosion['growth']
                if explosion['timer'] <= 0:
                    self.explosions.remove(explosion)
            
            # SUBIR DE NIVEL cada 10 enemigos
            if self.enemies_killed >= ENEMIES_PER_LEVEL * self.level:
                self.level += 1
                self.create_level_up_effect()
                self.audio.play_sound('powerup')
                # No resetear enemies_killed para progresión continua
            
            # Verificar game over
            players_alive = self.player.is_alive
            if self.player2:
                players_alive = players_alive or self.player2.is_alive
            
            if not players_alive:
                self.game_state = "game_over"
                self.audio.play_sound('game_over')
                # Verificar si es nuevo record
                self.is_new_record = self.high_scores.is_high_score(self.score)
    
    def spawn_enemy(self):
        """Genera un nuevo enemigo según el nivel actual"""
        # Determinar tipos de enemigos disponibles según nivel
        if self.level == 1:
            # Solo enemigos tipo 1
            enemy_type = 1
        elif self.level == 2:
            # 70% tipo 1, 30% tipo 2
            if random.random() < 0.7:
                enemy_type = 1
            else:
                enemy_type = 2
        else:
            # Nivel 3+: 50% tipo 1, 30% tipo 2, 20% tipo 3
            rand = random.random()
            if rand < 0.5:
                enemy_type = 1
            elif rand < 0.8:
                enemy_type = 2
            else:
                enemy_type = 3
        
        # Crear enemigo
        enemy = Enemy(enemy_type, self.level)
        
        # En multijugador, enemigos pueden aparecer arriba o abajo
        if self.player2 and self.game_state == "playing_multi":
            # 50% arriba, 50% abajo
            if random.random() < 0.5:
                enemy.y = random.randint(50, SCREEN_HEIGHT // 2 - 50)
            else:
                enemy.y = random.randint(SCREEN_HEIGHT // 2 + 50, SCREEN_HEIGHT - 50)
            enemy.rect.centery = enemy.y
        
        self.enemies.append(enemy)
    
    def create_explosion(self, x, y, type="enemy"):
        """Crea efectos de explosión"""
        # Agregar a lista de explosiones
        self.explosions.append({
            'x': x,
            'y': y,
            'size': 10,
            'growth': 2,
            'timer': 30,
            'type': type,
            'color': COLORS['enemy1'] if type == "enemy" else COLORS['player1']
        })
        
        # Partículas
        particle_count = 20 if type == "enemy" else 15
        for _ in range(particle_count):
            color = random.choice([
                (255, 200, 100), 
                (255, 150, 50), 
                (255, 100, 0),
                (255, 50, 50) if type == "enemy" else (100, 180, 255)
            ])
            
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(1, 4)
            
            self.particles.append({
                'x': x,
                'y': y,
                'speed_x': math.cos(angle) * speed,
                'speed_y': math.sin(angle) * speed,
                'life': random.randint(20, 40),
                'size': random.randint(2, 5),
                'color': color
            })
    
    def create_level_up_effect(self):
        """Crea efecto visual al subir de nivel"""
        # Partículas especiales
        for i in range(40):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(3, 8)
            
            self.particles.append({
                'x': SCREEN_WIDTH // 2,
                'y': SCREEN_HEIGHT // 2,
                'speed_x': math.cos(angle) * speed,
                'speed_y': math.sin(angle) * speed,
                'life': random.randint(40, 80),
                'size': random.randint(4, 8),
                'color': random.choice([COLORS['highlight'], COLORS['player1'], COLORS['player2']])
            })
    
    def draw(self):
        """Dibuja todo en pantalla"""
        # Fondo con estrellas
        self.draw_background()
        
        # Dibujar línea divisoria HORIZONTAL solo en multijugador
        if self.game_state == "playing_multi" and self.player2:
            ShapeDrawer.draw_division_line(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, True)
        
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "game_over":
            self.draw_game_over()
        elif self.game_state == "enter_name":
            self.draw_enter_name()
        elif self.game_state == "view_records":
            self.draw_high_scores()
        else:
            # Dibujar elementos del juego
            for enemy in self.enemies:
                enemy.draw(self.screen)
            
            for bullet in self.bullets:
                bullet.draw(self.screen)
            
            # Dibujar explosiones
            for explosion in self.explosions:
                size = explosion['size']
                alpha = min(255, explosion['timer'] * 8)
                explosion_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                
                # Círculo exterior
                pygame.draw.circle(explosion_surf, 
                                 (*explosion['color'], alpha),
                                 (size, size), size)
                
                # Círculo interior
                inner_size = size // 2
                pygame.draw.circle(explosion_surf,
                                 (255, 255, 200, alpha),
                                 (size, size), inner_size)
                
                self.screen.blit(explosion_surf, 
                               (explosion['x'] - size, explosion['y'] - size))
            
            # Dibujar partículas
            for particle in self.particles:
                pygame.draw.circle(self.screen, particle['color'],
                                 (int(particle['x']), int(particle['y'])),
                                 int(particle['size']))
            
            self.player.draw(self.screen)
            if self.player2:
                self.player2.draw(self.screen)
            
            self.draw_ui()
            
            # Dibujar pantalla de pausa
            if self.paused:
                self.draw_pause_screen()
        
        pygame.display.flip()
    
    def draw_background(self):
        """Dibuja el fondo con estrellas animadas"""
        # Fondo sólido
        self.screen.fill(COLORS['background'])
        
        # Estrellas
        time = pygame.time.get_ticks()
        for i in range(100):
            # Posición base de la estrella
            base_x = (i * 37) % SCREEN_WIDTH
            base_y = (i * 23) % SCREEN_HEIGHT
            
            # Movimiento según el tiempo
            offset_x = math.sin(time / 1000 + i) * 10
            offset_y = math.cos(time / 800 + i) * 10
            
            x = (base_x + offset_x) % SCREEN_WIDTH
            y = (base_y + offset_y) % SCREEN_HEIGHT
            
            # Tamaño y brillo variables
            size = 1 + (i % 3)
            brightness = 100 + (int(time / 100 + i) % 155)
            
            # Color de estrella (algunas azules, otras blancas)
            if i % 4 == 0:
                color = (brightness // 2, brightness // 2, brightness)
            else:
                color = (brightness, brightness, brightness)
            
            pygame.draw.circle(self.screen, color, (int(x), int(y)), size)
    
    def draw_menu(self):
        """Dibuja el menú principal con records y selección por flechas"""
        # Overlay semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Título con efecto - CAMBIADO: "SPACIAL SOLDIER" en lugar de "AVIONCITOS"
        title_text = "SPACIAL SOLDIER"
        title = self.font_large.render(title_text, True, COLORS['player1'])
        
        # Efecto de sombra
        title_shadow = self.font_large.render(title_text, True, (0, 0, 0))
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2 + 3, 103))
        self.screen.blit(title_shadow, title_rect)
        
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Subtítulo - Mantenemos "Juego Retro de Naves"
        subtitle = self.font_medium.render("Juego Retro de Naves", True, COLORS['ui_text'])
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, 170))
        self.screen.blit(subtitle, subtitle_rect)
        
        # MEJORES RECORDS en el menú principal
        records_y = 220
        records_title = self.font_small.render("MEJORES PUNTAJES", True, COLORS['highlight'])
        records_title_rect = records_title.get_rect(center=(SCREEN_WIDTH//2, records_y))
        self.screen.blit(records_title, records_title_rect)
        
        # Mostrar los 3 mejores records
        top_scores = self.high_scores.get_top_scores(3)
        for i, record in enumerate(top_scores):
            record_text = f"{i+1}. {record['name']} ........ {record['score']:06d}"
            color = COLORS['highlight'] if i == 0 else COLORS['ui_text']
            record_display = self.font_small.render(record_text, True, color)
            record_rect = record_display.get_rect(center=(SCREEN_WIDTH//2, records_y + 30 + i * 25))
            self.screen.blit(record_display, record_rect)
        
        # Instrucciones con efecto de parpadeo
        time = pygame.time.get_ticks()
        if time % 1000 < 700:
            instructions = self.font_small.render("↑ ↓ para navegar | ENTER para seleccionar", 
                                                True, COLORS['highlight'])
            instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH//2, records_y + 120))
            self.screen.blit(instructions, instructions_rect)
        
        # Marco para opciones
        menu_box = pygame.Surface((400, 200), pygame.SRCALPHA)
        menu_box.fill((0, 0, 0, 150))
        pygame.draw.rect(menu_box, COLORS['player1'], (0, 0, 400, 200), 2)
        self.screen.blit(menu_box, (SCREEN_WIDTH//2 - 200, records_y + 150))
        
        # Opciones del menú
        menu_y_start = records_y + 180
        option_spacing = 50
        
        for i, option in enumerate(self.menu_options):
            y_pos = menu_y_start + (i * option_spacing)
            
            # Si está seleccionada
            if i == self.selected_option:
                # Fondo resaltado
                highlight = pygame.Surface((350, 35), pygame.SRCALPHA)
                highlight.fill((255, 255, 255, 30))
                
                # Efecto de brillo intermitente
                if time % 500 < 250:
                    pygame.draw.rect(highlight, (255, 255, 255, 50), 
                                    (0, 0, 350, 35), 2)
                
                self.screen.blit(highlight, (SCREEN_WIDTH//2 - 175, y_pos - 10))
                
                # Flechas indicadoras animadas
                arrow_offset = math.sin(time / 200) * 5
                
                # Flecha izquierda
                left_x = SCREEN_WIDTH//2 - 180 + arrow_offset
                pygame.draw.polygon(self.screen, COLORS['highlight'], [
                    (left_x, y_pos),
                    (left_x - 12, y_pos + 7),
                    (left_x - 12, y_pos - 7)
                ])
                
                # Flecha derecha
                right_x = SCREEN_WIDTH//2 + 180 - arrow_offset
                pygame.draw.polygon(self.screen, COLORS['highlight'], [
                    (right_x, y_pos),
                    (right_x + 12, y_pos + 7),
                    (right_x + 12, y_pos - 7)
                ])
            
            # Color del texto según opción
            if i == 0:  # Un Jugador
                text_color = COLORS['player1']
                icon = "▶" if i == self.selected_option else "●"
            elif i == 1:  # Multijugador
                text_color = COLORS['player2']
                icon = "▶" if i == self.selected_option else "●"
            elif i == 2:  # Ver Records
                text_color = COLORS['highlight']
                icon = "▶" if i == self.selected_option else "●"
            else:  # Salir
                text_color = COLORS['ui_text']
                icon = "▶" if i == self.selected_option else "●"
            
            # Texto con icono
            option_display = f"  {icon}  {option}"
            option_text = self.font_medium.render(option_display, True, text_color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH//2, y_pos))
            self.screen.blit(option_text, option_rect)
        
        # Información de controles incluyendo controles de audio
        controls_info = [
            "ESC: Salir del juego",
            f"M: Música {'ON' if self.audio.is_music_enabled else 'OFF'} | S: Efectos {'ON' if self.audio.is_sound_enabled else 'OFF'}",
            "+/-: Ajustar volumen música"
        ]
        
        for j, line in enumerate(controls_info):
            line_text = self.font_small.render(line, True, COLORS['ui_text'])
            line_rect = line_text.get_rect(center=(SCREEN_WIDTH//2, 620 + j * 20))
            self.screen.blit(line_text, line_rect)
    
    def draw_high_scores(self):
        """Dibuja la pantalla completa de records"""
        # Overlay semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Título - Mantenemos "MEJORES PUNTAJES"
        title = self.font_large.render("MEJORES PUNTAJES", True, COLORS['highlight'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Marco para records
        scores_box = pygame.Surface((500, 350), pygame.SRCALPHA)
        scores_box.fill((0, 0, 0, 150))
        pygame.draw.rect(scores_box, COLORS['player1'], (0, 0, 500, 350), 3)
        self.screen.blit(scores_box, (SCREEN_WIDTH//2 - 250, 150))
        
        # Encabezado
        header = self.font_medium.render("POS  NOMBRE  PUNTAJE", True, COLORS['highlight'])
        header_rect = header.get_rect(center=(SCREEN_WIDTH//2, 180))
        self.screen.blit(header, header_rect)
        
        # Lista de records
        all_scores = self.high_scores.scores
        for i, record in enumerate(all_scores):
            # Color según posición
            if i == 0:
                color = (255, 215, 0)  # Oro
                rank_symbol = "🥇"
            elif i == 1:
                color = (192, 192, 192)  # Plata
                rank_symbol = "🥈"
            elif i == 2:
                color = (205, 127, 50)  # Bronce
                rank_symbol = "🥉"
            else:
                color = COLORS['ui_text']
                rank_symbol = f"{i+1}."
            
            # Texto del record
            record_text = f"{rank_symbol}  {record['name']}  ........  {record['score']:06d}"
            record_display = self.font_medium.render(record_text, True, color)
            record_rect = record_display.get_rect(center=(SCREEN_WIDTH//2, 230 + i * 40))
            self.screen.blit(record_display, record_rect)
        
        # Instrucciones para volver
        instructions = [
            "Presiona ESC para volver al menú principal"
        ]
        
        for j, line in enumerate(instructions):
            line_text = self.font_small.render(line, True, COLORS['ui_text'])
            line_rect = line_text.get_rect(center=(SCREEN_WIDTH//2, 520 + j * 25))
            self.screen.blit(line_text, line_rect)
    
    def draw_enter_name(self):
        """Dibuja la pantalla para ingresar nombre para nuevo record"""
        # Overlay semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Título
        title = self.font_large.render("¡NUEVO RECORD!", True, COLORS['highlight'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(title, title_rect)
        
        # Puntaje obtenido
        score_text = self.font_medium.render(f"Puntaje: {self.score:06d}", True, COLORS['ui_text'])
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 220))
        self.screen.blit(score_text, score_rect)
        
        # Instrucción
        instruction = self.font_medium.render("Ingresa tu nombre (3 letras):", True, COLORS['ui_text'])
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH//2, 280))
        self.screen.blit(instruction, instruction_rect)
        
        # Marco para el nombre
        name_box = pygame.Surface((300, 80), pygame.SRCALPHA)
        name_box.fill((0, 0, 0, 150))
        pygame.draw.rect(name_box, COLORS['highlight'], (0, 0, 300, 80), 3)
        self.screen.blit(name_box, (SCREEN_WIDTH//2 - 150, 320))
        
        # Mostrar nombre actual
        display_name = self.player_name
        if len(display_name) < 3:
            display_name += "_" * (3 - len(display_name))
        
        # Separar letras con espacios
        spaced_name = "   ".join(display_name)
        name_text = self.font_large.render(spaced_name, True, COLORS['player1'])
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH//2, 360))
        self.screen.blit(name_text, name_rect)
        
        # Cursor de parpadeo
        if self.name_cursor_blink < 30 and len(self.player_name) < 3:
            cursor_x = SCREEN_WIDTH//2 - 60 + (len(self.player_name) * 60)
            pygame.draw.line(self.screen, COLORS['highlight'],
                           (cursor_x, 340), (cursor_x, 380), 3)
        
        # Instrucciones
        instructions = [
            "Usa el teclado para ingresar 3 letras",
            "ENTER: Guardar  |  ESC: Saltar",
            "BACKSPACE: Borrar última letra"
        ]
        
        for j, line in enumerate(instructions):
            line_text = self.font_small.render(line, True, COLORS['ui_text'])
            line_rect = line_text.get_rect(center=(SCREEN_WIDTH//2, 430 + j * 25))
            self.screen.blit(line_text, line_rect)
    
    def draw_ui(self):
        """Dibuja la interfaz de usuario durante el juego"""
        # Panel superior
        pygame.draw.rect(self.screen, (0, 0, 0, 180), (0, 0, SCREEN_WIDTH, 50))
        
        # Puntaje
        score_text = self.font_small.render(f"Puntaje: {self.score:06d}", True, COLORS['ui_text'])
        self.screen.blit(score_text, (10, 15))
        
        # Nivel
        level_text = self.font_small.render(f"Nivel: {self.level}", True, COLORS['ui_text'])
        self.screen.blit(level_text, (200, 15))
        
        # Vidas jugador 1
        hearts = ""
        for i in range(PLAYER_LIVES):
            if i < self.player.lives:
                hearts += "♥"
            else:
                hearts += "♡"
        
        lives_text = self.font_small.render(f"J1: {hearts}", True, COLORS['player1'])
        self.screen.blit(lives_text, (350, 15))
        
        # Vidas jugador 2 (si existe)
        if self.player2:
            hearts2 = ""
            for i in range(PLAYER_LIVES):
                if i < self.player2.lives:
                    hearts2 += "♥"
                else:
                    hearts2 += "♡"
            
            lives2_text = self.font_small.render(f"J2: {hearts2}", True, COLORS['player2'])
            self.screen.blit(lives2_text, (500, 15))
        
        # Modo de juego
        mode = "SOLO" if self.game_state == "playing_solo" else "MULTIJUGADOR"
        mode_text = self.font_small.render(mode, True, COLORS['highlight'])
        mode_rect = mode_text.get_rect(topright=(SCREEN_WIDTH - 10, 15))
        self.screen.blit(mode_text, mode_rect)
        
        # Indicadores de audio en la esquina superior derecha
        audio_y = 15
        audio_x = SCREEN_WIDTH - 150
        
        # Indicador de música
        music_text = self.font_tiny.render(f"MÚSICA: {'ON' if self.audio.is_music_enabled else 'OFF'}", 
                                          True, COLORS['player1'])
        self.screen.blit(music_text, (audio_x, audio_y))
        
        # Indicador de efectos
        sound_text = self.font_tiny.render(f"EFECTOS: {'ON' if self.audio.is_sound_enabled else 'OFF'}", 
                                          True, COLORS['player2'])
        self.screen.blit(sound_text, (audio_x, audio_y + 20))
        
        # Barra de progreso de nivel
        progress_width = 200
        progress_height = 8
        progress_x = SCREEN_WIDTH // 2 - progress_width // 2
        progress_y = SCREEN_HEIGHT - 100
        
        # Fondo de la barra
        pygame.draw.rect(self.screen, (50, 50, 50), 
                        (progress_x, progress_y, progress_width, progress_height))
        
        # Progreso actual (para subir al siguiente nivel)
        current_progress = self.enemies_killed % ENEMIES_PER_LEVEL
        progress = current_progress / ENEMIES_PER_LEVEL
        fill_width = int(progress_width * progress)
        
        # Color del progreso (cambia según el progreso)
        if progress < 0.33:
            progress_color = (255, 50, 50)  # Rojo
        elif progress < 0.66:
            progress_color = (255, 200, 50)  # Amarillo
        else:
            progress_color = (50, 255, 50)  # Verde
        
        pygame.draw.rect(self.screen, progress_color,
                        (progress_x, progress_y, fill_width, progress_height))
        
        # Borde de la barra
        pygame.draw.rect(self.screen, COLORS['ui_text'],
                        (progress_x, progress_y, progress_width, progress_height), 1)
        
        # Texto de progreso
        progress_text = self.font_tiny.render(f"Próx. nivel: {current_progress}/{ENEMIES_PER_LEVEL}", 
                                            True, COLORS['ui_text'])
        progress_text_rect = progress_text.get_rect(center=(SCREEN_WIDTH//2, progress_y - 10))
        self.screen.blit(progress_text, progress_text_rect)
        
        # Información de enemigos derribados
        enemies_text = self.font_tiny.render(f"Total derribados: {self.enemies_killed}", 
                                           True, COLORS['ui_text'])
        enemies_rect = enemies_text.get_rect(center=(SCREEN_WIDTH//2, progress_y - 25))
        self.screen.blit(enemies_text, enemies_rect)
        
        # Controles en la parte inferior
        controls_y = SCREEN_HEIGHT - 70
        pygame.draw.rect(self.screen, (0, 0, 0, 180),
                        (0, controls_y, SCREEN_WIDTH, 70))
        
        # Jugador 1
        p1_controls = self.font_small.render("J1: Flechas - ESPACIO", True, COLORS['player1'])
        self.screen.blit(p1_controls, (10, controls_y + 10))
        
        # Jugador 2 (si existe)
        if self.player2:
            p2_controls = self.font_small.render("J2: WASD - ENTER", True, COLORS['player2'])
            self.screen.blit(p2_controls, (10, controls_y + 35))
        
        # Controles generales
        general_x = SCREEN_WIDTH - 200
        general_controls = [
            ("ESC", "Menú"),
            ("P", "Pausa"),
            ("M", "Música ON/OFF"),
            ("S", "Efectos ON/OFF")
        ]
        
        for i, (key, action) in enumerate(general_controls):
            key_text = self.font_small.render(f"{key}:", True, COLORS['highlight'])
            action_text = self.font_small.render(action, True, COLORS['ui_text'])
            
            self.screen.blit(key_text, (general_x, controls_y + 10 + i * 20))
            self.screen.blit(action_text, (general_x + 40, controls_y + 10 + i * 20))
    
    def draw_pause_screen(self):
        """Dibuja la pantalla de pausa"""
        # Overlay semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Texto de pausa
        pause_text = self.font_large.render("PAUSA", True, COLORS['highlight'])
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(pause_text, pause_rect)
        
        # Instrucciones
        instructions = [
            "Presiona P para continuar",
            "Presiona ESC para volver al menú"
        ]
        
        for i, line in enumerate(instructions):
            line_text = self.font_medium.render(line, True, COLORS['ui_text'])
            line_rect = line_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20 + i * 40))
            self.screen.blit(line_text, line_rect)
        
        # Estadísticas actuales
        stats = [
            f"Puntaje: {self.score}",
            f"Nivel: {self.level}",
            f"Enemigos eliminados: {self.enemies_killed}",
            f"Próximo nivel en: {ENEMIES_PER_LEVEL - (self.enemies_killed % ENEMIES_PER_LEVEL)} enemigos"
        ]
        
        for i, stat in enumerate(stats):
            stat_text = self.font_small.render(stat, True, COLORS['ui_text'])
            stat_rect = stat_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100 + i * 25))
            self.screen.blit(stat_text, stat_rect)
    
    def draw_game_over(self):
        """Dibuja pantalla de Game Over"""
        # Fondo semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Texto GAME OVER grande
        game_over = self.font_large.render("GAME OVER", True, COLORS['enemy1'])
        game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH//2, 120))
        self.screen.blit(game_over, game_over_rect)
        
        # Puntaje final
        score_text = self.font_medium.render(f"Puntaje Final: {self.score:06d}", True, COLORS['ui_text'])
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(score_text, score_rect)
        
        # Nivel alcanzado
        level_text = self.font_medium.render(f"Nivel alcanzado: {self.level}", True, COLORS['ui_text'])
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH//2, 240))
        self.screen.blit(level_text, level_rect)
        
        # Enemigos eliminados
        enemies_text = self.font_medium.render(f"Enemigos eliminados: {self.enemies_killed}", True, COLORS['ui_text'])
        enemies_rect = enemies_text.get_rect(center=(SCREEN_WIDTH//2, 280))
        self.screen.blit(enemies_text, enemies_rect)
        
        # Puntos por enemigo
        points_info = self.font_small.render(f"Cada enemigo da {POINTS_PER_ENEMY} puntos", True, COLORS['ui_text'])
        points_rect = points_info.get_rect(center=(SCREEN_WIDTH//2, 310))
        self.screen.blit(points_info, points_rect)
        
        # Verificar si es nuevo record
        if self.is_new_record:
            new_record_text = self.font_large.render("¡NUEVO RECORD!", True, COLORS['highlight'])
            new_record_rect = new_record_text.get_rect(center=(SCREEN_WIDTH//2, 350))
            self.screen.blit(new_record_text, new_record_rect)
            
            instructions = [
                "Presiona ENTER/ESPACIO para guardar tu nombre",
                "Presiona ESC para volver al menú sin guardar"
            ]
        else:
            # Mostrar posición en el ranking
            temp_scores = self.high_scores.scores.copy()
            temp_scores.append({"name": "TMP", "score": self.score})
            temp_scores.sort(key=lambda x: x["score"], reverse=True)
            position = temp_scores.index({"name": "TMP", "score": self.score}) + 1
            
            rank_text = f"Posición en ranking: #{position}"
            rank_display = self.font_medium.render(rank_text, True, COLORS['ui_text'])
            rank_rect = rank_display.get_rect(center=(SCREEN_WIDTH//2, 350))
            self.screen.blit(rank_display, rank_rect)
            
            instructions = [
                "Presiona ENTER/ESPACIO para volver al menú",
                "Presiona ESC para salir al menú"
            ]
        
        # Instrucciones
        for j, line in enumerate(instructions):
            line_text = self.font_small.render(line, True, COLORS['ui_text'])
            line_rect = line_text.get_rect(center=(SCREEN_WIDTH//2, 400 + j * 25))
            self.screen.blit(line_text, line_rect)
    
    def run(self):
        """Bucle principal del juego"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

# Para ejecutar directamente
if __name__ == "__main__":
    game = Game()
    game.run()