# ui/tabs/dashboard_tab.py - MODIFIÉ POUR ACCEPTER MOBILE_MODE
import customtkinter as ctk

class DashboardTab(ctk.CTkFrame):
    def __init__(self, parent, mobile_mode=True):
        super().__init__(parent, fg_color="#0A0A0F")
        self.mobile_mode = mobile_mode
        self._setup_ui()
        
    def _setup_ui(self):
        """Interface simple - responsive"""
        # Header
        title_font = ("Segoe UI", 22 if not self.mobile_mode else 20, "bold")
        ctk.CTkLabel(
            self,
            text="📊 SURVEILLANCE SYSTÈME",
            font=title_font,
            text_color="#6C63FF"
        ).pack(pady=25 if not self.mobile_mode else 20)
        
        # Métriques en grille
        metrics_frame = ctk.CTkFrame(self, fg_color="transparent")
        metrics_frame.pack(fill="both", expand=True, 
                          padx=20 if not self.mobile_mode else 10, 
                          pady=15 if not self.mobile_mode else 10)
        
        metrics = [
            ("⚡ CPU", "45%", "#FF4D4D"),
            ("💾 RAM", "68%", "#6C63FF"),
            ("💿 DISQUE", "32%", "#00D4AA"),
            ("🌐 RÉSEAU", "12%", "#FFB74D"),
            ("🔋 BATTERIE", "85%", "#4CAF50"),
            ("🎮 GPU", "23%", "#9C27B0")
        ]
        
        # Nombre de colonnes selon le mode
        columns = 3 if not self.mobile_mode else 2
        
        for i, (name, value, color) in enumerate(metrics):
            row = i // columns
            col = i % columns
            
            widget_size = 140 if not self.mobile_mode else 150
            widget = ctk.CTkFrame(
                metrics_frame,
                fg_color="#111118",
                width=widget_size,
                height=widget_size,
                corner_radius=15
            )
            widget.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(
                widget,
                text=name,
                font=("Segoe UI", 14),
                text_color=color
            ).place(relx=0.5, rely=0.3, anchor="center")
            
            ctk.CTkLabel(
                widget,
                text=value,
                font=("Segoe UI", 28, "bold"),
                text_color="#FFFFFF"
            ).place(relx=0.5, rely=0.6, anchor="center")
            
        # Boutons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent", height=50)
        btn_frame.pack(fill="x", padx=30 if not self.mobile_mode else 20, pady=15)
        
        btn_height = 45 if not self.mobile_mode else 40
        btn_font = ("Segoe UI", 14) if not self.mobile_mode else ("Segoe UI", 12)
        
        ctk.CTkButton(
            btn_frame,
            text="🔄 Rafraîchir",
            height=btn_height,
            font=btn_font,
            fg_color="#1E1E2E"
        ).pack(side="left", padx=5, expand=True, fill="x")
        
        ctk.CTkButton(
            btn_frame,
            text="📊 Détails",
            height=btn_height,
            font=btn_font,
            fg_color="#6C63FF"
        ).pack(side="left", padx=5, expand=True, fill="x")