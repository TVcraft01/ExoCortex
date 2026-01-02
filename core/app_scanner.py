# core/app_scanner.py
import os
import winreg
import json
from PIL import Image, ImageTk
import subprocess
import sys
from pathlib import Path

class WindowsAppScanner:
    """Scanner d'applications Windows réel"""
    
    def __init__(self):
        self.applications = []
        self.categories = {
            "productivity": ["office", "word", "excel", "powerpoint", "outlook"],
            "development": ["visual studio", "pycharm", "vscode", "python", "git"],
            "media": ["vlc", "spotify", "photos", "video", "music"],
            "browsers": ["chrome", "firefox", "edge", "opera", "brave"],
            "gaming": ["steam", "epic", "ubisoft", "game", "riot"],
            "tools": ["calculator", "notepad", "paint", "cmd", "powershell"],
            "system": ["control panel", "settings", "task manager", "device manager"]
        }
        
    def scan_registry(self):
        """Scanner le registre Windows pour les applications installées"""
        apps = []
        
        # Clés de registre à scanner
        registry_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        ]
        
        for hive, path in registry_paths:
            try:
                key = winreg.OpenKey(hive, path)
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)
                        
                        # Récupérer les informations
                        app_info = self._extract_app_info(subkey)
                        if app_info:
                            apps.append(app_info)
                            
                        winreg.CloseKey(subkey)
                    except:
                        continue
                winreg.CloseKey(key)
            except:
                continue
                
        return apps
    
    def _extract_app_info(self, subkey):
        """Extrait les informations d'une application depuis la clé de registre"""
        try:
            # Récupérer le nom
            name, _ = winreg.QueryValueEx(subkey, "DisplayName")
            if not name:
                return None
                
            # Ignorer les mises à jour Windows
            if "update" in name.lower() or "mise à jour" in name.lower():
                return None
                
            app = {
                "name": name,
                "id": winreg.QueryValueEx(subkey, "UninstallString")[0] if winreg.QueryValueEx(subkey, "UninstallString") else "",
                "version": winreg.QueryValueEx(subkey, "DisplayVersion")[0] if winreg.QueryValueEx(subkey, "DisplayVersion") else "1.0.0",
                "publisher": winreg.QueryValueEx(subkey, "Publisher")[0] if winreg.QueryValueEx(subkey, "Publisher") else "Unknown",
                "install_date": winreg.QueryValueEx(subkey, "InstallDate")[0] if winreg.QueryValueEx(subkey, "InstallDate") else "",
                "install_location": winreg.QueryValueEx(subkey, "InstallLocation")[0] if winreg.QueryValueEx(subkey, "InstallLocation") else "",
                "exe_path": self._find_exe_path(subkey),
                "category": "unknown",
                "is_favorite": False
            }
            
            # Déterminer la catégorie
            app["category"] = self._categorize_app(app["name"].lower())
            
            # Chercher l'icône
            app["icon_path"] = self._find_icon_path(app)
            
            return app
            
        except:
            return None
    
    def _find_exe_path(self, subkey):
        """Trouve le chemin de l'exécutable"""
        try:
            # Essayer DisplayIcon
            icon_path, _ = winreg.QueryValueEx(subkey, "DisplayIcon")
            if icon_path and icon_path.lower().endswith('.exe'):
                return icon_path.split(',')[0]  # Enlever l'index d'icône
            
            # Essayer InstallLocation + nom d'exe probable
            install_path, _ = winreg.QueryValueEx(subkey, "InstallLocation")
            if install_path:
                exe_name = winreg.QueryValueEx(subkey, "DisplayName")[0].split()[0] + ".exe"
                possible_paths = [
                    os.path.join(install_path, exe_name),
                    os.path.join(install_path, "bin", exe_name),
                    os.path.join(install_path, "app", exe_name),
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        return path
                        
        except:
            pass
            
        return ""
    
    def _find_icon_path(self, app):
        """Trouve le chemin de l'icône"""
        # Priorité 1: DisplayIcon du registre
        # Priorité 2: EXE lui-même
        # Priorité 3: Icône par défaut
        
        if app["exe_path"] and os.path.exists(app["exe_path"]):
            return app["exe_path"]
            
        # Chercher dans les dossiers communs
        common_paths = [
            os.path.join(os.environ.get("PROGRAMFILES", ""), app["name"]),
            os.path.join(os.environ.get("PROGRAMFILES(X86)", ""), app["name"]),
            os.path.join(os.environ.get("APPDATA", ""), app["name"]),
            os.path.join(os.environ.get("LOCALAPPDATA", ""), app["name"]),
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.lower().endswith('.exe'):
                            return os.path.join(root, file)
                            
        return ""
    
    def _categorize_app(self, app_name):
        """Catégorise une application par son nom"""
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword in app_name:
                    return category
                    
        return "other"
    
    def scan_common_folders(self):
        """Scanner les dossiers communs d'applications"""
        apps = []
        
        folders = [
            os.environ.get("PROGRAMFILES", "C:\\Program Files"),
            os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)"),
            os.path.join(os.environ.get("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs"),
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs"),
        ]
        
        for folder in folders:
            if os.path.exists(folder):
                apps.extend(self._scan_folder(folder))
                
        return apps
    
    def _scan_folder(self, folder_path):
        """Scanner un dossier récursivement pour les .exe"""
        apps = []
        
        try:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith('.exe') and not file.lower().startswith('uninst'):
                        app_path = os.path.join(root, file)
                        
                        # Éviter les fichiers système
                        if any(skip in app_path.lower() for skip in ["system32", "windows", "temp", "cache"]):
                            continue
                            
                        app = {
                            "name": os.path.splitext(file)[0],
                            "id": app_path,
                            "version": "1.0.0",
                            "publisher": "Unknown",
                            "install_date": "",
                            "install_location": root,
                            "exe_path": app_path,
                            "category": self._categorize_app(file.lower()),
                            "icon_path": app_path,
                            "is_favorite": False
                        }
                        
                        apps.append(app)
                        
        except:
            pass
            
        return apps
    
    def scan_start_menu(self):
        """Scanner le menu Démarrer"""
        apps = []
        
        start_menu_paths = [
            os.path.join(os.environ.get("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs"),
            os.path.join(os.environ.get("PROGRAMDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs"),
        ]
        
        for start_path in start_menu_paths:
            if os.path.exists(start_path):
                apps.extend(self._scan_shortcuts(start_path))
                
        return apps
    
    def _scan_shortcuts(self, folder_path):
        """Scanner les raccourcis .lnk"""
        apps = []
        
        try:
            import pythoncom
            from win32com.shell import shell, shellcon
            
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith('.lnk'):
                        shortcut_path = os.path.join(root, file)
                        
                        try:
                            # Résoudre le raccourci
                            pythoncom.CoInitialize()
                            shell_link = pythoncom.CoCreateInstance(
                                shell.CLSID_ShellLink,
                                None,
                                pythoncom.CLSCTX_INPROC_SERVER,
                                shell.IID_IShellLink
                            )
                            
                            persist_file = shell_link.QueryInterface(pythoncom.IID_IPersistFile)
                            persist_file.Load(shortcut_path)
                            
                            # Récupérer le chemin cible
                            target_path = shell_link.GetPath(shell.SLGP_SHORTPATH)[0]
                            
                            if target_path and target_path.lower().endswith('.exe'):
                                app = {
                                    "name": os.path.splitext(file)[0].replace('.lnk', ''),
                                    "id": shortcut_path,
                                    "version": "1.0.0",
                                    "publisher": "Unknown",
                                    "install_date": "",
                                    "install_location": os.path.dirname(target_path),
                                    "exe_path": target_path,
                                    "category": self._categorize_app(file.lower()),
                                    "icon_path": target_path,
                                    "is_favorite": False
                                }
                                
                                apps.append(app)
                                
                        except:
                            continue
                            
        except ImportError:
            # win32com n'est pas disponible, on saute cette méthode
            pass
            
        return apps
    
    def get_all_applications(self):
        """Récupère toutes les applications"""
        print("[SCANNER] Scan du registre Windows...")
        registry_apps = self.scan_registry()
        
        print("[SCANNER] Scan des dossiers communs...")
        folder_apps = self.scan_common_folders()
        
        print("[SCANNER] Scan du menu Démarrer...")
        start_apps = self.scan_start_menu()
        
        # Fusionner et dédupliquer
        all_apps = []
        seen_ids = set()
        
        for app in registry_apps + folder_apps + start_apps:
            app_id = app.get("exe_path") or app.get("id") or app.get("name")
            if app_id and app_id not in seen_ids and app["name"]:
                seen_ids.add(app_id)
                all_apps.append(app)
                
        print(f"[SCANNER] {len(all_apps)} applications trouvées")
        return all_apps
    
    def launch_application(self, app_path):
        """Lance une application"""
        try:
            if os.path.exists(app_path):
                os.startfile(app_path)
                return True
            return False
        except:
            try:
                subprocess.Popen([app_path], shell=True)
                return True
            except:
                return False
    
    def get_icon_image(self, app, size=(64, 64)):
        """Récupère l'icône d'une application"""
        try:
            from PIL import Image
            import win32ui
            import win32gui
            import win32con
            import win32api
            
            # Essayer d'extraire l'icône du EXE
            if app.get("icon_path") and os.path.exists(app["icon_path"]):
                ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
                ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)
                
                large, small = win32gui.ExtractIconEx(app["icon_path"], 0)
                win32gui.DestroyIcon(small[0])
                
                hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
                hbmp = win32ui.CreateBitmap()
                hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_y)
                hdc = hdc.CreateCompatibleDC()
                
                hdc.SelectObject(hbmp)
                hdc.DrawIcon((0,0), large[0])
                
                bmpinfo = hbmp.GetInfo()
                bmpstr = hbmp.GetBitmapBits(True)
                
                img = Image.frombuffer(
                    'RGB',
                    (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                    bmpstr, 'raw', 'BGRX', 0, 1
                )
                
                win32gui.DestroyIcon(large[0])
                return img.resize(size, Image.Resampling.LANCZOS)
                
        except:
            pass
            
        # Icône par défaut
        return self._create_default_icon(app["name"], size)
    
    def _create_default_icon(self, name, size):
        """Crée une icône par défaut"""
        from PIL import Image, ImageDraw, ImageFont
        
        img = Image.new('RGB', size, '#6C63FF')
        draw = ImageDraw.Draw(img)
        
        try:
            # Essayer d'ajouter la première lettre
            font = ImageFont.truetype("arial.ttf", 32)
            text = name[0].upper() if name else "A"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
            draw.text(position, text, font=font, fill='white')
        except:
            pass
            
        return img