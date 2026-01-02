# main.py - EXOCORTEX VERSION INTELLIGENTE
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os
import sys
import json
import threading
import time
import winreg
import psutil
import shutil
from pathlib import Path
import tempfile

class ExocortexApp:
    """EXOCORTEX - Agent intelligent qui scanne puis nettoie"""
    
    def __init__(self):
        # Configuration
        ctk.set_appearance_mode("dark")
        
        # Fenêtre principale
        self.root = ctk.CTk()
        self._setup_window()
        
        # Configuration utilisateur
        self.config = {
            "language": "fr",
            "apps_permissions": {},
            "system_access": True,
            "privacy_mode": False,
            "scan_complete": False
        }
        
        # Scanner initial COMPLET
        self._perform_full_scan()
        
        # Démarrer avec l'écran de langue
        self._show_language_screen()
        
    def _setup_window(self):
        """Configure la fenêtre mobile"""
        self.root.title("EXOCORTEX")
        self.root.geometry("360x640")
        self.root.configure(fg_color="#000000")
        self.root.resizable(False, False)
        
        # Centrer
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 180
        y = (self.root.winfo_screenheight() // 2) - 320
        self.root.geometry(f'360x640+{x}+{y}')
        
    def _perform_full_scan(self):
        """Scan COMPLET du système avant de montrer l'interface"""
        print("🔍 Scan complet du système en cours...")
        
        # Créer un cache temporaire pour le scan
        self.scan_cache = {
            "all_apps": [],
            "system_apps": [],
            "user_apps": [],
            "running_apps": [],
            "installed_apps": []
        }
        
        # Scanner dans un thread
        scan_thread = threading.Thread(target=self._full_system_scan, daemon=True)
        scan_thread.start()
        
    def _full_system_scan(self):
        """Scan exhaustif de TOUT le système"""
        try:
            print("📁 Scanning Windows Registry...")
            registry_apps = self._deep_scan_registry()
            self.scan_cache["installed_apps"] = registry_apps
            
            print("📁 Scanning Program Files...")
            program_apps = self._deep_scan_program_files()
            self.scan_cache["user_apps"] = program_apps
            
            print("⚙️ Scanning System Apps...")
            system_apps = self._deep_scan_system_apps()
            self.scan_cache["system_apps"] = system_apps
            
            print("🔄 Scanning Running Processes...")
            running_apps = self._deep_scan_running_processes()
            self.scan_cache["running_apps"] = running_apps
            
            # Combiner TOUT
            all_apps = []
            seen_paths = set()
            
            for app_list in [registry_apps, program_apps, system_apps, running_apps]:
                for app in app_list:
                    if app["path"] not in seen_paths:
                        all_apps.append(app)
                        seen_paths.add(app["path"])
            
            self.scan_cache["all_apps"] = all_apps
            
            print(f"✅ Scan complet terminé: {len(all_apps)} applications trouvées")
            self.config["scan_complete"] = True
            
        except Exception as e:
            print(f"❌ Erreur scan: {e}")
            
    def _deep_scan_registry(self):
        """Scan PROFOND du registre Windows"""
        apps = []
        try:
            # Toutes les clés possibles du registre
            reg_keys = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Classes\Installer\Products"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Classes\Installer\Features"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"),
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths")
            ]
            
            for hive, reg_path in reg_keys:
                try:
                    key = winreg.OpenKey(hive, reg_path)
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            subkey = winreg.OpenKey(key, subkey_name)
                            
                            # Essayer différents noms de valeur
                            name = None
                            for name_key in ["DisplayName", "ProductName", "InstallLocation"]:
                                try:
                                    name_val = winreg.QueryValueEx(subkey, name_key)[0]
                                    if name_val:
                                        name = str(name_val)
                                        break
                                except:
                                    continue
                            
                            # Chercher l'exécutable
                            exe_path = None
                            for exe_key in ["DisplayIcon", "InstallLocation", "UninstallString"]:
                                try:
                                    exe_val = winreg.QueryValueEx(subkey, exe_key)[0]
                                    if exe_val and (".exe" in str(exe_val).lower() or ".lnk" in str(exe_val).lower()):
                                        exe_path = str(exe_val).replace('"', '').split(',')[0]
                                        if not os.path.exists(exe_path):
                                            # Essayer de trouver l'exe dans le répertoire
                                            dir_path = os.path.dirname(exe_path) if os.path.dirname(exe_path) else exe_path
                                            if os.path.exists(dir_path):
                                                for file in os.listdir(dir_path):
                                                    if file.lower().endswith('.exe'):
                                                        exe_path = os.path.join(dir_path, file)
                                                        break
                                        break
                                except:
                                    continue
                            
                            if name and exe_path and os.path.exists(exe_path):
                                apps.append({
                                    "name": name[:40],
                                    "path": exe_path,
                                    "type": "installée",
                                    "default_enabled": True
                                })
                            
                            winreg.CloseKey(subkey)
                        except:
                            continue
                    winreg.CloseKey(key)
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Erreur registre: {e}")
            
        return apps
        
    def _deep_scan_program_files(self):
        """Scan PROFOND de tous les dossiers"""
        apps = []
        try:
            # Tous les dossiers à scanner
            scan_dirs = [
                os.environ.get('ProgramFiles', 'C:\\Program Files'),
                os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)'),
                os.path.join(os.environ['USERPROFILE'], 'Desktop'),
                os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs'),
                os.path.join(os.environ['LOCALAPPDATA']),
                os.path.join(os.environ['LOCALAPPDATA'], 'Programs'),
                os.path.join(os.environ['APPDATA']),
                "C:\\",
                "D:\\",
                "E:\\"
            ]
            
            exe_extensions = ['.exe', '.lnk', '.bat', '.cmd']
            
            for scan_dir in scan_dirs:
                if os.path.exists(scan_dir):
                    print(f"  Scanning: {scan_dir}")
                    try:
                        for root, dirs, files in os.walk(scan_dir, topdown=True):
                            # Éviter certains dossiers système
                            dirs[:] = [d for d in dirs if not any(
                                ignore in d.lower() for ignore in [
                                    'windows', 'system32', 'syswow64', 'temp', 
                                    'cache', 'logs', 'backup', '$'
                                ]
                            )]
                            
                            for file in files:
                                if any(file.lower().endswith(ext) for ext in exe_extensions):
                                    full_path = os.path.join(root, file)
                                    
                                    # Pour les .lnk, résoudre le chemin cible
                                    if file.lower().endswith('.lnk'):
                                        try:
                                            import win32com.client
                                            shell = win32com.client.Dispatch("WScript.Shell")
                                            shortcut = shell.CreateShortCut(full_path)
                                            target_path = shortcut.Targetpath
                                            if target_path and os.path.exists(target_path):
                                                full_path = target_path
                                        except:
                                            continue
                                    
                                    if os.path.exists(full_path):
                                        app_name = os.path.splitext(os.path.basename(file))[0]
                                        apps.append({
                                            "name": app_name[:30],
                                            "path": full_path,
                                            "type": "fichier",
                                            "default_enabled": False
                                        })
                    except:
                        continue
                        
        except Exception as e:
            print(f"⚠️ Erreur scan dossiers: {e}")
            
        return apps[:100]  # Limiter à 100 max
        
    def _deep_scan_system_apps(self):
        """Scan des applications système"""
        apps = []
        windows_dir = os.environ.get('SystemRoot', 'C:\\Windows')
        
        system_apps = [
            ("Explorateur", "explorer.exe"),
            ("Calculatrice", "calc.exe"),
            ("Bloc-notes", "notepad.exe"),
            ("Paint", "mspaint.exe"),
            ("CMD", "cmd.exe"),
            ("Regedit", "regedit.exe"),
            ("Task Manager", "taskmgr.exe"),
            ("WordPad", "wordpad.exe"),
            ("Magnifier", "magnify.exe"),
            ("Narrator", "narrator.exe"),
            ("Windows Media Player", "wmplayer.exe"),
            ("Sound Recorder", "soundrecorder.exe"),
            ("Snipping Tool", "snippingtool.exe"),
            ("Sticky Notes", "stikynot.exe"),
            ("Character Map", "charmap.exe")
        ]
        
        for name, exe in system_apps:
            exe_path = os.path.join(windows_dir, "System32", exe)
            if os.path.exists(exe_path):
                apps.append({
                    "name": name,
                    "path": exe_path,
                    "type": "système",
                    "default_enabled": True
                })
                
        return apps
        
    def _deep_scan_running_processes(self):
        """Scan des processus en cours"""
        apps = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
                try:
                    if proc.info['exe'] and proc.info['name']:
                        apps.append({
                            "name": proc.info['name'].replace('.exe', ''),
                            "path": proc.info['exe'],
                            "type": "en cours",
                            "default_enabled": True
                        })
                except:
                    continue
        except:
            pass
            
        return apps[:50]
        
    def _show_language_screen(self):
        """Écran 1: Sélection de la langue"""
        self._clear_screen()
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.root, fg_color="#000000")
        main_frame.pack(fill="both", expand=True, padx=20, pady=30)
        
        # Logo EXOCORTEX
        ctk.CTkLabel(
            main_frame,
            text="EXOCORTEX",
            font=("Segoe UI", 32, "bold"),
            text_color="#00FF00"
        ).pack(pady=(0, 20))
        
        # Titre
        ctk.CTkLabel(
            main_frame,
            text="Sélectionnez votre langue",
            font=("Segoe UI", 18),
            text_color="#FFFFFF"
        ).pack(pady=(0, 30))
        
        # Liste des langues
        languages = [
            ("🇫🇷 Français", "fr"),
            ("🇬🇧 English", "en"),
            ("🇩🇪 Deutsch", "de"),
            ("🇪🇸 Español", "es"),
            ("🇮🇹 Italiano", "it"),
            ("🇵🇹 Português", "pt"),
            ("🇨🇳 中文", "zh"),
            ("🇯🇵 日本語", "ja")
        ]
        
        for text, code in languages:
            btn = ctk.CTkButton(
                main_frame,
                text=text,
                font=("Segoe UI", 15),
                height=45,
                fg_color="#111111",
                hover_color="#222222",
                text_color="#FFFFFF",
                border_color="#333333",
                border_width=1,
                command=lambda c=code: self._select_language(c)
            )
            btn.pack(fill="x", pady=4)
            
        # Bouton Continuer
        self.continue_btn = ctk.CTkButton(
            main_frame,
            text="Continuer →",
            font=("Segoe UI", 16, "bold"),
            height=50,
            fg_color="#00FF00",
            hover_color="#00CC00",
            text_color="#000000",
            command=self._show_apps_screen
        )
        self.continue_btn.pack(fill="x", pady=(20, 10))
        
        # Barre de progression
        self._create_progress_bar(main_frame, 1)
        
    def _select_language(self, lang_code):
        """Sélectionne une langue"""
        print(f"🌐 Langue sélectionnée: {lang_code}")
        self.config["language"] = lang_code
        
    def _show_apps_screen(self):
        """Écran 2: Permissions d'applications"""
        self._clear_screen()
        
        # Attendre que le scan soit complet si nécessaire
        if not self.config["scan_complete"]:
            self._show_loading_screen()
            return
            
        # Frame principal avec scroll
        main_frame = ctk.CTkScrollableFrame(
            self.root,
            fg_color="#000000",
            scrollbar_button_color="#00FF00"
        )
        main_frame.pack(fill="both", expand=True)
        
        # Contenu
        content_frame = ctk.CTkFrame(main_frame, fg_color="#000000")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Logo
        ctk.CTkLabel(
            content_frame,
            text="EXOCORTEX",
            font=("Segoe UI", 28, "bold"),
            text_color="#00FF00"
        ).pack(pady=(0, 15))
        
        # Titre
        ctk.CTkLabel(
            content_frame,
            text="Donnez accès à vos apps",
            font=("Segoe UI", 20, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=(0, 10))
        
        # Description
        ctk.CTkLabel(
            content_frame,
            text="Activez les applications avec lesquelles\nEXOCORTEX peut interagir.",
            font=("Segoe UI", 13),
            text_color="#888888",
            justify="center"
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            content_frame,
            text="Toutes les apps sont désactivées par défaut.",
            font=("Segoe UI", 11),
            text_color="#666666"
        ).pack(pady=(0, 20))
        
        # TOGGLE - Accès complet au PC
        access_frame = ctk.CTkFrame(content_frame, fg_color="#111111", height=50)
        access_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            access_frame,
            text="🔓 Accès complet au système",
            font=("Segoe UI", 15, "bold"),
            text_color="#FFFFFF"
        ).pack(side="left", padx=15)
        
        self.full_access_switch = ctk.CTkSwitch(
            access_frame,
            text="",
            width=50,
            height=30,
            switch_width=50,
            switch_height=25,
            fg_color="#333333",
            progress_color="#00FF00",
            button_color="#FFFFFF",
            button_hover_color="#CCCCCC",
            command=self._toggle_full_access
        )
        self.full_access_switch.pack(side="right", padx=15)
        self.full_access_switch.select()
        
        # Liste des applications (du scan complet)
        self.apps_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.apps_container.pack(fill="x", pady=10)
        
        # Variables pour les toggles
        self.app_toggles = {}
        
        # Afficher les applications du scan
        all_apps = self.scan_cache["all_apps"]
        print(f"📊 Affichage de {len(all_apps)} applications")
        
        for app in all_apps:
            app_frame = ctk.CTkFrame(self.apps_container, fg_color="#111111", height=50)
            app_frame.pack(fill="x", pady=3)
            
            # Nom et type
            info_frame = ctk.CTkFrame(app_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=15)
            
            # Nom tronqué si trop long
            display_name = app["name"]
            if len(display_name) > 25:
                display_name = display_name[:22] + "..."
                
            ctk.CTkLabel(
                info_frame,
                text=display_name,
                font=("Segoe UI", 13),
                text_color="#FFFFFF",
                anchor="w"
            ).pack(anchor="w")
            
            type_color = {
                "système": "#00FF00",
                "installée": "#FFAA00", 
                "en cours": "#AA55FF",
                "fichier": "#888888"
            }.get(app["type"], "#888888")
            
            ctk.CTkLabel(
                info_frame,
                text=app["type"],
                font=("Segoe UI", 10),
                text_color=type_color,
                anchor="w"
            ).pack(anchor="w")
            
            # TOGGLE ON/OFF
            toggle_var = tk.BooleanVar(value=app["default_enabled"])
            self.app_toggles[app["path"]] = {
                "var": toggle_var,
                "name": app["name"],
                "type": app["type"]
            }
            
            toggle = ctk.CTkSwitch(
                app_frame,
                text="",
                variable=toggle_var,
                width=45,
                height=25,
                switch_width=45,
                switch_height=25,
                fg_color="#333333",
                progress_color="#00FF00",
                button_color="#FFFFFF",
                button_hover_color="#CCCCCC"
            )
            toggle.pack(side="right", padx=15)
            
        # Bouton Nouveau scan
        ctk.CTkButton(
            content_frame,
            text="🔄 Nouveau scan complet",
            font=("Segoe UI", 14),
            height=40,
            fg_color="transparent",
            hover_color="#111111",
            text_color="#00FF00",
            border_color="#00FF00",
            border_width=1,
            command=self._rescan_apps
        ).pack(fill="x", pady=(20, 10))
        
        # Bouton Terminer
        self.finish_btn = ctk.CTkButton(
            content_frame,
            text="🚀 Lancer EXOCORTEX",
            font=("Segoe UI", 16, "bold"),
            height=50,
            fg_color="#00FF00",
            hover_color="#00CC00",
            text_color="#000000",
            command=self._clean_and_launch
        )
        self.finish_btn.pack(fill="x", pady=(10, 5))
        
        # Barre de progression
        self._create_progress_bar(content_frame, 2)
        
    def _show_loading_screen(self):
        """Écran de chargement pendant le scan"""
        self._clear_screen()
        
        frame = ctk.CTkFrame(self.root, fg_color="#000000")
        frame.pack(fill="both", expand=True)
        
        # Logo
        ctk.CTkLabel(
            frame,
            text="EXOCORTEX",
            font=("Segoe UI", 32, "bold"),
            text_color="#00FF00"
        ).pack(pady=(100, 30))
        
        # Message
        ctk.CTkLabel(
            frame,
            text="🔍 Scan complet du système",
            font=("Segoe UI", 20),
            text_color="#FFFFFF"
        ).pack(pady=(0, 20))
        
        # Détails
        ctk.CTkLabel(
            frame,
            text="Recherche de toutes les applications...",
            font=("Segoe UI", 14),
            text_color="#888888"
        ).pack(pady=(0, 30))
        
        # Barre de progression
        progress = ctk.CTkProgressBar(
            frame,
            width=300,
            height=8,
            progress_color="#00FF00",
            fg_color="#222222",
            mode="indeterminate"
        )
        progress.pack(pady=20)
        progress.start()
        
        # Vérifier périodiquement si le scan est terminé
        self._check_scan_complete()
        
    def _check_scan_complete(self):
        """Vérifie si le scan est terminé"""
        if self.config["scan_complete"]:
            self._show_apps_screen()
        else:
            self.root.after(1000, self._check_scan_complete)
            
    def _toggle_full_access(self):
        """Active/désactive l'accès complet"""
        self.config["system_access"] = self.full_access_switch.get()
        
    def _rescan_apps(self):
        """Relance un scan complet"""
        self.config["scan_complete"] = False
        self.scan_cache = {"all_apps": []}
        threading.Thread(target=self._full_system_scan, daemon=True).start()
        self._show_loading_screen()
        
    def _clean_and_launch(self):
        """Nettoie et garde SEULEMENT les apps activées"""
        print("🧹 Nettoyage des applications...")
        
        # Récupérer UNIQUEMENT les apps activées
        enabled_apps = {}
        for app_path, app_data in self.app_toggles.items():
            if app_data["var"].get():  # Si le toggle est activé
                enabled_apps[app_data["name"]] = app_path
                print(f"  ✅ Garder: {app_data['name']}")
            else:
                print(f"  🗑️ Supprimer: {app_data['name']}")
        
        # Mettre à jour la configuration
        self.config["apps_permissions"] = enabled_apps
        
        # Sauvegarder la configuration
        self._save_config()
        
        # Supprimer le cache de scan (garder seulement les apps activées)
        self.scan_cache["all_apps"] = [
            {"name": name, "path": path, "type": "activée", "default_enabled": True}
            for name, path in enabled_apps.items()
        ]
        
        print(f"✅ {len(enabled_apps)} applications gardées")
        
        # Lancer l'interface principale
        self._launch_main_interface()
        
    def _save_config(self):
        """Sauvegarde la configuration"""
        try:
            config_dir = "data"
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
                
            config_path = os.path.join(config_dir, "exocortex_clean.json")
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
                
            print(f"💾 Configuration propre sauvegardée: {config_path}")
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde: {e}")
            
    def _launch_main_interface(self):
        """Lance l'interface principale"""
        # Fermer la fenêtre de configuration
        self.root.destroy()
        
        # Lancer l'interface principale
        main_app = ExocortexMainInterface(self.config, self.scan_cache)
        main_app.run()
        
    def _create_progress_bar(self, parent, step):
        """Crée une barre de progression"""
        prog_frame = ctk.CTkFrame(parent, fg_color="transparent")
        prog_frame.pack(side="bottom", fill="x", pady=10)
        
        # Texte
        ctk.CTkLabel(
            prog_frame,
            text=f"Étape {step}/2 • Scan: {len(self.scan_cache.get('all_apps', []))} apps",
            font=("Segoe UI", 12),
            text_color="#666666"
        ).pack()
        
    def _clear_screen(self):
        """Nettoie l'écran"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def run(self):
        """Lance l'application"""
        self.root.mainloop()


