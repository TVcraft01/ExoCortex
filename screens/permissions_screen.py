# screens/permissions_screen.py - AVEC MOBILE_MODE
import customtkinter as ctk

class PermissionsScreen(ctk.CTkFrame):
    def __init__(self, parent, controller, mobile_mode=True):
        super().__init__(parent, fg_color="#0A0A0F")
        self.controller = controller
        self.mobile_mode = mobile_mode
        self.app_vars = {}
        self._setup_ui()
        
    def _setup_ui(self):
        """Gestion des permissions - responsive"""
        # Titre principal
        title_font = ("Segoe UI", 28 if not self.mobile_mode else 24, "bold")
        ctk.CTkLabel(
            self,
            text="Donnez accès à vos apps",
            font=title_font,
            text_color="#FFFFFF"
        ).pack(pady=(60 if not self.mobile_mode else 40, 15))
        
        # Description
        desc_font = ("Segoe UI", 16 if not self.mobile_mode else 14)
        ctk.CTkLabel(
            self,
            text="Activez les applications avec lesquelles\nEXOCORTEX peut interagir.",
            font=desc_font,
            text_color="#888888",
            justify="center"
        ).pack(pady=(0, 5))
        
        note_font = ("Segoe UI", 13 if not self.mobile_mode else 12)
        ctk.CTkLabel(
            self,
            text="Toutes les apps sont désactivées par défaut.",
            font=note_font,
            text_color="#666666"
        ).pack(pady=(0, 50 if not self.mobile_mode else 40))
        
        # Liste des applications
        apps = [
            ("Messages", "💬"),
            ("Photos", "🖼️"),
            ("Musique", "🎵"),
            ("Éditeur", "📝"),
            ("Réglages", "⚙️"),
            ("Email", "📧"),
            ("Agenda", "📅")
        ]
        
        # Checkboxes pour chaque app
        padx_value = 100 if not self.mobile_mode else 80
        frame_height = 55 if not self.mobile_mode else 50
        app_font = ("Segoe UI", 18 if not self.mobile_mode else 16)
        
        for app_name, emoji in apps:
            frame = ctk.CTkFrame(self, fg_color="transparent", height=frame_height)
            frame.pack(fill="x", padx=padx_value, pady=4)
            
            # Label avec émoji
            ctk.CTkLabel(
                frame,
                text=f"{emoji}  {app_name}",
                font=app_font,
                text_color="#FFFFFF",
                anchor="w"
            ).pack(side="left", padx=(20, 0))
            
            # Checkbox (Photos activée par défaut comme l'image)
            var = ctk.BooleanVar(value=(app_name == "Photos"))
            self.app_vars[app_name] = var
            
            checkbox_size = 35 if not self.mobile_mode else 30
            checkbox = ctk.CTkCheckBox(
                frame,
                text="",
                variable=var,
                width=checkbox_size,
                height=checkbox_size,
                fg_color="#6C63FF",
                hover_color="#5A52E0",
                border_width=1
            )
            checkbox.pack(side="right", padx=(0, 20))
            
        # Bouton Relancer la recherche
        button_height = 45 if not self.mobile_mode else 40
        button_font = ("Segoe UI", 15 if not self.mobile_mode else 14)
        
        ctk.CTkButton(
            self,
            text="Relancer la recherche",
            font=button_font,
            height=button_height,
            fg_color="transparent",
            hover_color="#1A1A1F",
            border_color="#6C63FF",
            border_width=1,
            command=self.rescan_apps
        ).pack(pady=(50 if not self.mobile_mode else 40, 25), padx=padx_value)
        
        # Bouton Terminer
        finish_height = 55 if not self.mobile_mode else 50
        finish_font = ("Segoe UI", 18 if not self.mobile_mode else 16, "bold")
        
        ctk.CTkButton(
            self,
            text="Terminer la configuration",
            font=finish_font,
            height=finish_height,
            fg_color="#00D4AA",
            hover_color="#00B894",
            command=self.finish_setup
        ).pack(pady=(10, 50 if not self.mobile_mode else 40), padx=padx_value)
        
    def rescan_apps(self):
        """Rescanne les applications"""
        print("🔄 Recherche d'applications...")
        
    def finish_setup(self):
        """Termine la configuration et lance le dashboard"""
        # Récupérer les permissions
        permissions = {app: var.get() for app, var in self.app_vars.items()}
        print(f"✅ Permissions activées: {permissions}")
        
        # Passer au dashboard principal
        self.controller.show_screen("dashboard")