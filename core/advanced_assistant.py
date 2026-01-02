import os
import json
from datetime import datetime

class AdvancedAssistant:
    """Assistant avancé avec demande de fichiers et compteur de messages"""
    
    def __init__(self, ai_choice="local", api_key=None, use_internet=True):
        self.ai_choice = ai_choice
        self.api_key = api_key
        self.use_internet = use_internet
        self.message_count = 0
        self.max_messages = 30  # Limite de messages pour la session
        self.conversation_history = []
        
        # Initialiser l'API choisie
        if ai_choice == "deepseek" and use_internet and api_key:
            from ai.deepseek_api import DeepSeekAPI
            self.ai_engine = DeepSeekAPI(api_key, use_internet)
        elif ai_choice == "gemini" and use_internet and api_key:
            from ai.gemini_api import GeminiAPI
            self.ai_engine = GeminiAPI(api_key, use_internet)
        else:
            self.ai_engine = None  # Mode local/démo
        
    def process_query(self, query):
        """Traite une requête avec l'IA sélectionnée"""
        self.message_count += 1
        
        # Vérifier la limite de messages
        if self.message_count > self.max_messages:
            return f"⚠️ Limite de messages atteinte ({self.max_messages}). Veuillez redémarrer l'application."
        
        # Demander des fichiers si nécessaire
        if self._needs_files(query):
            return "📁 J'ai besoin de fichiers pour vous aider. Veuillez m'envoyer les fichiers concernés."
        
        # Utiliser l'IA si disponible
        if self.ai_engine:
            response = self.ai_engine.chat(query)
        else:
            # Mode démo
            response = self._demo_response(query)
        
        # Enregistrer dans l'historique
        self.conversation_history.append({
            "query": query,
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "message_number": self.message_count
        })
        
        # Ajouter le compteur de messages
        response_with_counter = f"{response}\n\n({self.message_count}/{self.max_messages} messages utilisés)"
        
        return response_with_counter
    
    def _needs_files(self, query):
        """Détecte si la requête nécessite des fichiers"""
        file_keywords = ["fichier", "document", "image", "pdf", "txt", "lire", "ouvrir", "modifier", "écrire"]
        return any(keyword in query.lower() for keyword in file_keywords)
    
    def _demo_response(self, query):
        """Réponse en mode démo"""
        query_lower = query.lower()
        
        if "bonjour" in query_lower:
            return "Bonjour ! Je suis en mode démo. Pour utiliser l'IA avancée, configurez une clé API."
        elif "heure" in query_lower:
            now = datetime.now()
            return f"Il est {now.hour} heures {now.minute}."
        elif "fichier" in query_lower:
            return "En mode démo, je ne peux pas lire de fichiers. Activez une IA avec clé API pour cette fonctionnalité."
        else:
            return f"Mode démo: '{query}'. Configurez DeepSeek ou Gemini pour des réponses avancées."
    
    def get_remaining_messages(self):
        """Retourne le nombre de messages restants"""
        return self.max_messages - self.message_count
    
    def reset_counter(self):
        """Réinitialise le compteur de messages"""
        self.message_count = 0