class ExocortexMainInterface:
    """Interface principale avec chat, apps et monitoring"""
    
    def __init__(self, config, scan_cache):
        self.config = config
        self.scan_cache = scan_cache
        
        # Fenêtre principale
        self.root = ctk.CTk()
        self._setup_window()
        
        # Créer l'interface
        self._create_interface()
        
    def _setup_window(self):
        """Configure la fenêtre"""
        self.root.title("EXOCORTEX")
        self.root.geometry("360x640")
        self.root.configure(fg_color="#000000")
        self.root.resizable(False, False)
        
        # Centrer
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 180
        y = (self.root.winfo_screenheight() // 2) - 320
        self.root.geometry(f'360x640+{x}+{y}')
        
    def _create_interface(self):
        """Crée l'interface principale"""
        # Header
        header = ctk.CTkFrame(self.root, fg_color="#111111", height=60)
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="🤖 EXOCORTEX",
            font=("Segoe UI", 22, "bold"),
            text_color="#00FF00"
        ).pack(side="left", padx=20, pady=15)
        
        # Bouton rafraîchir
        ctk.CTkButton(
            header,
            text="🔄",
            width=40,
            height=40,
            fg_color="transparent",
            hover_color="#222222",
            command=self._refresh_apps
        ).pack(side="right", padx=10, pady=10)
        
        # Onglets
        self.tabview = ctk.CTkTabview(
            self.root,
            fg_color="#000000",
            segmented_button_fg_color="#111111",
            segmented_button_selected_color="#00FF00",
            segmented_button_selected_hover_color="#00CC00",
            segmented_button_unselected_color="#222222",
            segmented_button_unselected_hover_color="#333333",
            height=580
        )
        self.tabview.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Créer les onglets
        self.tabview.add("💬 Chat")
        self.tabview.add("📁 Apps")
        self.tabview.add("📊 Monitoring")
        
        # Configurer les onglets
        self._setup_chat_tab()
        self._setup_apps_tab()
        self._setup_monitoring_tab()
        
    def _setup_chat_tab(self):
        """Configure l'onglet Chat"""
        frame = self.tabview.tab("💬 Chat")
        
        # Zone de messages avec scroll
        self.chat_frame = ctk.CTkScrollableFrame(
            frame,
            fg_color="#000000",
            height=400
        )
        self.chat_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Message de bienvenue
        welcome = ctk.CTkFrame(
            self.chat_frame,
            fg_color="#111111",
            corner_radius=10
        )
        welcome.pack(fill="x", pady=10)
        
        welcome_text = "🎯 **EXOCORTEX ACTIVÉ**\n\n"
        welcome_text += f"• Langue: {self.config['language']}\n"
        welcome_text += f"• Apps activées: {len(self.config['apps_permissions'])}\n"
        welcome_text += f"• Accès système: {'✅' if self.config['system_access'] else '❌'}\n\n"
        welcome_text += "🎤 Dites 'Hey EXOCORTEX' ou tapez un message"
        
        ctk.CTkLabel(
            welcome,
            text=welcome_text,
            font=("Segoe UI", 13),
            text_color="#00FF00",
            justify="left"
        ).pack(padx=15, pady=15)
        
        # Zone de saisie
        input_frame = ctk.CTkFrame(frame, fg_color="#111111", height=80)
        input_frame.pack(fill="x", side="bottom", padx=10, pady=10)
        
        # Microphone
        self.mic_btn = ctk.CTkButton(
            input_frame,
            text="🎤",
            width=50,
            height=50,
            font=("Segoe UI", 20),
            fg_color="#00FF00",
            hover_color="#00CC00",
            command=self._toggle_microphone
        )
        self.mic_btn.pack(side="left", padx=(10, 5))
        
        # Champ texte
        self.chat_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="Tapez votre message...",
            height=45,
            font=("Segoe UI", 14)
        )
        self.chat_input.pack(side="left", fill="x", expand=True, padx=5)
        self.chat_input.bind("<Return>", lambda e: self._send_message())
        
        # Bouton envoyer
        ctk.CTkButton(
            input_frame,
            text="➤",
            width=50,
            height=50,
            font=("Segoe UI", 18),
            fg_color="#00FF00",
            hover_color="#00CC00",
            command=self._send_message
        ).pack(side="right", padx=(5, 10))
        
    def _setup_apps_tab(self):
        """Configure l'onglet Apps"""
        frame = self.tabview.tab("📁 Apps")
        
        # Barre de recherche
        search_frame = ctk.CTkFrame(frame, fg_color="transparent", height=50)
        search_frame.pack(fill="x", padx=10, pady=10)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Rechercher une app...",
            height=40,
            font=("Segoe UI", 14)
        )
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self._filter_apps)
        
        # Bouton tri
        ctk.CTkButton(
            search_frame,
            text="🔽",
            width=40,
            height=40,
            fg_color="#222222",
            hover_color="#333333",
            command=self._sort_apps
        ).pack(side="right", padx=(5, 0))
        
        # Liste des applications
        self.apps_list_frame = ctk.CTkScrollableFrame(
            frame,
            fg_color="#000000",
            height=420
        )
        self.apps_list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Afficher les applications
        self._display_apps_list()
        
    def _setup_monitoring_tab(self):
        """Configure l'onglet Monitoring"""
        frame = self.tabview.tab("📊 Monitoring")
        
        # Titre
        ctk.CTkLabel(
            frame,
            text="📈 Surveillance système",
            font=("Segoe UI", 20, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=(10, 20))
        
        # Métriques en temps réel
        metrics_frame = ctk.CTkFrame(frame, fg_color="#111111", corner_radius=10)
        metrics_frame.pack(fill="x", padx=20, pady=10)
        
        self.metrics = {
            "CPU": ctk.CTkLabel(metrics_frame, text="⚡ CPU: --%", font=("Segoe UI", 14), text_color="#FF5555"),
            "RAM": ctk.CTkLabel(metrics_frame, text="💾 RAM: --%", font=("Segoe UI", 14), text_color="#55AAFF"),
            "DISK": ctk.CTkLabel(metrics_frame, text="💿 Disque: --%", font=("Segoe UI", 14), text_color="#55FF55"),
            "NETWORK": ctk.CTkLabel(metrics_frame, text="🌐 Réseau: -- Kb/s", font=("Segoe UI", 14), text_color="#FFAA55")
        }
        
        for metric in self.metrics.values():
            metric.pack(pady=5, padx=20, anchor="w")
            
        # Démarrer la surveillance
        self._start_monitoring()
        
        # Activités récentes
        ctk.CTkLabel(
            frame,
            text="📝 Activités EXOCORTEX",
            font=("Segoe UI", 16, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=(20, 10))
        
        self.activities_frame = ctk.CTkScrollableFrame(
            frame,
            fg_color="#111111",
            height=200
        )
        self.activities_frame.pack(fill="x", padx=20, pady=10)
        
        # Exemples d'activités
        activities = [
            ("🔍 Scan système", "Terminé - " + time.strftime("%H:%M")),
            ("📱 Apps activées", f"{len(self.config['apps_permissions'])} applications"),
            ("🌐 Langue", self.config['language']),
            ("🔒 Sécurité", "Mode surveillance activé"),
            ("💾 Données", "Configuration sauvegardée")
        ]
        
        for activity, detail in activities:
            act_frame = ctk.CTkFrame(self.activities_frame, fg_color="#222222", height=35)
            act_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(
                act_frame,
                text=activity,
                font=("Segoe UI", 12),
                text_color="#FFFFFF"
            ).pack(side="left", padx=10)
            
            ctk.CTkLabel(
                act_frame,
                text=detail,
                font=("Segoe UI", 11),
                text_color="#888888"
            ).pack(side="right", padx=10)
            
    def _display_apps_list(self):
        """Affiche la liste des applications"""
        # Nettoyer la liste
        for widget in self.apps_list_frame.winfo_children():
            widget.destroy()
            
        # Afficher chaque application
        apps = list(self.config["apps_permissions"].items())
        
        if not apps:
            ctk.CTkLabel(
                self.apps_list_frame,
                text="Aucune application activée.\nRetournez à la configuration.",
                font=("Segoe UI", 14),
                text_color="#888888",
                justify="center"
            ).pack(pady=50)
            return
            
        for app_name, app_path in apps:
            app_frame = ctk.CTkFrame(self.apps_list_frame, fg_color="#111111", height=55)
            app_frame.pack(fill="x", pady=2)
            
            # Nom
            display_name = app_name
            if len(display_name) > 25:
                display_name = display_name[:22] + "..."
                
            ctk.CTkLabel(
                app_frame,
                text=display_name,
                font=("Segoe UI", 13),
                text_color="#FFFFFF"
            ).pack(side="left", padx=15, pady=10)
            
            # Bouton lancer
            ctk.CTkButton(
                app_frame,
                text="▶",
                width=40,
                height=40,
                fg_color="#00FF00",
                hover_color="#00CC00",
                command=lambda p=app_path: self._launch_app(p)
            ).pack(side="right", padx=5, pady=7)
            
            # Bouton infos
            ctk.CTkButton(
                app_frame,
                text="ℹ️",
                width=30,
                height=30,
                fg_color="#333333",
                hover_color="#444444",
                command=lambda n=app_name, p=app_path: self._show_app_info(n, p)
            ).pack(side="right", padx=5, pady=12)
            
    def _filter_apps(self, event=None):
        """Filtre les applications selon la recherche"""
        search_text = self.search_entry.get().lower()
        
        # Pour l'instant, on ne filtre pas (implémentation basique)
        # Vous pouvez implémenter une logique de filtrage ici
        
    def _sort_apps(self):
        """Trie les applications"""
        # Implémentation basique - inverse l'ordre
        apps = list(self.config["apps_permissions"].items())
        apps.reverse()
        self.config["apps_permissions"] = dict(apps)
        self._display_apps_list()
        
    def _launch_app(self, app_path):
        """Lance une application"""
        try:
            os.startfile(app_path)
            self._add_activity(f"🚀 Lancement: {os.path.basename(app_path)}")
        except Exception as e:
            print(f"❌ Erreur lancement: {e}")
            
    def _show_app_info(self, app_name, app_path):
        """Affiche les infos d'une app"""
        try:
            size = os.path.getsize(app_path)
            mtime = time.ctime(os.path.getmtime(app_path))
            
            info = f"📱 {app_name}\n\n"
            info += f"📍 Chemin: {app_path}\n"
            info += f"📏 Taille: {self._format_size(size)}\n"
            info += f"🕐 Modifié: {mtime}\n"
            info += f"📁 Type: {self._get_file_type(app_path)}"
            
            messagebox.showinfo("Informations", info)
        except:
            messagebox.showinfo("Informations", f"📱 {app_name}\n\n📍 Chemin: {app_path}")
            
    def _format_size(self, size):
        """Formate la taille d'un fichier"""
        for unit in ['octets', 'Ko', 'Mo', 'Go']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} To"
        
    def _get_file_type(self, path):
        """Détermine le type de fichier"""
        if path.lower().endswith('.exe'):
            return "Application exécutable"
        elif path.lower().endswith('.lnk'):
            return "Raccourci"
        elif path.lower().endswith('.bat'):
            return "Script batch"
        elif path.lower().endswith('.msi'):
            return "Installateur Windows"
        else:
            return "Fichier programme"
            
    def _toggle_microphone(self):
        """Active/désactive le microphone"""
        current_text = self.mic_btn.cget("text")
        if current_text == "🎤":
            self.mic_btn.configure(text="🔴", fg_color="#FF5555")
            self._add_chat_message("system", "🎤 Microphone activé - Parlez maintenant")
        else:
            self.mic_btn.configure(text="🎤", fg_color="#00FF00")
            self._add_chat_message("system", "🎤 Microphone désactivé")
            
    def _send_message(self):
        """Envoie un message"""
        message = self.chat_input.get().strip()
        if not message:
            return
            
        self.chat_input.delete(0, "end")
        self._add_chat_message("user", message)
        
        # Réponse simulée
        self.root.after(1000, lambda: self._simulate_response(message))
        
    def _add_chat_message(self, sender, text):
        """Ajoute un message au chat"""
        color = "#00FF00" if sender == "user" else "#FFFFFF"
        bg = "#111111" if sender == "user" else "#222222"
        
        msg_frame = ctk.CTkFrame(
            self.chat_frame,
            fg_color=bg,
            corner_radius=10
        )
        msg_frame.pack(fill="x", pady=5, padx=5, anchor="e" if sender == "user" else "w")
        
        ctk.CTkLabel(
            msg_frame,
            text=text,
            font=("Segoe UI", 13),
            text_color=color,
            wraplength=250,
            justify="left"
        ).pack(padx=12, pady=10)
        
        # Défiler vers le bas
        self.chat_frame._parent_canvas.yview_moveto(1.0)
        
    def _simulate_response(self, message):
        """Simule une réponse de l'IA"""
        responses = {
            "bonjour": "👋 Bonjour ! Comment puis-je vous aider ?",
            "heure": f"🕐 Il est {time.strftime('%H:%M')}",
            "apps": f"📱 Vous avez {len(self.config['apps_permissions'])} applications activées",
            "aide": "💡 Je peux vous aider à:\n• Lancer des applications\n• Surveiller votre système\n• Répondre à vos questions",
            "merci": "😊 Avec plaisir !"
        }
        
        message_lower = message.lower()
        response = "🤖 J'ai bien reçu votre message. Comment puis-je vous assister ?"
        
        for key, resp in responses.items():
            if key in message_lower:
                response = resp
                break
                
        self._add_chat_message("assistant", response)
        
    def _start_monitoring(self):
        """Démarre la surveillance système"""
        self._update_metrics()
        
    def _update_metrics(self):
        """Met à jour les métriques système"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self.metrics["CPU"].configure(text=f"⚡ CPU: {cpu_percent:.1f}%")
            
            # RAM
            ram_percent = psutil.virtual_memory().percent
            self.metrics["RAM"].configure(text=f"💾 RAM: {ram_percent:.1f}%")
            
            # Disk
            disk_percent = psutil.disk_usage('C:\\').percent
            self.metrics["DISK"].configure(text=f"💿 Disque: {disk_percent:.1f}%")
            
            # Network (simplifié)
            net_io = psutil.net_io_counters()
            kb_sent = net_io.bytes_sent / 1024
            kb_recv = net_io.bytes_recv / 1024
            self.metrics["NETWORK"].configure(text=f"🌐 Réseau: ↑{kb_sent:.0f} ↓{kb_recv:.0f} Kb")
            
        except:
            pass
            
        # Mettre à jour toutes les 2 secondes
        self.root.after(2000, self._update_metrics)
        
    def _add_activity(self, activity):
        """Ajoute une activité au monitoring"""
        act_frame = ctk.CTkFrame(self.activities_frame, fg_color="#222222", height=35)
        act_frame.pack(fill="x", pady=2)
        
        ctk.CTkLabel(
            act_frame,
            text=activity,
            font=("Segoe UI", 12),
            text_color="#FFFFFF"
        ).pack(side="left", padx=10)
        
        ctk.CTkLabel(
            act_frame,
            text=time.strftime("%H:%M"),
            font=("Segoe UI", 11),
            text_color="#888888"
        ).pack(side="right", padx=10)
        
    def _refresh_apps(self):
        """Rafraîchit la liste des apps"""
        self._display_apps_list()
        
    def run(self):
        """Lance l'interface principale"""
        self.root.mainloop()


# Lancement
if __name__ == "__main__":
    app = ExocortexApp()
    app.run()