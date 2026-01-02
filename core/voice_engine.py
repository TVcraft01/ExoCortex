# core/voice_engine.py
import threading
import time

class VoiceEngine:
    """Moteur vocal de Zodiac OS"""
    
    def __init__(self):
        self.is_listening = False
        self.callbacks = {}
        
    def initialize(self):
        """Initialise le moteur vocal"""
        print("[VOICE] VoiceEngine initialisé (mode simulation)")
        
    def start_listening(self):
        """Démarre l'écoute"""
        self.is_listening = True
        print("[VOICE] Écoute démarrée")
        
        # Appeler le callback si défini
        if hasattr(self, 'on_listening_start'):
            self.on_listening_start()
            
        # Simuler une transcription après 3 secondes
        threading.Timer(3.0, self._simulate_transcription).start()
        
    def stop_listening(self):
        """Arrête l'écoute"""
        self.is_listening = False
        print("[VOICE] Écoute arrêtée")
        
        # Appeler le callback si défini
        if hasattr(self, 'on_listening_stop'):
            self.on_listening_stop()
            
    def _simulate_transcription(self):
        """Simule une transcription vocale"""
        if self.is_listening:
            simulated_text = "Ceci est une simulation de reconnaissance vocale"
            print(f"[VOICE] Simulation : {simulated_text}")
            
            # Appeler les callbacks
            if hasattr(self, 'on_transcription'):
                self.on_transcription(simulated_text)
                
    def set_callback(self, event, callback):
        """Définit un callback"""
        self.callbacks[event] = callback
        
    def speak(self, text):
        """Parle un texte"""
        print(f"[VOICE] Synthèse : {text}")