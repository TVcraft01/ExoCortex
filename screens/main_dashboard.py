# screens/main_dashboard.py - Dashboard responsive
import customtkinter as ctk
from ui.tabs.assistant_tab import AssistantTab
from ui.tabs.vault_tab import VaultTab
from ui.tabs.dashboard_tab import DashboardTab

class MainDashboard(ctk.CTkFrame):
    """Dashboard principal EXOCORTEX - Version responsive"""
    
    def __init__(self, parent, controller, mobile_mode):
        super().__init__(parent, fg_color="#0A0A0F")
        self.controller = controller
        self.mobile_mode = mobile_mode
        
        # Configuration responsive
        if not self.mobile_mode:
            # Mode desktop - utiliser grid
            self._setup_desktop_ui()
        else:
            # Mode mobile - utiliser pack
            self._setup_mobile_ui()
            
    def _setup_mobile_ui(self):
        """Interface mobile (votre design existant)"""
        # Header
        header = ctk.CTkFrame(self, fg_color="#111118", height=70)
        header.pack(fill="x", padx=0, pady=0)
        
        ctk.CTkLabel(
            header,
            text="EXOCORTEX",
            font=("Segoe UI", 22, "bold"),
            text_color="#6C63FF"
        ).pack(side="left", padx=20, pady=15)
        
        # Zone de contenu
        self.content_frame = ctk.CTkFrame(self, fg_color="#0A0A0F", height=500)
        self.content_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Créer les onglets
        self._create_tabs()
        
        # Navigation bas
        self._create_mobile_navigation()
        
    def _setup_desktop_ui(self):
        """Interface desktop avec sidebar"""
        # Layout principal desktop
        self.grid_columnconfigure(0, weight=0)  # Sidebar
        self.grid_columnconfigure(1, weight=1)  # Contenu
        
        # SIDEBAR (gauche)
        self.sidebar = ctk.CTkFrame(self, fg_color="#111118", width=200)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # Logo sidebar
        ctk.CTkLabel(
            self.sidebar,
            text="EXOCORTEX",
            font=("Segoe UI", 24, "bold"),
            text_color="#6C63FF"
        ).pack(pady=(30, 40))
        
        # Boutons sidebar
        nav_items = [
            ("🤖 Assistant", "assistant"),
            ("📁 Applications", "vault"),
            ("📊 Dashboard", "dashboard"),
            ("⚙️ Paramètres", "settings")
        ]
        
        self.sidebar_buttons = {}
        for text, key in nav_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                font=("Segoe UI", 14),
                height=45,
                fg_color="transparent",
                hover_color="#1E1E2E",
                anchor="w",
                command=lambda k=key: self._switch_tab(k)
            )
            btn.pack(fill="x", padx=15, pady=5)
            self.sidebar_buttons[key] = btn
            
        # Zone de contenu principale (droite)
        self.content_frame = ctk.CTkFrame(self, fg_color="#0A0A0F")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Créer les onglets
        self._create_tabs()
        
        # Afficher assistant par défaut
        self._switch_tab("assistant")
        
    def _create_tabs(self):
        """Crée les onglets"""
        # Note: On passe le mobile_mode aux onglets
        self.tabs = {
            "assistant": AssistantTab(self.content_frame, None, None, self.mobile_mode),
            "vault": VaultTab(self.content_frame, self.mobile_mode),
            "dashboard": DashboardTab(self.content_frame, self.mobile_mode)
        }
        
        # Stocker l'onglet courant
        self.current_tab = "assistant"
        
    def _create_mobile_navigation(self):
        """Navigation mobile (bas de l'écran)"""
        if self.mobile_mode:
            nav_frame = ctk.CTkFrame(self, fg_color="#111118", height=60, corner_radius=0)
            nav_frame.pack(side="bottom", fill="x")
            
            # 3 boutons égaux
            nav_frame.grid_columnconfigure(0, weight=1)
            nav_frame.grid_columnconfigure(1, weight=1)
            nav_frame.grid_columnconfigure(2, weight=1)
            
            nav_items = [
                ("🤖", "assistant"),
                ("📁", "vault"), 
                ("📊", "dashboard")
            ]
            
            self.nav_buttons = []
            
            for col, (emoji, tab_key) in enumerate(nav_items):
                btn = ctk.CTkButton(
                    nav_frame,
                    text=emoji,
                    font=("Segoe UI", 24),
                    fg_color="transparent",
                    hover_color="#1E1E2E",
                    width=60,
                    height=60,
                    command=lambda k=tab_key: self._switch_tab(k)
                )
                btn.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
                self.nav_buttons.append((btn, tab_key))
                
                # Style actif pour le premier
                if tab_key == "assistant":
                    btn.configure(fg_color="#6C63FF")
                    
            # Afficher l'onglet assistant par défaut
            self.tabs["assistant"].pack(fill="both", expand=True)
            
    def _switch_tab(self, tab_key):
        """Change d'onglet"""
        if tab_key == self.current_tab:
            return
            
        # Mode mobile
        if self.mobile_mode:
            # 1. Cacher l'onglet actuel
            self.tabs[self.current_tab].pack_forget()
            
            # 2. Afficher le nouveau
            self.tabs[tab_key].pack(fill="both", expand=True)
            
            # 3. Mettre à jour le style des boutons
            for btn, key in self.nav_buttons:
                if key == tab_key:
                    btn.configure(fg_color="#6C63FF")
                else:
                    btn.configure(fg_color="transparent")
                    
        # Mode desktop
        else:
            # 1. Cacher l'onglet actuel
            self.tabs[self.current_tab].grid_remove()
            
            # 2. Afficher le nouveau
            self.tabs[tab_key].grid(row=0, column=0, sticky="nsew")
            
            # 3. Mettre à jour le style des boutons sidebar
            for key, btn in self.sidebar_buttons.items():
                if key == tab_key:
                    btn.configure(fg_color="#6C63FF")
                else:
                    btn.configure(fg_color="transparent")
                    
        # 4. Mettre à jour
        self.current_tab = tab_key