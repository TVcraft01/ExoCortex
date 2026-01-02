# core/assistant.py
class ZodiacAssistant:
    """Assistant principal de Zodiac OS"""
    
    def __init__(self):
        self.name = "Zodiac"
        self.version = "2.0.0"
        
    def process_query(self, query):
        """Traite une requête utilisateur"""
        query_lower = query.lower()
        
        # Réponses par défaut
        if "bonjour" in query_lower or "salut" in query_lower:
            return "Bonjour ! Je suis Zodiac. Comment puis-je vous aider ?"
        elif "heure" in query_lower:
            from datetime import datetime
            now = datetime.now()
            return f"Il est {now.hour} heures {now.minute}."
        elif "date" in query_lower:
            from datetime import datetime
            now = datetime.now()
            months = ["janvier", "février", "mars", "avril", "mai", "juin",
                     "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
            return f"Nous sommes le {now.day} {months[now.month-1]} {now.year}."
        elif "météo" in query_lower:
            return "Je récupère les informations météo... (Mode démo)"
        elif "musique" in query_lower:
            return "Contrôle musical activé. (Mode démo)"
        else:
            return f"J'ai bien reçu votre message : '{query}'. Mode démo activé."