# ui/tabs/vault_tab.py - RESPONSIVE
import customtkinter as ctk

class VaultTab(ctk.CTkFrame):
    def __init__(self, parent, mobile_mode=True):
        super().__init__(parent, fg_color="#0A0A0F")
        self.mobile_mode = mobile_mode
        self._setup_ui()
        
    def _setup_ui(self):
        """Interface responsive"""
        # Header
        title_font = ("Segoe UI", 22 if not self.mobile_mode else 20, "bold")
        ctk.CTkLabel(
            self,
            text="📁 GESTIONNAIRE D'APPS",
            font=title_font,
            text_color="#6C63FF"
        ).pack(pady=25 if not self.mobile_mode else 20)
        
        # Barre recherche
        search_padx = 40 if not self.mobile_mode else 20
        search_height = 50 if not self.mobile_mode else 45
        
        ctk.CTkEntry(
            self,
            placeholder_text="🔍 Rechercher une application...",
            height=search_height,
            font=("Segoe UI", 14)
        ).pack(fill="x", padx=search_padx, pady=15)
        
        # Liste scrollable
        scroll_height = 450 if not self.mobile_mode else 380
        scroll_frame = ctk.CTkScrollableFrame(
            self, 
            fg_color="transparent", 
            height=scroll_height
        )
        scroll_frame.pack(fill="both", expand=True, 
                         padx=20 if not self.mobile_mode else 10, 
                         pady=10)
        
        # Apps (plus sur desktop)
        apps = [
            ("🎵 Spotify", "Musique", "#1DB954"),
            ("🌐 Chrome", "Navigateur", "#4285F4"),
            ("💬 WhatsApp", "Messagerie", "#25D366"),
            ("📷 Instagram", "Social", "#E4405F"),
            ("📧 Gmail", "Email", "#EA4335"),
            ("📁 Explorateur", "Fichiers", "#757575"),
            ("🎮 Steam", "Jeux", "#171A21"),
            ("🎥 YouTube", "Vidéo", "#FF0000"),
        ]
        
        for name, category, color in apps:
            app_height = 80 if not self.mobile_mode else 70
            frame = ctk.CTkFrame(scroll_frame, fg_color="#111118", height=app_height)
            frame.pack(fill="x", pady=5)
            
            # Icone et nom
            icon_frame = ctk.CTkFrame(frame, fg_color="transparent", width=50)
            icon_frame.pack(side="left", padx=15)
            
            ctk.CTkLabel(
                icon_frame,
                text=name.split()[0],  # Juste l'émoji
                font=("Segoe UI", 24),
                text_color=color
            ).pack()
            
            # Détails
            details_frame = ctk.CTkFrame(frame, fg_color="transparent")
            details_frame.pack(side="left", fill="both", expand=True, padx=10)
            
            ctk.CTkLabel(
                details_frame,
                text=name,
                font=("Segoe UI", 16 if not self.mobile_mode else 14),
                text_color="#FFFFFF"
            ).pack(anchor="w", pady=(10, 2))
            
            ctk.CTkLabel(
                details_frame,
                text=category,
                font=("Segoe UI", 12),
                text_color="#888888"
            ).pack(anchor="w")
            
            # Bouton lancer
            btn_size = 45 if not self.mobile_mode else 40
            ctk.CTkButton(
                frame,
                text="▶",
                width=btn_size,
                height=btn_size,
                font=("Segoe UI", 14),
                fg_color="#00D4AA",
                hover_color="#00B894"
            ).pack(side="right", padx=15)