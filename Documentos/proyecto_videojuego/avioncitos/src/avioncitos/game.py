import pygame
import random
from config import *
from player import Player
from enemy import Enemy
from bullet import Bullet
from highscores import HighScores
from audio import AudioManager
from ui import UI

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "mode_select"
        
        # Inicializar pantalla (solo modo ventana)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Avioncitos - Juego Retro")
        
        # Inicializar juego
        self.player = Player(1)
        self.player2 = None
        self.enemies = []
        self.enemies2 = []
        self.bullets = []
        self.bullets2 = []
        self.high_scores = HighScores()
        self.audio = AudioManager()
        self.ui = UI(self.screen)
        self.level = 1
        self.level2 = 1
        self.enemies_destroyed = 0
        self.enemies_destroyed2 = 0
        self.enemy_spawn_timer = 0
        self.enemy_spawn_timer2 = 0
        self.selected_mode = 0
        self.multiplayer = False
        self.split_screen = True
        
        # Inicializar audio
        self.audio.load_sounds()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                # MENÚ DE SELECCIÓN DE MODO
                if self.game_state == "mode_select":
                    if event.key == pygame.K_UP:
                        self.selected_mode = (self.selected_mode - 1) % len(GAME_MODES)
                    elif event.key == pygame.K_DOWN:
                        self.selected_mode = (self.selected_mode + 1) % len(GAME_MODES)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_mode == 0:  # SOLO
                            self.multiplayer = False
                            self.start_game()
                        elif self.selected_mode == 1:  # MULTIJUGADOR
                            self.multiplayer = True
                            self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                
                # JUEGO EN PROGRESO
                elif self.game_state == "playing":
                    if event.key == pygame.K_SPACE:
                        self.bullets.append(Bullet(self.player.shoot(), 1))
                        self.audio.play_sound("shoot")
                    
                    if self.multiplayer and event.key == pygame.K_RETURN:
                        self.bullets2.append(Bullet(self.player2.shoot(), 2))
                        self.audio.play_sound("shoot")
                    
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = "mode_select"
                
                # GAME OVER
                elif self.game_state == "game_over":
                    if event.key == pygame.K_RETURN:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
    
    def start_game(self):
        """Inicia un nuevo juego según el modo seleccionado"""
        self.player.reset()
        if self.multiplayer:
            self.player2 = Player(2)
            self.player2.reset()
        else:
            self.player2 = None
            self.split_screen = False
        
        self.enemies.clear()
        self.enemies2.clear()
        self.bullets.clear()
        self.bullets2.clear()
        self.level = 1
        self.level2 = 1
        self.enemies_destroyed = 0
        self.enemies_destroyed2 = 0
        self.game_state = "playing"
        if not self.audio.music_playing:
            self.audio.play_music()
    
    def reset_game(self):
        """Reinicia el juego al estado inicial"""
        self.game_state = "mode_select"
        self.selected_mode = 0
        self.multiplayer = False
        self.player.reset()
        self.player2 = None
        self.enemies.clear()
        self.enemies2.clear()
        self.bullets.clear()
        self.bullets2.clear()
        self.level = 1
        self.level2 = 1
        self.enemies_destroyed = 0
        self.enemies_destroyed2 = 0
    
    def update_single_screen(self):
        """Actualiza el juego en modo pantalla única"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player.move("up")
        if keys[pygame.K_DOWN]:
            self.player.move("down")
        
        if self.multiplayer and self.player2:
            if keys[pygame.K_w]:
                self.player2.move("up")
            if keys[pygame.K_s]:
                self.player2.move("down")
        
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= ENEMY_SPAWN_RATE:
            self.enemies.append(Enemy(self.level))
            self.enemy_spawn_timer = 0
        
        for bullet in self.bullets[:]:
            if bullet.update():
                self.bullets.remove(bullet)
        
        self.check_collisions_single_screen()
    
    def update_split_screen(self):
        """Actualiza el juego en modo split screen"""
        screen_height_half = SCREEN_HEIGHT // 2
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if self.player.rect.top > 0:
                self.player.move("up")
        if keys[pygame.K_DOWN]:
            if self.player.rect.bottom < screen_height_half:
                self.player.move("down")
        
        if self.multiplayer and self.player2:
            if keys[pygame.K_w]:
                if self.player2.rect.top > screen_height_half:
                    self.player2.move("up")
            if keys[pygame.K_s]:
                if self.player2.rect.bottom < SCREEN_HEIGHT:
                    self.player2.move("down")
        
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= ENEMY_SPAWN_RATE:
            enemy = Enemy(self.level)
            enemy.rect.y = random.randint(0, screen_height_half - ENEMY_HEIGHT)
            self.enemies.append(enemy)
            self.enemy_spawn_timer = 0
        
        self.enemy_spawn_timer2 += 1
        if self.enemy_spawn_timer2 >= ENEMY_SPAWN_RATE:
            enemy = Enemy(self.level2)
            enemy.rect.y = random.randint(screen_height_half, SCREEN_HEIGHT - ENEMY_HEIGHT)
            self.enemies2.append(enemy)
            self.enemy_spawn_timer2 = 0
        
        for bullet in self.bullets[:]:
            if bullet.update():
                self.bullets.remove(bullet)
        
        for bullet in self.bullets2[:]:
            if bullet.update():
                self.bullets2.remove(bullet)
        
        self.check_collisions_split_screen()
    
    def check_collisions_single_screen(self):
        """Verifica colisiones en modo pantalla única"""
        enemies_to_remove = []
        bullets_to_remove = []
        
        for enemy in self.enemies[:]:
            if enemy.update():
                enemies_to_remove.append(enemy)
                continue
            
            if enemy.collides_with(self.player.rect):
                enemies_to_remove.append(enemy)
                self.audio.play_sound("explosion")
                if self.player.take_damage():
                    self.game_over()
                continue
            
            if self.multiplayer and self.player2 and enemy.collides_with(self.player2.rect):
                enemies_to_remove.append(enemy)
                self.audio.play_sound("explosion")
                if self.player2.take_damage():
                    self.game_over()
                continue
            
            for bullet in self.bullets[:]:
                if enemy.collides_with(bullet.rect):
                    enemies_to_remove.append(enemy)
                    bullets_to_remove.append(bullet)
                    self.audio.play_sound("explosion")
                    
                    if bullet.player_num == 1:
                        self.player.score += POINTS_PER_ENEMY
                        self.enemies_destroyed += 1
                    else:
                        self.player2.score += POINTS_PER_ENEMY
                        self.enemies_destroyed += 1
                    
                    if self.enemies_destroyed >= ENEMIES_PER_LEVEL and self.level < MAX_LEVEL:
                        self.level += 1
                        self.enemies_destroyed = 0
                    break
        
        for item in enemies_to_remove:
            if item in self.enemies:
                self.enemies.remove(item)
        for item in bullets_to_remove:
            if item in self.bullets:
                self.bullets.remove(item)
    
    def check_collisions_split_screen(self):
        """Verifica colisiones en modo split screen"""
        screen_height_half = SCREEN_HEIGHT // 2
        
        enemies_to_remove = []
        bullets_to_remove = []
        
        for enemy in self.enemies[:]:
            if enemy.update():
                enemies_to_remove.append(enemy)
                continue
            
            if enemy.collides_with(self.player.rect):
                enemies_to_remove.append(enemy)
                self.audio.play_sound("explosion")
                if self.player.take_damage():
                    self.game_over()
                continue
            
            for bullet in self.bullets[:]:
                if enemy.collides_with(bullet.rect):
                    enemies_to_remove.append(enemy)
                    bullets_to_remove.append(bullet)
                    self.audio.play_sound("explosion")
                    self.player.score += POINTS_PER_ENEMY
                    self.enemies_destroyed += 1
                    
                    if self.enemies_destroyed >= ENEMIES_PER_LEVEL and self.level < MAX_LEVEL:
                        self.level += 1
                        self.enemies_destroyed = 0
                    break
        
        enemies_to_remove2 = []
        bullets_to_remove2 = []
        
        for enemy in self.enemies2[:]:
            if enemy.update():
                enemies_to_remove2.append(enemy)
                continue
            
            if enemy.collides_with(self.player2.rect):
                enemies_to_remove2.append(enemy)
                self.audio.play_sound("explosion")
                if self.player2.take_damage():
                    self.game_over()
                continue
            
            for bullet in self.bullets2[:]:
                if enemy.collides_with(bullet.rect):
                    enemies_to_remove2.append(enemy)
                    bullets_to_remove2.append(bullet)
                    self.audio.play_sound("explosion")
                    self.player2.score += POINTS_PER_ENEMY
                    self.enemies_destroyed2 += 1
                    
                    if self.enemies_destroyed2 >= ENEMIES_PER_LEVEL and self.level2 < MAX_LEVEL:
                        self.level2 += 1
                        self.enemies_destroyed2 = 0
                    break
        
        for item in enemies_to_remove:
            if item in self.enemies:
                self.enemies.remove(item)
        for item in bullets_to_remove:
            if item in self.bullets:
                self.bullets.remove(item)
        
        for item in enemies_to_remove2:
            if item in self.enemies2:
                self.enemies2.remove(item)
        for item in bullets_to_remove2:
            if item in self.bullets2:
                self.bullets2.remove(item)
    
    def update(self):
        if self.game_state != "playing":
            return
        
        if self.multiplayer and self.split_screen:
            self.update_split_screen()
        else:
            self.update_single_screen()
    
    def draw_split_screen(self):
        """Dibuja el juego en modo split screen"""
        screen_height_half = SCREEN_HEIGHT // 2
        
        # Fondo completo negro primero
        self.screen.fill(BLACK)
        
        # Dibujar todos los elementos
        self.player.draw(self.screen)
        
        if self.player2:
            self.player2.draw(self.screen)
        
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        for enemy in self.enemies2:
            enemy.draw(self.screen)
        
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        for bullet in self.bullets2:
            bullet.draw(self.screen)
        
        # Línea divisoria
        pygame.draw.line(self.screen, WHITE, (0, screen_height_half), 
                        (SCREEN_WIDTH, screen_height_half), 2)
    
    def draw_single_screen(self):
        """Dibuja el juego en modo pantalla única"""
        self.screen.fill(BLACK)
        self.player.draw(self.screen)
        
        if self.multiplayer and self.player2:
            self.player2.draw(self.screen)
        
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        for bullet in self.bullets:
            bullet.draw(self.screen)
    
    def draw(self):
        if self.game_state == "mode_select":
            self.ui.draw_start_screen(self.high_scores.get_scores(), self.selected_mode)
        
        elif self.game_state == "playing":
            if self.multiplayer and self.split_screen:
                self.draw_split_screen()
            else:
                self.draw_single_screen()
            
            # Dibujar UI
            if self.multiplayer and self.split_screen:
                self.ui.draw_game_ui(
                    self.player.score, self.player.lives, self.level,
                    multiplayer=True,
                    player2_score=self.player2.score if self.player2 else 0,
                    player2_lives=self.player2.lives if self.player2 else 0,
                    split_screen=True
                )
            elif self.multiplayer:
                self.ui.draw_game_ui(
                    self.player.score, self.player.lives, self.level,
                    multiplayer=True,
                    player2_score=self.player2.score if self.player2 else 0,
                    player2_lives=self.player2.lives if self.player2 else 0
                )
            else:
                self.ui.draw_game_ui(self.player.score, self.player.lives, self.level)
        
        elif self.game_state == "game_over":
            if self.multiplayer and self.player2:
                self.ui.draw_game_over(
                    self.player.score, 
                    self.high_scores.get_scores(),
                    multiplayer=True,
                    player1_score=self.player.score,
                    player2_score=self.player2.score
                )
            else:
                is_high_score = self.high_scores.is_high_score(self.player.score)
                self.ui.draw_game_over(self.player.score, self.high_scores.get_scores(), is_high_score)
        
        pygame.display.flip()
    
    def game_over(self):
        """Maneja el fin del juego"""
        self.game_state = "game_over"
        
        if not self.multiplayer and self.high_scores.is_high_score(self.player.score):
            self.game_state = "high_score_input"
            player_name = self.ui.get_player_name()
            self.high_scores.add_score(player_name, self.player.score)
            self.game_state = "game_over"
    
    def run(self):
        """Bucle principal del juego"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)