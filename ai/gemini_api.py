import os
from typing import Optional, List, Dict

class GeminiAPI:
    """Client pour l'API Gemini (Google)"""
    
    def __init__(self, api_key: Optional[str] = None, use_internet: bool = True):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.use_internet = use_internet
        self.model = "gemini-pro"
        self.conversation_history: List[Dict] = []
        self.max_history = 10
        
    def chat(self, message: str, context: Optional[str] = None, files: Optional[List[str]] = None) -> str:
        """
        Envoie un message à l'API Gemini
        
        Args:
            message: Le message de l'utilisateur
            context: Contexte optionnel
            files: Liste de chemins de fichiers optionnels
            
        Returns:
            La réponse de l'API
        """
        if not self.use_internet:
            return "🌐 Veuillez activer l'accès internet pour utiliser Gemini."
        
        if not self.api_key:
            return "🔑 Veuillez configurer votre clé API Gemini dans les paramètres."
        
        # Importation différée de google.generativeai
        try:
            import google.generativeai as genai
        except ImportError:
            return "❌ Le package 'google-generativeai' n'est pas installé. Veuillez l'installer avec 'pip install google-generativeai'"
        
        # Configuration de l'API
        genai.configure(api_key=self.api_key)
        
        # Préparer le modèle
        model = genai.GenerativeModel(self.model)
        
        # Préparer le contenu
        prompt = self._prepare_prompt(message, context, files)
        
        try:
            response = model.generate_content(prompt)
            reply = response.text
            
            # Mettre à jour l'historique
            self._update_history(message, reply)
            
            return reply
            
        except Exception as e:
            return f"❌ Erreur Gemini: {str(e)}"
    
    def _prepare_prompt(self, message: str, context: Optional[str], files: Optional[List[str]]) -> str:
        """Prépare le prompt pour Gemini"""
        prompt_parts = []
        
        if context:
            prompt_parts.append(f"Contexte: {context}")
        
        prompt_parts.append(f"Utilisateur: {message}")
        
        if files:
            file_info = self._process_files(files)
            prompt_parts.append(f"Fichiers fournis:\n{file_info}")
        
        return "\n\n".join(prompt_parts)
    
    def _process_files(self, files: List[str]) -> str:
        """Traite les fichiers et retourne un résumé"""
        # Pour Gemini, nous ne pouvons pas envoyer les fichiers directement via l'API texte,
        # donc nous lisons le contenu des fichiers texte et les incluons dans le prompt.
        file_summary = []
        
        for file_path in files:
            if os.path.exists(file_path):
                filename = os.path.basename(file_path)
                size = os.path.getsize(file_path)
                ext = os.path.splitext(file_path)[1].lower()
                
                # Lire le contenu des fichiers texte
                if ext in ['.txt', '.py', '.js', '.html', '.css', '.json', '.md', '.xml']:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read(2000)  # Limiter la taille
                            file_summary.append(f"- {filename}:\n```\n{content[:500]}...\n```")
                    except:
                        file_summary.append(f"- {filename} - Impossible de lire")
                else:
                    file_summary.append(f"- {filename} (fichier binaire, extension: {ext})")
            else:
                file_summary.append(f"- {file_path} - Fichier non trouvé")
        
        return "\n".join(file_summary)
    
    def _update_history(self, user_message: str, assistant_message: str):
        """Met à jour l'historique de conversation"""
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": assistant_message})
        
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-(self.max_history * 2):]
    
    def clear_history(self):
        """Efface l'historique de conversation"""
        self.conversation_history = []
        return "✅ Historique Gemini effacé."
    
    def get_instructions(self) -> str:
        """Retourne les instructions pour configurer Gemini"""
        return """📝 Pour utiliser Gemini API :
1. Allez sur: https://makersuite.google.com/app/apikey
2. Créez un nouveau projet
3. Générez une clé API
4. Collez-la dans les paramètres d'EXOCORTEX

Note: L'API Gemini nécessite l'installation du package:
pip install google-generativeai"""