import pygame
import os
from config import ASSETS_PATH

class AudioManager:
    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        
    def load_sounds(self):
        """Carga los efectos de sonido"""
        try:
            # Efectos de sonido básicos (podrías agregar archivos reales después)
            self.sounds["shoot"] = pygame.mixer.Sound(self._create_beep_sound(440, 100))
            self.sounds["explosion"] = pygame.mixer.Sound(self._create_beep_sound(220, 200))
        except:
            # Si hay error, crear sonidos por defecto
            self._create_default_sounds()
    
    def _create_beep_sound(self, frequency, duration):
        """Crea un sonido de beep simple (temporal)"""
        sample_rate = 44100
        n_samples = int(round(duration * 0.001 * sample_rate))
        buf = numpy.zeros((n_samples, 2), dtype=numpy.int16)
        max_sample = 2**(16 - 1) - 1
        for s in range(n_samples):
            t = float(s) / sample_rate
            buf[s][0] = int(round(max_sample * math.sin(2 * math.pi * frequency * t)))
            buf[s][1] = int(round(max_sample * math.sin(2 * math.pi * frequency * t)))
        return pygame.sndarray.make_sound(buf)
    
    def _create_default_sounds(self):
        """Crea sonidos por defecto si no se pueden cargar archivos"""
        # Sonidos simples como placeholder
        self.sounds["shoot"] = None
        self.sounds["explosion"] = None
    
    def play_sound(self, sound_name):
        """Reproduce un efecto de sonido"""
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play()
    
    def play_music(self):
        """Reproduce música de fondo (MIDI)"""
        try:
            # Intentar cargar música MIDI
            pygame.mixer.music.load(os.path.join(ASSETS_PATH, "music", "background.mid"))
            pygame.mixer.music.play(-1)  # Repetir indefinidamente
            self.music_playing = True
        except:
            # Si no hay archivo MIDI, continuar sin música
            self.music_playing = False
    
    def stop_music(self):
        """Detiene la música"""
        pygame.mixer.music.stop()