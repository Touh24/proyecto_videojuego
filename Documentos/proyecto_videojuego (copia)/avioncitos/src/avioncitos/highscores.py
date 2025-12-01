# highscores.py
import json
import os

class HighScores:
    def __init__(self, filename="highscores.json"):
        self.filename = filename
        self.scores = self.load_scores()
    
    def load_scores(self):
        """Carga los puntajes altos desde el archivo JSON"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # Si hay error, crear archivo nuevo
                return self.get_default_scores()
        else:
            return self.get_default_scores()
    
    def get_default_scores(self):
        """Retorna los puntajes por defecto"""
        return [
            {"name": "AAA", "score": 1000},
            {"name": "BBB", "score": 750},
            {"name": "CCC", "score": 500},
            {"name": "DDD", "score": 250},
            {"name": "EEE", "score": 100}
        ]
    
    def save_scores(self):
        """Guarda los puntajes en el archivo JSON"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.scores, f, indent=2)
        except IOError:
            print("Error al guardar puntajes altos")
    
    def add_score(self, name, score):
        """Agrega un nuevo puntaje y ordena la lista"""
        # Limitar nombre a 3 letras
        name = name[:3].upper()
        
        self.scores.append({"name": name, "score": score})
        
        # Ordenar de mayor a menor
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        
        # Mantener solo los 5 mejores
        self.scores = self.scores[:5]
        
        # Guardar cambios
        self.save_scores()
    
    def is_high_score(self, score):
        """Verifica si el puntaje es suficientemente alto para entrar en el top 5"""
        if len(self.scores) < 5:
            return True
        
        # El puntaje más bajo en el top 5
        lowest_score = min(entry["score"] for entry in self.scores)
        return score > lowest_score
    
    def get_top_scores(self, count=3):
        """Retorna los mejores puntajes"""
        return self.scores[:count]
    
    def clear_scores(self):
        """Limpia todos los puntajes"""
        self.scores = self.get_default_scores()
        self.save_scores()