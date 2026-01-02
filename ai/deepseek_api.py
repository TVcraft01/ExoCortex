import requests
import json

class DeepSeekAPI:
    def __init__(self, api_key=None, use_internet=True):
        self.api_key = api_key
        self.use_internet = use_internet
        self.base_url = "https://api.deepseek.com/v1"
        self.conversation_history = []
        
    def chat(self, message, context=None):
        """Envoie un message à DeepSeek API"""
        if not self.use_internet or not self.api_key:
            return "⚠️ Mode démo - Connectez internet et ajoutez une clé API"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Ajouter le contexte
        messages = []
        if context:
            messages.append({"role": "system", "content": context})
        
        # Ajouter l'historique
        for msg in self.conversation_history[-5:]:  # Garder les 5 derniers
            messages.append(msg)
        
        # Ajouter le nouveau message
        messages.append({"role": "user", "content": message})
        
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                reply = result["choices"][0]["message"]["content"]
                
                # Mettre à jour l'historique
                self.conversation_history.append({"role": "user", "content": message})
                self.conversation_history.append({"role": "assistant", "content": reply})
                
                return reply
            else:
                return f"❌ Erreur API: {response.status_code}"
                
        except Exception as e:
            return f"❌ Erreur connexion: {str(e)}"
    
    def ask_for_files(self, query):
        """Demande des fichiers si nécessaire"""
        file_keywords = ["fichier", "document", "image", "pdf", "txt", "lire", "ouvrir"]
        
        if any(keyword in query.lower() for keyword in file_keywords):
            return "📁 J'ai besoin de fichiers pour vous aider. Veuillez m'envoyer les fichiers concernés."
        
        return None