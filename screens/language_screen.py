# screens/language_screen.py - CORRIGÉ
import customtkinter as ctk

class LanguageScreen(ctk.CTkFrame):
    def __init__(self, parent, controller, mobile_mode=True):
        super().__init__(parent, fg_color="#0A0A0F")
        self.controller = controller
        self.mobile_mode = mobile_mode
        self._setup_ui()
        
    def _setup_ui(self):
        """Interface responsive"""
        # Logo EXOCORTEX
        logo_font = ("Segoe UI", 40 if not self.mobile_mode else 32, "bold")
        self.logo_label = ctk.CTkLabel(
            self,
            text="EXOCORTEX",
            font=logo_font,
            text_color="#6C63FF"
        )
        self.logo_label.pack(pady=(80 if not self.mobile_mode else 60, 30))
        
        # Sous-titre
        subtitle_font = ("Segoe UI", 22 if not self.mobile_mode else 18)
        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Sélectionnez votre langue",
            font=subtitle_font,
            text_color="#FFFFFF"
        )
        self.subtitle_label.pack(pady=(0, 50 if not self.mobile_mode else 40))
        
        # Liste des langues
        languages = [
            ("Français", "🇫🇷"),
            ("English", "🇬🇧"),
            ("Deutsch", "🇩🇪"),
            ("日本語", "🇯🇵"),
            ("中文", "🇨🇳"),
            ("Español", "🇪🇸"),
            ("Italiano", "🇮🇹"),
            ("Português", "🇵🇹")
        ]
        
        # Configuration responsive pour les boutons
        button_padx = 120 if not self.mobile_mode else 60
        button_height = 55 if not self.mobile_mode else 50
        button_font = ("Segoe UI", 18) if not self.mobile_mode else ("Segoe UI", 16)
        
        for lang_name, flag in languages:
            btn = ctk.CTkButton(
                self,
                text=f"{flag}  {lang_name}",
                font=button_font,
                height=button_height,
                fg_color="transparent",
                hover_color="#1A1A1F",
                border_color="#444444",
                border_width=1,
                command=lambda l=lang_name: self.select_language(l)
            )
            btn.pack(fill="x", padx=button_padx, pady=5)
            
        # Bouton Continuer
        continue_font = ("Segoe UI", 18 if not self.mobile_mode else 16, "bold")
        continue_height = 55 if not self.mobile_mode else 50
        
        self.continue_btn = ctk.CTkButton(
            self,
            text="Continuer",
            font=continue_font,
            height=continue_height,
            fg_color="#6C63FF",
            hover_color="#5A52E0",
            state="disabled",
            command=lambda: self.controller.show_screen("setup")
        )
        self.continue_btn.pack(pady=(40, 30), padx=button_padx)
        
    def select_language(self, language):
        """Sélectionne une langue"""
        print(f"🌐 Langue sélectionnée: {language}")
        self.continue_btn.configure(state="normal")