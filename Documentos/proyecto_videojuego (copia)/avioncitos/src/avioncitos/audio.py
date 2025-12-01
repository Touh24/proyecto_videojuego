# audio.py - VERSIÓN CORREGIDA
import pygame
import os
import math  # Importar math en lugar de usar pygame.math
import numpy as np

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music_volume = 0.7
        self.sound_volume = 0.8
        self.is_music_enabled = True
        self.is_sound_enabled = True
        
        # Cargar efectos de sonido
        self.load_sounds()
        
        # Cargar música de fondo
        self.load_music()
    
    def load_sounds(self):
        """Carga todos los efectos de sonido"""
        try:
            # Crear sonidos simples si no hay archivos
            self.create_default_sounds()
            
            # Intentar cargar archivos si existen
            sound_files = {
                'shoot': 'sounds/shoot.wav',
                'enemy_shoot': 'sounds/enemy_shoot.wav',
                'explosion': 'sounds/explosion.wav',
                'hit': 'sounds/hit.wav',
                'powerup': 'sounds/powerup.wav',
                'game_over': 'sounds/game_over.wav'
            }
            
            for name, path in sound_files.items():
                if os.path.exists(path):
                    self.sounds[name] = pygame.mixer.Sound(path)
                    print(f"Sonido cargado: {name}")
            
        except Exception as e:
            print(f"Error cargando sonidos: {e}")
            # Usar sonidos por defecto
            self.create_default_sounds()
    
    def create_default_sounds(self):
        """Crea sonidos por defecto si no hay archivos"""
        # Disparo jugador (sonido agudo corto)
        shoot_buffer = pygame.mixer.Sound(buffer=bytes([0] * 2205))  # 0.05 segundos
        shoot_freq = 440  # Hz (La4)
        shoot_array = pygame.sndarray.array(shoot_buffer)
        for i in range(len(shoot_array)):
            t = i / 44100.0
            shoot_array[i] = int(32767 * 0.3 * (t < 0.05) * 
                               math.sin(2 * math.pi * shoot_freq * t))  # CORREGIDO: math.sin en lugar de pygame.math.sin
        
        self.sounds['shoot'] = pygame.mixer.Sound(array=shoot_array)
        
        # Disparo enemigo (sonido más grave)
        enemy_shoot_buffer = pygame.mixer.Sound(buffer=bytes([0] * 2205))
        enemy_freq = 220  # Hz (La3)
        enemy_array = pygame.sndarray.array(enemy_shoot_buffer)
        for i in range(len(enemy_array)):
            t = i / 44100.0
            enemy_array[i] = int(32767 * 0.3 * (t < 0.07) * 
                               math.sin(2 * math.pi * enemy_freq * t))  # CORREGIDO
        
        self.sounds['enemy_shoot'] = pygame.mixer.Sound(array=enemy_array)
        
        # Explosión (ruido blanco con decaimiento)
        explosion_buffer = pygame.mixer.Sound(buffer=bytes([0] * 8820))  # 0.2 segundos
        explosion_array = pygame.sndarray.array(explosion_buffer)
        for i in range(len(explosion_array)):
            t = i / 44100.0
            if t < 0.2:
                decay = 1.0 - (t / 0.2)
                explosion_array[i] = int(32767 * 0.5 * decay * 
                                       (math.sin(2 * math.pi * 100 * t) +  # CORREGIDO
                                        math.sin(2 * math.pi * 200 * t) +  # CORREGIDO
                                        math.sin(2 * math.pi * 300 * t)) / 3)  # CORREGIDO
        
        self.sounds['explosion'] = pygame.mixer.Sound(array=explosion_array)
        
        # Impacto (sonido corto con frecuencia descendente)
        hit_buffer = pygame.mixer.Sound(buffer=bytes([0] * 4410))  # 0.1 segundos
        hit_array = pygame.sndarray.array(hit_buffer)
        for i in range(len(hit_array)):
            t = i / 44100.0
            if t < 0.1:
                freq = 800 * (1 - t/0.1)  # Frecuencia descendente
                hit_array[i] = int(32767 * 0.4 * (t < 0.1) * 
                                 math.sin(2 * math.pi * freq * t))  # CORREGIDO
        
        self.sounds['hit'] = pygame.mixer.Sound(array=hit_array)
        
        # Game Over (sonido más largo)
        game_over_buffer = pygame.mixer.Sound(buffer=bytes([0] * 13230))  # 0.3 segundos
        game_over_array = pygame.sndarray.array(game_over_buffer)
        for i in range(len(game_over_array)):
            t = i / 44100.0
            if t < 0.3:
                decay = 1.0 - (t / 0.3)
                freq = 300 * (1 - t/0.3) + 50  # Frecuencia descendente
                game_over_array[i] = int(32767 * 0.6 * decay * 
                                       math.sin(2 * math.pi * freq * t))  # CORREGIDO
        
        self.sounds['game_over'] = pygame.mixer.Sound(array=game_over_array)
        
        # Powerup (sonido ascendente)
        powerup_buffer = pygame.mixer.Sound(buffer=bytes([0] * 4410))  # 0.1 segundos
        powerup_array = pygame.sndarray.array(powerup_buffer)
        for i in range(len(powerup_array)):
            t = i / 44100.0
            if t < 0.1:
                freq = 200 + (t/0.1) * 800  # Frecuencia ascendente
                powerup_array[i] = int(32767 * 0.5 * 
                                     math.sin(2 * math.pi * freq * t))  # CORREGIDO
        
        self.sounds['powerup'] = pygame.mixer.Sound(array=powerup_array)
        
        print("Sonidos por defecto creados")
    
    def load_music(self):
        """Carga o crea música de fondo"""
        try:
            # Intentar cargar archivo de música
            music_files = [
                'music/background.mp3',
                'music/background.ogg',
                'music/background.wav'
            ]
            
            for music_file in music_files:
                if os.path.exists(music_file):
                    self.music_file = music_file
                    print(f"Música encontrada: {music_file}")
                    return
            
            print("No se encontraron archivos de música, continuando sin música")
            self.music_file = None
            
        except Exception as e:
            print(f"Error cargando música: {e}")
            self.music_file = None
    
    def play_music(self, loop=-1):
        """Reproduce la música de fondo"""
        if not self.is_music_enabled:
            return
            
        if self.music_file and os.path.exists(self.music_file):
            try:
                pygame.mixer.music.load(self.music_file)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(loop)
                print(f"Reproduciendo música: {self.music_file}")
            except Exception as e:
                print(f"Error reproduciendo música: {e}")
    
    def stop_music(self):
        """Detiene la música"""
        pygame.mixer.music.stop()
    
    def play_sound(self, sound_name):
        """Reproduce un efecto de sonido"""
        if not self.is_sound_enabled or sound_name not in self.sounds:
            return
            
        try:
            sound = self.sounds[sound_name]
            sound.set_volume(self.sound_volume)
            sound.play()
        except Exception as e:
            print(f"Error reproduciendo sonido {sound_name}: {e}")
    
    def set_music_volume(self, volume):
        """Ajusta el volumen de la música (0.0 a 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sound_volume(self, volume):
        """Ajusta el volumen de efectos (0.0 a 1.0)"""
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)
    
    def toggle_music(self):
        """Activa/desactiva la música"""
        self.is_music_enabled = not self.is_music_enabled
        if self.is_music_enabled:
            self.play_music(-1)
        else:
            self.stop_music()
        return self.is_music_enabled
    
    def toggle_sound(self):
        """Activa/desactiva los efectos"""
        self.is_sound_enabled = not self.is_sound_enabled
        return self.is_sound_enabled