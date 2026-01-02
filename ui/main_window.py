# ui/main_window.py - VERSION SIMPLIFIÉE MOBILE
import customtkinter as ctk
from ui.tabs.assistant_tab import AssistantTab
from ui.tabs.vault_tab import VaultTab
from ui.tabs.dashboard_tab import DashboardTab

class MainWindow:
    """Fenêtre principale MOBILE SIMPLIFIÉE"""
    
    def __init__(self, assistant=None, voice_engine=None, mobile_mode=True):
        self.assistant = assistant
        self.voice_engine = voice_engine
        self.mobile_mode = mobile_mode
        
        # Créer la fenêtre
        self.root = ctk.CTk()
        self._setup_window()
        self._setup_ui()
        
    def _setup_window(self):
        """Configuration mobile simple"""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # TAILLE MOBILE FIXE
        self.root.geometry("360x640")
        self.root.title("Zodiac Mobile")
        self.root.resizable(False, False)
        
    def _setup_ui(self):
        """Interface ultra-simple"""
        # Frame principal qui prend tout
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#0A0A0F")
        self.main_frame.pack(fill="both", expand=True)
        
        # Créer les onglets
        self._create_tabs()
        
        # Créer la navigation
        self._create_navigation()
        
    def _create_tabs(self):
        """Crée les onglets - version SIMPLE"""
        # Frame pour le contenu (90% de l'écran)
        self.content_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color="#0A0A0F",
            height=580
        )
        self.content_frame.pack(fill="both", expand=True, padx=0, pady=0)
        self.content_frame.pack_propagate(False)  # Garde la hauteur
        
        # Créer les onglets MAIS NE PAS LES AFFICHER TOUT DE SUITE
        self.tabs = {
            "assistant": AssistantTab(self.content_frame, self.assistant, self.voice_engine),
            "vault": VaultTab(self.content_frame),
            "dashboard": DashboardTab(self.content_frame)
        }
        
        # Afficher seulement l'assistant
        self.tabs["assistant"].pack(fill="both", expand=True)
        self.current_tab = "assistant"
        
    def _create_navigation(self):
        """Navigation bas - SIMPLE"""
        # Frame de navigation (10% de l'écran)
        self.nav_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#111118",
            height=60,
            corner_radius=0
        )
        self.nav_frame.pack(side="bottom", fill="x")
        
        # 3 boutons égaux
        self.nav_frame.grid_columnconfigure(0, weight=1)
        self.nav_frame.grid_columnconfigure(1, weight=1)
        self.nav_frame.grid_columnconfigure(2, weight=1)
        
        # Boutons de navigation
        nav_items = [
            ("🤖", "assistant"),
            ("📁", "vault"), 
            ("📊", "dashboard")
        ]
        
        self.nav_buttons = []
        
        for col, (emoji, tab_key) in enumerate(nav_items):
            btn = ctk.CTkButton(
                self.nav_frame,
                text=emoji,
                font=("Segoe UI", 24),
                fg_color="transparent",
                hover_color="#1E1E2E",
                width=60,
                height=60,
                command=lambda k=tab_key: self._switch_tab_simple(k)
            )
            btn.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
            self.nav_buttons.append((btn, tab_key))
            
            # Style actif pour le premier
            if tab_key == "assistant":
                btn.configure(fg_color="#6C63FF")
                
    def _switch_tab_simple(self, tab_key):
        """Change d'onglet - SIMPLE"""
        if tab_key == self.current_tab:
            return
            
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
                
        # 4. Mettre à jour l'onglet courant
        self.current_tab = tab_key
        
        # 5. Forcer un update
        self.root.update()
        
    def run(self):
        """Lance l'application"""
        self.root.mainloop()