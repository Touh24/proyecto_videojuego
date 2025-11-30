import json
import os
from config import HIGHSCORES_FILE

class HighScores:
    def __init__(self):
        self.scores = self.load_scores()
    
    def load_scores(self):
        """Carga los highscores desde el archivo"""
        try:
            if os.path.exists(HIGHSCORES_FILE):
                with open(HIGHSCORES_FILE, 'r') as f:
                    return json.load(f)
        except:
            pass
        # Scores por defecto
        return [{"name": "AAA", "score": 100}, 
                {"name": "BBB", "score": 50}, 
                {"name": "CCC", "score": 25}]
    
    def save_scores(self):
        """Guarda los highscores en el archivo"""
        try:
            with open(HIGHSCORES_FILE, 'w') as f:
                json.dump(self.scores, f)
        except:
            pass
    
    def is_high_score(self, score):
        """Verifica si el puntaje es un high score"""
        return score > self.scores[-1]["score"]
    
    def add_score(self, name, score):
        """Agrega un nuevo high score"""
        self.scores.append({"name": name, "score": score})
        # Ordenar y mantener solo los top 3
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[:3]
        self.save_scores()
    
    def get_scores(self):
        """Obtiene la lista de highscores"""
        return self.scores