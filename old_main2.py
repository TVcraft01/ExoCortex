# main.py - EXOCORTEX MOBILE COMPLET
import customtkinter as ctk
import tkinter as tk
import os
import sys
import json
from tkinter import messagebox

class ExocortexApp:
    """Application EXOCORTEX - Version mobile complète"""
    
    def __init__(self):
        # FORCER LE MODE MOBILE
        self.mobile_mode = True
        
        # Configuration
        ctk.set_appearance_mode("dark")
        
        # Fenêtre mobile
        self.root = ctk.CTk()
        self._setup_mobile_window()
        
        # Configuration
        self.config = {
            "language": "fr",
            "apps_permissions": {},
            "ai_settings": {}
        }
        
        # Créer l'interface
        self._show_language_screen()
        
    def _setup_mobile_window(self):
        """Configure la fenêtre MOBILE"""
        self.root.title("EXOCORTEX")
        self.root.geometry("360x640")  # Taille mobile standard
        self.root.configure(fg_color="#000000")
        self.root.resizable(False, False)  # Non redimensionnable
        
        # Centrer
        self.root.update_idletasks()
        width = 360
        height = 640
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def _clear_screen(self):
        """Nettoie l'écran"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def _show_language_screen(self):
        """Écran 1: Sélection de la langue"""
        self._clear_screen()
        
        # Frame principal
        frame = ctk.CTkFrame(self.root, fg_color="#000000", corner_radius=0)
        frame.pack(fill="both", expand=True, padx=20, pady=40)
        
        # Logo
        ctk.CTkLabel(
            frame,
            text="EXOCORTEX",
            font=("Helvetica", 28, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=(0, 30))
        
        # Titre dynamique selon langue
        titles = {
            "fr": "Sélectionnez votre langue",
            "en": "Select your language",
            "de": "Wählen Sie Ihre Sprache",
            "es": "Seleccione su idioma",
            "it": "Seleziona la tua lingua"
        }
        
        current_title = titles.get(self.config["language"], titles["fr"])
        ctk.CTkLabel(
            frame,
            text=current_title,
            font=("Helvetica", 16),
            text_color="#888888"
        ).pack(pady=(0, 30))
        
        # Liste des langues
        languages = [
            ("FR", "Français", "fr"),
            ("GB", "English", "en"), 
            ("DE", "Deutsch", "de"),
            ("ES", "Español", "es"),
            ("IT", "Italiano", "it"),
            ("CN", "中文", "zh"),
            ("JP", "日本語", "ja")
        ]
        
        for code, name, lang_code in languages:
            btn = ctk.CTkButton(
                frame,
                text=f"{code}  {name}",
                font=("Helvetica", 14),
                height=45,
                fg_color="#111111",
                hover_color="#222222",
                text_color="#FFFFFF",
                border_color="#333333",
                border_width=1,
                command=lambda lc=lang_code, n=name: self._select_language(lc, n)
            )
            btn.pack(fill="x", pady=4)
            
        # Barre de progression
        ctk.CTkLabel(
            frame,
            text="Étape 1/3",
            font=("Helvetica", 12),
            text_color="#666666"
        ).pack(side="bottom", pady=20)
        
    def _select_language(self, lang_code, lang_name):
        """Sélectionne une langue"""
        print(f"🌐 Langue sélectionnée: {lang_name} ({lang_code})")
        self.config["language"] = lang_code
        
        # IMMÉDIATEMENT passer à l'écran suivant
        self._show_ai_config_screen()
        
    def _show_ai_config_screen(self):
        """Écran 2: Configuration IA"""
        self._clear_screen()
        
        # Traductions
        translations = {
            "fr": {
                "title": "Configurez votre agent IA",
                "personality": "Personnalité",
                "voice": "Voix",
                "detail": "Niveau de détail",
                "continue": "Continuer"
            },
            "en": {
                "title": "Configure your AI agent",
                "personality": "Personality", 
                "voice": "Voice",
                "detail": "Detail level",
                "continue": "Continue"
            },
            "de": {
                "title": "Konfigurieren Sie Ihren KI-Agenten",
                "personality": "Persönlichkeit",
                "voice": "Stimme",
                "detail": "Detaillierungsgrad", 
                "continue": "Weiter"
            }
        }
        
        trans = translations.get(self.config["language"], translations["fr"])
        
        # Frame principal
        frame = ctk.CTkFrame(self.root, fg_color="#000000", corner_radius=0)
        frame.pack(fill="both", expand=True, padx=20, pady=40)
        
        # Logo
        ctk.CTkLabel(
            frame,
            text="EXOCORTEX",
            font=("Helvetica", 28, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=(0, 30))
        
        # Titre
        ctk.CTkLabel(
            frame,
            text=trans["title"],
            font=("Helvetica", 18),
            text_color="#FFFFFF"
        ).pack(pady=(0, 40))
        
        # Options de configuration
        options = [
            (trans["personality"], ["Professionnel", "Amical", "Strict", "Créatif"]),
            (trans["voice"], ["Masculine", "Féminine", "Neutre"]),
            (trans["detail"], ["Minimal", "Standard", "Détaillé"])
        ]
        
        self.ai_settings = {}
        
        for label, choices in options:
            option_frame = ctk.CTkFrame(frame, fg_color="transparent")
            option_frame.pack(fill="x", pady=10)
            
            ctk.CTkLabel(
                option_frame,
                text=label,
                font=("Helvetica", 14),
                text_color="#888888",
                width=100
            ).pack(side="left")
            
            combo = ctk.CTkComboBox(
                option_frame,
                values=choices,
                font=("Helvetica", 14),
                fg_color="#111111",
                border_color="#333333",
                button_color="#00FF00",
                width=150
            )
            combo.set(choices[0])
            combo.pack(side="right")
            self.ai_settings[label] = combo
            
        # Espacement
        ctk.CTkLabel(frame, text="", height=30).pack()
        
        # Bouton Continuer
        ctk.CTkButton(
            frame,
            text=trans["continue"] + " →",
            font=("Helvetica", 16, "bold"),
            height=50,
            fg_color="#00FF00",
            hover_color="#00CC00",
            text_color="#000000",
            command=self._show_apps_screen
        ).pack(fill="x", pady=10)
        
        # Barre de progression
        ctk.CTkLabel(
            frame,
            text="Étape 2/3",
            font=("Helvetica", 12),
            text_color="#666666"
        ).pack(side="bottom", pady=20)
        
        # Bouton Retour
        ctk.CTkButton(
            frame,
            text="← Retour",
            font=("Helvetica", 12),
            height=35,
            fg_color="transparent",
            hover_color="#111111",
            text_color="#666666",
            command=self._show_language_screen
        ).pack(side="bottom", pady=10)
        
    def _show_apps_screen(self):
        """Écran 3: Applications RÉELLES"""
        self._clear_screen()
        
        # Traductions
        translations = {
            "fr": {
                "title": "Donnez accès à vos apps",
                "desc": "Activez les applications avec lesquelles\nEXOCORTEX peut interagir.",
                "note": "Toutes les apps sont désactivées par défaut.",
                "rescan": "Relancer la recherche",
                "finish": "Terminer"
            },
            "en": {
                "title": "Give access to your apps",
                "desc": "Activate the applications with which\nEXOCORTEX can interact.",
                "note": "All apps are disabled by default.",
                "rescan": "Rescan applications",
                "finish": "Finish"
            }
        }
        
        trans = translations.get(self.config["language"], translations["fr"])
        
        # Frame principal avec scroll
        main_frame = ctk.CTkScrollableFrame(
            self.root, 
            fg_color="#000000",
            corner_radius=0,
            height=640
        )
        main_frame.pack(fill="both", expand=True)
        
        # Padding
        content_frame = ctk.CTkFrame(main_frame, fg_color="#000000", corner_radius=0)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Logo
        ctk.CTkLabel(
            content_frame,
            text="EXOCORTEX",
            font=("Helvetica", 28, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=(0, 20))
        
        # Titre
        ctk.CTkLabel(
            content_frame,
            text=trans["title"],
            font=("Helvetica", 20, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=(0, 10))
        
        # Description
        ctk.CTkLabel(
            content_frame,
            text=trans["desc"],
            font=("Helvetica", 13),
            text_color="#888888",
            justify="center"
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            content_frame,
            text=trans["note"],
            font=("Helvetica", 11),
            text_color="#666666"
        ).pack(pady=(0, 30))
        
        # Scanner les applications RÉELLES
        apps = self._scan_real_apps()
        
        self.app_vars = {}
        
        # Afficher les applications
        for app_name, app_path, default_enabled in apps:
            app_frame = ctk.CTkFrame(content_frame, fg_color="#111111", height=55)
            app_frame.pack(fill="x", pady=3)
            
            # Nom de l'app
            ctk.CTkLabel(
                app_frame,
                text=app_name,
                font=("Helvetica", 14),
                text_color="#FFFFFF",
                anchor="w"
            ).pack(side="left", padx=15, fill="x", expand=True)
            
            # Checkbox
            var = tk.BooleanVar(value=default_enabled)
            self.app_vars[app_name] = {"var": var, "path": app_path}
            
            checkbox = ctk.CTkCheckBox(
                app_frame,
                text="",
                variable=var,
                width=28,
                height=28,
                fg_color="#00FF00",
                hover_color="#00CC00",
                border_color="#333333"
            )
            checkbox.pack(side="right", padx=15)
            
        # Bouton Rescan
        ctk.CTkButton(
            content_frame,
            text=trans["rescan"],
            font=("Helvetica", 14),
            height=40,
            fg_color="transparent",
            hover_color="#111111",
            text_color="#00FF00",
            border_color="#00FF00",
            border_width=1,
            command=self._rescan_apps
        ).pack(fill="x", pady=(30, 10))
        
        # Bouton Terminer
        ctk.CTkButton(
            content_frame,
            text=trans["finish"] + " →",
            font=("Helvetica", 16, "bold"),
            height=50,
            fg_color="#00FF00",
            hover_color="#00CC00",
            text_color="#000000",
            command=self._finish_configuration
        ).pack(fill="x", pady=10)
        
        # Barre de progression
        ctk.CTkLabel(
            content_frame,
            text="Étape 3/3",
            font=("Helvetica", 12),
            text_color="#666666"
        ).pack(side="bottom", pady=20)
        
        # Bouton Retour
        ctk.CTkButton(
            content_frame,
            text="← Retour",
            font=("Helvetica", 12),
            height=35,
            fg_color="transparent",
            hover_color="#111111",
            text_color="#666666",
            command=self._show_ai_config_screen
        ).pack(side="bottom", pady=10)
        
    def _scan_real_apps(self):
        """Scanner les applications RÉELLES du système"""
        apps = []
        
        # Applications système Windows (exemples)
        windows_apps = [
            ("Explorateur de fichiers", "explorer.exe", True),
            ("Calculatrice", "calc.exe", True),
            ("Bloc-notes", "notepad.exe", True),
            ("Paint", "mspaint.exe", False),
            ("Command Prompt", "cmd.exe", False),
            ("Microsoft Edge", "msedge.exe", True),
            ("Windows Media Player", "wmplayer.exe", False),
            ("Regedit", "regedit.exe", False),
            ("Task Manager", "taskmgr.exe", False),
            ("WordPad", "wordpad.exe", False)
        ]
        
        # Vérifier quelles applications existent vraiment
        import os
        system_paths = [
            os.environ.get("SystemRoot", "C:\\Windows"),
            os.environ.get("ProgramFiles", "C:\\Program Files"),
            os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
        ]
        
        for app_name, exe_name, default_enabled in windows_apps:
            found = False
            for path in system_paths:
                exe_path = os.path.join(path, exe_name)
                if os.path.exists(exe_path):
                    apps.append((app_name, exe_path, default_enabled))
                    found = True
                    break
            
            # Si pas trouvé, chercher dans le PATH
            if not found:
                import shutil
                full_path = shutil.which(exe_name)
                if full_path:
                    apps.append((app_name, full_path, default_enabled))
                else:
                    # Ajouter quand même (pour démo)
                    apps.append((app_name, exe_name, default_enabled))
                    
        # Applications courantes
        common_apps = [
            ("Google Chrome", "chrome.exe", True),
            ("Mozilla Firefox", "firefox.exe", True),
            ("Discord", "Discord.exe", False),
            ("Spotify", "Spotify.exe", True),
            ("Steam", "steam.exe", False),
            ("VLC", "vlc.exe", True),
            ("7-Zip", "7zFM.exe", False),
            ("Adobe Reader", "AcroRd32.exe", False)
        ]
        
        for app_name, exe_name, default_enabled in common_apps:
            import shutil
            full_path = shutil.which(exe_name)
            if full_path:
                apps.append((app_name, full_path, default_enabled))
            else:
                # Chercher dans Program Files
                for path in [os.environ.get("ProgramFiles", "C:\\Program Files"), 
                           os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")]:
                    for root, dirs, files in os.walk(path):
                        if exe_name in files:
                            exe_path = os.path.join(root, exe_name)
                            apps.append((app_name, exe_path, default_enabled))
                            break
        
        return apps[:15]  # Limiter à 15 apps max
        
    def _rescan_apps(self):
        """Rescanner les applications"""
        print("🔄 Rescan des applications...")
        self._show_apps_screen()  # Recharger l'écran
        
    def _finish_configuration(self):
        """Termine la configuration et lance Zodiac OS"""
        # Sauvegarder les permissions
        self.config["apps_permissions"] = {
            app_name: data["var"].get() 
            for app_name, data in self.app_vars.items()
        }
        
        # Sauvegarder les paramètres IA
        self.config["ai_settings"] = {
            "personality": self.ai_settings.get("Personnalité", "").get() if self.ai_settings else "Professionnel",
            "voice": self.ai_settings.get("Voix", "").get() if self.ai_settings else "Masculine",
            "detail": self.ai_settings.get("Niveau de détail", "").get() if self.ai_settings else "Standard"
        }
        
        # Sauvegarder la config
        self._save_config()
        
        # Message de succès
        messagebox.showinfo(
            "EXOCORTEX",
            f"✅ Configuration terminée!\n\n"
            f"🌐 Langue: {self.config['language']}\n"
            f"🤖 Agent IA configuré\n"
            f"📱 {sum(self.config['apps_permissions'].values())} apps activées\n\n"
            f"Lancement de Zodiac OS..."
        )
        
        # Fermer EXOCORTEX
        self.root.destroy()
        
        # Lancer ZODIAC OS
        self._launch_zodiac_os()
        
    def _save_config(self):
        """Sauvegarde la configuration"""
        try:
            config_dir = "data"
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
                
            config_path = os.path.join(config_dir, "exocortex_config.json")
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
                
            print(f"💾 Configuration sauvegardée: {config_path}")
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde: {e}")
            
    def _launch_zodiac_os(self):
        """Lance Zodiac OS avec la configuration"""
        print("🚀 Lancement de Zodiac OS...")
        
        try:
            # Charger la configuration
            config_path = "data/exocortex_config.json"
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                print(f"📋 Config chargée: {config}")
            
            # Importer et lancer Zodiac OS
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            
            from ui.main_window import MainWindow
            from core.assistant import ZodiacAssistant
            from core.voice_engine import VoiceEngine
            
            # Créer l'assistant avec configuration
            assistant = ZodiacAssistant()
            voice_engine = VoiceEngine()
            
            # Lancer en mode MOBILE
            app = MainWindow(
                assistant=assistant,
                voice_engine=voice_engine,
                mobile_mode=True  # FORCER mobile
            )
            app.run()
            
        except ImportError as e:
            print(f"❌ Erreur d'import: {e}")
            
            # Lancer l'ancien main.py de Zodiac
            import subprocess
            try:
                subprocess.run([sys.executable, "old_main.py"], check=True)
            except:
                print("💡 Lancez Zodiac OS manuellement")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
            import traceback
            traceback.print_exc()
            
    def run(self):
        """Lance l'application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ExocortexApp()
    app.run()