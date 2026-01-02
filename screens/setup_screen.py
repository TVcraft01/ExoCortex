# screens/setup_screen.py - AVEC MOBILE_MODE
import customtkinter as ctk

class SetupScreen(ctk.CTkFrame):
    def __init__(self, parent, controller, mobile_mode=True):
        super().__init__(parent, fg_color="#0A0A0F")
        self.controller = controller
        self.mobile_mode = mobile_mode
        self._setup_ui()
        
    def _setup_ui(self):
        """Configuration de l'agent IA - responsive"""
        # Logo
        logo_font = ("Segoe UI", 40 if not self.mobile_mode else 32, "bold")
        ctk.CTkLabel(
            self,
            text="EXOCORTEX",
            font=logo_font,
            text_color="#6C63FF"
        ).pack(pady=(80 if not self.mobile_mode else 60, 20))
        
        # Titre
        title_font = ("Segoe UI", 24 if not self.mobile_mode else 20)
        ctk.CTkLabel(
            self,
            text="Configurez votre agent IA",
            font=title_font,
            text_color="#FFFFFF"
        ).pack(pady=(0, 50 if not self.mobile_mode else 40))
        
        # Options de configuration
        options = [
            ("Personnalité", ["Professionnel", "Amical", "Strict", "Créatif"]),
            ("Voix", ["Masculine", "Féminine", "Neutre"]),
            ("Niveau de détail", ["Minimal", "Standard", "Détaillé"]),
            ("Notifications", ["Activées", "Désactivées"])
        ]
        
        padx_value = 80 if not self.mobile_mode else 60
        label_width = 150 if not self.mobile_mode else 120
        
        for label, values in options:
            frame = ctk.CTkFrame(self, fg_color="transparent")
            frame.pack(fill="x", padx=padx_value, pady=12)
            
            ctk.CTkLabel(
                frame,
                text=label,
                font=("Segoe UI", 14),
                text_color="#CCCCCC",
                width=label_width
            ).pack(side="left")
            
            combo_width = 200 if not self.mobile_mode else 180
            combo = ctk.CTkComboBox(
                frame,
                values=values,
                font=("Segoe UI", 14),
                fg_color="#1A1A1F",
                border_color="#6C63FF",
                button_color="#6C63FF",
                dropdown_fg_color="#1A1A1F",
                width=combo_width
            )
            combo.set(values[0])
            combo.pack(side="right")
            
        # Bouton Démarrer
        button_height = 55 if not self.mobile_mode else 50
        button_font = ("Segoe UI", 18, "bold") if not self.mobile_mode else ("Segoe UI", 16, "bold")
        
        ctk.CTkButton(
            self,
            text="Démarrer la configuration",
            font=button_font,
            height=button_height,
            fg_color="#00D4AA",
            hover_color="#00B894",
            command=lambda: self.controller.show_screen("permissions")
        ).pack(pady=(60 if not self.mobile_mode else 40, 20), padx=padx_value)