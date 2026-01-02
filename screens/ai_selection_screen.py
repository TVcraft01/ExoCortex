import customtkinter as ctk
import tkinter as tk

class AISelectionScreen(ctk.CTkFrame):
    def __init__(self, parent, controller, mobile_mode=True):
        super().__init__(parent, fg_color="#0A0A0F")
        self.controller = controller
        self.mobile_mode = mobile_mode
        self._setup_ui()
        
    def _setup_ui(self):
        # Titre principal
        title_font = ("Segoe UI", 28 if not self.mobile_mode else 24, "bold")
        ctk.CTkLabel(
            self,
            text="Choisissez votre IA",
            font=title_font,
            text_color="#FFFFFF"
        ).pack(pady=(60 if not self.mobile_mode else 40, 15))
        
        # Description
        desc_font = ("Segoe UI", 16 if not self.mobile_mode else 14)
        ctk.CTkLabel(
            self,
            text="Sélectionnez le modèle d'IA que vous préférez.",
            font=desc_font,
            text_color="#888888",
            justify="center"
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            self,
            text="Vous pourrez entrer votre clé API et configurer la connexion.",
            font=("Segoe UI", 13 if not self.mobile_mode else 12),
            text_color="#666666"
        ).pack(pady=(0, 50 if not self.mobile_mode else 40))
        
        # Options IA
        self.ai_var = tk.StringVar(value="deepseek")
        
        ai_options = [
            ("🤖 DeepSeek (Recommandé)", "deepseek"),
            ("🌟 Gemini (Google)", "gemini"),
            ("🔧 Local (Mode démo)", "local")
        ]
        
        for text, value in ai_options:
            frame = ctk.CTkFrame(self, fg_color="#111111", height=60)
            frame.pack(fill="x", padx=80, pady=4)
            
            ctk.CTkLabel(
                frame,
                text=text,
                font=("Segoe UI", 15),
                text_color="#FFFFFF"
            ).pack(side="left", padx=15)
            
            ctk.CTkRadioButton(
                frame,
                text="",
                variable=self.ai_var,
                value=value,
                fg_color="#6C63FF",
                hover_color="#5A52E0",
                width=30,
                height=30
            ).pack(side="right", padx=15)
        
        # Frame pour la clé API
        api_frame = ctk.CTkFrame(self, fg_color="transparent")
        api_frame.pack(fill="x", padx=80, pady=20)
        
        ctk.CTkLabel(
            api_frame,
            text="Clé API (optionnel - pour DeepSeek/Gemini):",
            font=("Segoe UI", 14),
            text_color="#888888"
        ).pack(anchor="w", pady=(0, 5))
        
        self.api_key_entry = ctk.CTkEntry(
            api_frame,
            placeholder_text="Entrez votre clé API...",
            height=40,
            font=("Segoe UI", 14),
            show="*"
        )
        self.api_key_entry.pack(fill="x", pady=5)
        
        # Case à cocher pour utiliser internet
        self.use_internet_var = tk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            api_frame,
            text="Utiliser internet pour les requêtes IA",
            variable=self.use_internet_var,
            fg_color="#6C63FF",
            hover_color="#5A52E0",
            font=("Segoe UI", 13)
        ).pack(anchor="w", pady=10)
        
        # Bouton Continuer
        button_height = 55 if not self.mobile_mode else 50
        button_font = ("Segoe UI", 18, "bold") if not self.mobile_mode else ("Segoe UI", 16, "bold")
        
        ctk.CTkButton(
            self,
            text="Continuer",
            font=button_font,
            height=button_height,
            fg_color="#00D4AA",
            hover_color="#00B894",
            command=self.save_and_continue
        ).pack(pady=(60 if not self.mobile_mode else 40, 20), padx=80)
        
    def save_and_continue(self):
        """Sauvegarde la configuration IA et passe à l'écran suivant"""
        ai_choice = self.ai_var.get()
        api_key = self.api_key_entry.get()
        use_internet = self.use_internet_var.get()
        
        # Sauvegarder dans le contrôleur (ou configuration globale)
        self.controller.config["ai_choice"] = ai_choice
        self.controller.config["api_key"] = api_key
        self.controller.config["use_internet"] = use_internet
        
        print(f"🤖 IA sélectionnée: {ai_choice}")
        print(f"🔑 Clé API: {'Oui' if api_key else 'Non'}")
        print(f"🌐 Utiliser internet: {use_internet}")
        
        # Aller à l'écran des permissions
        self.controller.show_screen("permissions")