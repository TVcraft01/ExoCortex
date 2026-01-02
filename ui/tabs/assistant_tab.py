# ui/tabs/assistant_tab.py - VERSION COMPLÈTE CORRIGÉE
import customtkinter as ctk
import threading

class AssistantTab(ctk.CTkFrame):
    """Onglet Assistant EXOCORTEX - Version complète"""
    
    def __init__(self, parent, assistant=None, voice_engine=None, mobile_mode=True):
        super().__init__(parent, fg_color="#0A0A0F")
        self.mobile_mode = mobile_mode
        
        # Si assistant et voice_engine sont None, on les crée
        if assistant is None:
            from core.assistant import ZodiacAssistant
            self.assistant = ZodiacAssistant()
        else:
            self.assistant = assistant
            
        if voice_engine is None:
            from core.voice_engine import VoiceEngine
            self.voice_engine = VoiceEngine()
        else:
            self.voice_engine = voice_engine
            
        self.microphone_active = False
        self._setup_ui()
        
    def _setup_ui(self):
        """Interface responsive"""
        # Header
        if self.mobile_mode:
            header_height = 50
            title_font = ("Segoe UI", 18, "bold")
        else:
            header_height = 60
            title_font = ("Segoe UI", 22, "bold")
            
        header = ctk.CTkFrame(self, fg_color="#111118", height=header_height)
        header.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            header,
            text="🤖 EXOCORTEX ASSISTANT",
            font=title_font,
            text_color="#6C63FF"
        ).pack(pady=10)
        
        # Zone de chat
        chat_height = 380 if self.mobile_mode else 450
        self.chat_container = ctk.CTkScrollableFrame(
            self,
            fg_color="#0A0A0F",
            height=chat_height
        )
        self.chat_container.pack(fill="both", expand=True, padx=15 if not self.mobile_mode else 10, pady=5)
        
        # Message de bienvenue
        self._add_welcome_message()
        
        # Zone de saisie
        input_height = 80 if self.mobile_mode else 90
        input_frame = ctk.CTkFrame(self, fg_color="#111118", height=input_height)
        input_frame.pack(fill="x", side="bottom", 
                        padx=15 if not self.mobile_mode else 10, 
                        pady=15 if not self.mobile_mode else 10)
        
        # Microphone
        mic_size = 50 if self.mobile_mode else 55
        self.mic_btn = ctk.CTkButton(
            input_frame,
            text="🎤",
            width=mic_size,
            height=mic_size,
            font=("Segoe UI", 20),
            fg_color="#6C63FF",
            command=self._toggle_mic
        )
        self.mic_btn.pack(side="left", padx=(15 if not self.mobile_mode else 10, 5))
        
        # Champ texte
        entry_height = 45 if self.mobile_mode else 50
        self.text_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Tapez votre message ici...",
            height=entry_height,
            font=("Segoe UI", 14)
        )
        self.text_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.text_entry.bind("<Return>", lambda e: self._send_message())
        
        # Bouton envoyer
        send_btn = ctk.CTkButton(
            input_frame,
            text="➤",
            width=mic_size,
            height=mic_size,
            font=("Segoe UI", 20),
            fg_color="#00D4AA",
            command=self._send_message
        )
        send_btn.pack(side="right", padx=(5, 15 if not self.mobile_mode else 10))
        
        # Actions rapides (uniquement sur desktop)
        if not self.mobile_mode:
            actions_frame = ctk.CTkFrame(self, fg_color="transparent", height=50)
            actions_frame.pack(fill="x", padx=20, pady=10)
            
            quick_actions = [
                ("🌤️ Météo", "#FFB74D"),
                ("🎵 Musique", "#6C63FF"),
                ("📅 Agenda", "#00D4AA"),
                ("📧 Email", "#FF4D4D")
            ]
            
            for action, color in quick_actions:
                btn = ctk.CTkButton(
                    actions_frame,
                    text=action,
                    height=40,
                    font=("Segoe UI", 13),
                    fg_color=color,
                    hover_color=f"{color}DD",
                    command=lambda a=action: self._quick_action(a)
                )
                btn.pack(side="left", padx=5, expand=True, fill="x")
                
    def _add_welcome_message(self):
        """Ajoute le message de bienvenue"""
        welcome_frame = ctk.CTkFrame(
            self.chat_container,
            fg_color="#111118",
            corner_radius=15
        )
        welcome_frame.pack(fill="x", pady=10, padx=5)
        
        welcome_text = "🎯 EXOCORTEX ACTIVÉ\n\n" \
                      "• Assistant vocal intelligent\n" \
                      "• Gestionnaire d'applications\n" \
                      "• Surveillance système\n\n" \
                      "🔊 Dites 'Exocortex' ou tapez un message"
                      
        ctk.CTkLabel(
            welcome_frame,
            text=welcome_text,
            font=("Segoe UI", 14),
            text_color="#00D4AA",
            justify="left"
        ).pack(padx=20 if not self.mobile_mode else 15, 
               pady=20 if not self.mobile_mode else 15)
               
    def _toggle_mic(self):
        """Active/désactive le microphone"""
        if not self.microphone_active:
            # Activer le micro
            self.microphone_active = True
            self.mic_btn.configure(fg_color="#FF4D4D", text="🔴")
            self._add_message("system", "🎤 Microphone activé - Parlez maintenant...")
            
            # Démarrer l'écoute dans un thread
            threading.Thread(target=self._start_listening, daemon=True).start()
        else:
            # Désactiver le micro
            self.microphone_active = False
            self.mic_btn.configure(fg_color="#6C63FF", text="🎤")
            self._add_message("system", "🎤 Microphone désactivé")
            
    def _start_listening(self):
        """Démarre l'écoute vocale"""
        try:
            self.voice_engine.start_listening()
            # Simulation de transcription après 2 secondes
            threading.Timer(2.0, self._simulate_voice_input).start()
        except Exception as e:
            self._add_message("error", f"Erreur microphone: {str(e)}")
            
    def _simulate_voice_input(self):
        """Simule une entrée vocale (pour le mode démo)"""
        if self.microphone_active:
            simulated_phrases = [
                "Bonjour Exocortex",
                "Quelle heure est-il ?",
                "Ouvre mes applications",
                "Quelle est la météo aujourd'hui ?",
                "Joue de la musique"
            ]
            
            import random
            phrase = random.choice(simulated_phrases)
            self._add_message("user", f"🎤 {phrase}")
            
            # Traiter la phrase
            threading.Timer(1.0, lambda: self._process_voice_input(phrase)).start()
            
    def _process_voice_input(self, text):
        """Traite l'entrée vocale"""
        response = self.assistant.process_query(text)
        self._add_message("exocortex", response)
        
        # Désactiver le micro après réponse
        if self.microphone_active:
            self.microphone_active = False
            self.mic_btn.configure(fg_color="#6C63FF", text="🎤")
            
    def _send_message(self):
        """Envoie un message texte"""
        text = self.text_entry.get().strip()
        if not text:
            return
            
        # Effacer le champ
        self.text_entry.delete(0, "end")
        
        # Ajouter le message utilisateur
        self._add_message("user", text)
        
        # Traiter la requête dans un thread
        threading.Thread(target=self._process_text_input, args=(text,), daemon=True).start()
        
    def _process_text_input(self, text):
        """Traite l'entrée texte"""
        # Simuler un délai de traitement
        import time
        time.sleep(0.5)
        
        # Obtenir la réponse de l'assistant
        response = self.assistant.process_query(text)
        
        # Ajouter la réponse dans le thread principal
        self.after(0, lambda: self._add_message("exocortex", response))
        
    def _quick_action(self, action):
        """Action rapide"""
        responses = {
            "🌤️ Météo": "☀️ **Météo Paris**\nTempérature: 22°C\nConditions: Ensoleillé\nVent: 15 km/h\nHumidité: 65%",
            "🎵 Musique": "🎶 **Lecture en cours**\nTitre: Shape of You\nArtiste: Ed Sheeran\nDurée: 3:54\nVolume: 75%",
            "📅 Agenda": "📅 **Agenda du jour**\n• 10:00 - Réunion équipe\n• 14:30 - Cours Python\n• 16:00 - Rendez-vous client\n• 18:00 - Séance sport",
            "📧 Email": "📧 **Boîte de réception**\n3 nouveaux emails\n1. Newsletter Tech - Non lu\n2. Facture - Important\n3. Réunion - À confirmer"
        }
        
        response = responses.get(action, f"Action '{action}' exécutée")
        self._add_message("exocortex", response)
        
    def _add_message(self, sender, text):
        """Ajoute un message au chat"""
        # Définir les couleurs selon l'expéditeur
        if sender == "user":
            color = "#6C63FF"
            bg_color = "#1E1E2E"
            anchor = "e"
        elif sender == "exocortex":
            color = "#00D4AA"
            bg_color = "#111118"
            anchor = "w"
        elif sender == "system":
            color = "#FFB74D"
            bg_color = "#1A1A1F"
            anchor = "center"
        else:  # error
            color = "#FF4D4D"
            bg_color = "#2A1A1A"
            anchor = "center"
            
        # Créer le frame du message
        msg_frame = ctk.CTkFrame(
            self.chat_container,
            fg_color=bg_color,
            corner_radius=15
        )
        
        # Déterminer la largeur de texte selon le mode
        wrap_length = 350 if not self.mobile_mode else 250
        
        # Créer le label avec le message
        msg_label = ctk.CTkLabel(
            msg_frame,
            text=text,
            font=("Segoe UI", 13),
            text_color=color,
            wraplength=wrap_length,
            justify="left"
        )
        msg_label.pack(padx=15, pady=12)
        
        # Ajouter au conteneur avec l'ancre appropriée
        msg_frame.pack(fill="x", pady=8, padx=5, anchor=anchor)
        
        # Défiler vers le bas pour voir le nouveau message
        self.chat_container._parent_canvas.yview_moveto(1.0)
        
    def clear_chat(self):
        """Efface la conversation"""
        for widget in self.chat_container.winfo_children():
            widget.destroy()
        self._add_welcome_message()