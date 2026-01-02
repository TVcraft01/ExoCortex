"""
Splash Screen style EVA AI - Animations cyberpunk avancées
Inspiré de: https://www.youtube.com/watch?v=yRA5jS7q05A
Auteur: tvcraft01
"""
import customtkinter as ctk
import threading
import time
import sys
import os
from PIL import Image, ImageTk, ImageDraw, ImageFont
import random
import math

class EvaSplashScreen:
    def __init__(self, on_complete_callback):
        """
        Initialise le splash screen style EVA AI
        """
        self.on_complete = on_complete_callback
        self.root = ctk.CTk()
        
        # Configuration de la fenêtre
        self.root.title("Zodiac OS")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        
        # Fenêtre sans bordure et transparente
        self.root.overrideredirect(True)
        self.root.attributes('-alpha', 0.0)
        
        # Centrer la fenêtre
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Palette de couleurs EVA AI
        self.bg_color = "#000011"  # Bleu nuit profond
        self.primary_color = "#00FFFF"  # Cyan néon
        self.accent_color = "#FF00FF"  # Magenta néon
        self.secondary_color = "#00FFAA"  # Vert cyan
        self.text_color = "#FFFFFF"
        self.grid_color = "#00FFFF22"  # Grille semi-transparente
        
        # Configurer le thème
        ctk.set_appearance_mode("dark")
        
        # Variables d'animation
        self.particles = []
        self.scan_lines = []
        self.hologram_effects = []
        self.terminal_text = []
        
        # Créer le contenu
        self.setup_ui()
        
        # Démarrer les animations
        self.start_animations()
        
        # Faire apparaître la fenêtre
        self.fade_in()
        
    def setup_ui(self):
        """Configure l'interface du splash screen"""
        # Frame principal avec fond personnalisé
        self.main_frame = ctk.CTkFrame(
            self.root, 
            fg_color=self.bg_color,
            corner_radius=0
        )
        self.main_frame.pack(fill="both", expand=True)
        
        # Canvas pour les effets graphiques
        self.canvas = ctk.CTkCanvas(
            self.main_frame,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        # --- EFFETS DE FOND ---
        self.create_background_effects()
        
        # --- LOGO ZODIAC CYBERPUNK ---
        self.logo_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent",
            corner_radius=0
        )
        self.logo_frame.place(relx=0.5, rely=0.3, anchor="center")
        
        # Logo principal avec effet néon
        self.logo_label = ctk.CTkLabel(
            self.logo_frame,
            text="ZODIAC",
            font=("Orbitron", 64, "bold"),
            text_color=self.primary_color
        )
        self.logo_label.pack(pady=(0, 10))
        
        # Sous-titre avec glow
        self.subtitle_label = ctk.CTkLabel(
            self.logo_frame,
            text="SYSTEM INITIALIZATION",
            font=("Orbitron", 18),
            text_color=self.secondary_color
        )
        self.subtitle_label.pack()
        
        # --- TERMINAL DE CHARGEMENT ---
        self.terminal_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#000000",
            corner_radius=5,
            width=600,
            height=200
        )
        self.terminal_frame.place(relx=0.5, rely=0.65, anchor="center")
        self.terminal_frame.grid_propagate(False)
        
        # Texte du terminal
        self.terminal_text_widget = ctk.CTkTextbox(
            self.terminal_frame,
            fg_color="#000000",
            text_color=self.primary_color,
            border_width=0,
            font=("Consolas", 12),
            height=180,
            width=580
        )
        self.terminal_text_widget.pack(pady=10, padx=10)
        self.terminal_text_widget.configure(state="disabled")
        
        # Curseur clignotant
        self.cursor_label = ctk.CTkLabel(
            self.terminal_frame,
            text="█",
            font=("Consolas", 12),
            text_color=self.primary_color
        )
        self.cursor_label.place(x=20, y=170)
        
        # --- BARRE DE PROGRESSION FUTURISTE ---
        self.progress_container = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent",
            height=30
        )
        self.progress_container.place(relx=0.5, rely=0.85, anchor="center", width=600)
        
        # Barre de progression
        self.progress_bg = ctk.CTkFrame(
            self.progress_container,
            fg_color="#111133",
            height=20,
            corner_radius=10
        )
        self.progress_bg.pack(fill="x", pady=5)
        
        self.progress_fill = ctk.CTkFrame(
            self.progress_bg,
            fg_color=self.primary_color,
            height=16,
            corner_radius=8,
            width=0
        )
        self.progress_fill.place(x=2, y=2)
        
        # Pourcentage
        self.percentage_label = ctk.CTkLabel(
            self.progress_container,
            text="0%",
            font=("Orbitron", 16, "bold"),
            text_color=self.primary_color
        )
        self.percentage_label.pack()
        
        # --- INDICATEUR DE STATUT ---
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="> INITIALIZING CORE SYSTEMS...",
            font=("Consolas", 12),
            text_color=self.secondary_color
        )
        self.status_label.place(relx=0.5, rely=0.92, anchor="center")
        
        # --- COPYRIGHT ---
        self.copyright_label = ctk.CTkLabel(
            self.main_frame,
            text="© 2024 ZODIAC AI SYSTEMS | v2.0.0",
            font=("Consolas", 10),
            text_color="#6666AA"
        )
        self.copyright_label.place(relx=0.5, rely=0.97, anchor="center")
        
    def create_background_effects(self):
        """Crée les effets de fond cyberpunk"""
        # Grille holographique
        self.draw_grid()
        
        # Lignes de scan
        self.create_scan_lines()
        
        # Particules
        self.create_particles()
        
    def draw_grid(self):
        """Dessine une grille holographique"""
        width = 900
        height = 600
        
        for i in range(0, width, 40):
            self.canvas.create_line(i, 0, i, height, fill=self.grid_color, width=1)
        for i in range(0, height, 40):
            self.canvas.create_line(0, i, width, i, fill=self.grid_color, width=1)
            
    def create_scan_lines(self):
        """Crée des lignes de scan animées"""
        for i in range(20):
            y = random.randint(0, 600)
            line = self.canvas.create_line(0, y, 900, y, fill=self.primary_color, width=1)
            self.scan_lines.append({
                "id": line,
                "y": y,
                "speed": random.uniform(1, 3)
            })
            
    def create_particles(self):
        """Crée des particules flottantes"""
        for _ in range(50):
            x = random.randint(0, 900)
            y = random.randint(0, 600)
            size = random.randint(1, 3)
            particle = self.canvas.create_oval(
                x, y, x + size, y + size,
                fill=self.primary_color,
                outline=""
            )
            self.particles.append({
                "id": particle,
                "x": x,
                "y": y,
                "dx": random.uniform(-0.5, 0.5),
                "dy": random.uniform(-0.5, 0.5),
                "alpha": random.uniform(0.3, 0.8)
            })
            
    def fade_in(self):
        """Animation d'apparition en fondu"""
        def fade(alpha):
            if alpha <= 1.0:
                self.root.attributes('-alpha', alpha)
                self.root.after(20, lambda: fade(alpha + 0.05))
            else:
                self.start_loading_sequence()
                
        fade(0.0)
        
    def start_animations(self):
        """Démarre toutes les animations"""
        self.animate_particles()
        self.animate_scan_lines()
        self.animate_cursor()
        self.animate_logo()
        
    def animate_particles(self):
        """Anime les particules"""
        for particle in self.particles:
            # Déplacer la particule
            self.canvas.move(particle["id"], particle["dx"], particle["dy"])
            
            # Mettre à jour la position
            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]
            
            # Rebond sur les bords
            if particle["x"] <= 0 or particle["x"] >= 900:
                particle["dx"] *= -1
            if particle["y"] <= 0 or particle["y"] >= 600:
                particle["dy"] *= -1
                
            # Variation d'opacité
            particle["alpha"] += random.uniform(-0.02, 0.02)
            particle["alpha"] = max(0.1, min(1.0, particle["alpha"]))
            
        self.root.after(50, self.animate_particles)
        
    def animate_scan_lines(self):
        """Anime les lignes de scan"""
        for line in self.scan_lines:
            # Déplacer la ligne
            self.canvas.move(line["id"], 0, line["speed"])
            line["y"] += line["speed"]
            
            # Réinitialiser si hors écran
            if line["y"] > 600:
                self.canvas.coords(line["id"], 0, 0, 900, 0)
                line["y"] = 0
                
        self.root.after(30, self.animate_scan_lines)
        
    def animate_cursor(self):
        """Fait clignoter le curseur du terminal"""
        current_color = self.cursor_label.cget("text_color")
        new_color = self.bg_color if current_color == self.primary_color else self.primary_color
        self.cursor_label.configure(text_color=new_color)
        self.root.after(500, self.animate_cursor)
        
    def animate_logo(self):
        """Animation du logo avec effet glow"""
        colors = [self.primary_color, self.accent_color, self.secondary_color]
        current_color = self.logo_label.cget("text_color")
        new_color = random.choice([c for c in colors if c != current_color])
        self.logo_label.configure(text_color=new_color)
        self.root.after(1000, self.animate_logo)
        
    def start_loading_sequence(self):
        """Démarre la séquence de chargement"""
        loading_steps = [
            ("INITIALIZING CORE SYSTEMS...", 0.1),
            ("LOADING NEURAL NETWORK...", 0.2),
            ("CONNECTING TO VOICE ENGINE...", 0.35),
            ("BOOTING AI MODULES...", 0.5),
            ("CALIBRATING SENSORS...", 0.65),
            ("LOADING INTERFACE MODULES...", 0.8),
            ("SYNCHRONIZING DATABASES...", 0.9),
            ("SYSTEM READY...", 1.0)
        ]
        
        # Démarrer l'animation dans un thread séparé
        thread = threading.Thread(target=self.run_loading_steps, args=(loading_steps,), daemon=True)
        thread.start()
        
    def run_loading_steps(self, steps):
        """Exécute les étapes de chargement"""
        for step_text, target_progress in steps:
            # Mettre à jour le statut
            self.root.after(0, self.status_label.configure, {"text": f"> {step_text}"})
            
            # Ajouter au terminal
            self.root.after(0, self.add_terminal_text, f"[{time.strftime('%H:%M:%S')}] {step_text}")
            
            # Animer la progression
            current_progress = self.get_current_progress()
            steps_count = 15
            step_increment = (target_progress - current_progress) / steps_count
            
            for i in range(steps_count):
                new_progress = current_progress + (step_increment * (i + 1))
                self.root.after(0, self.update_progress, new_progress)
                time.sleep(0.1)  # Vitesse d'animation
            
            # Petite pause entre les étapes
            time.sleep(0.3)
            
        # Chargement terminé
        self.root.after(0, self.status_label.configure, {"text": "> SYSTEM READY. LAUNCHING ZODIAC OS..."})
        self.root.after(0, self.add_terminal_text, f"[{time.strftime('%H:%M:%S')}] SYSTEM READY. LAUNCHING...")
        time.sleep(1.5)
        
        # Fermer le splash screen
        self.root.after(0, self.close_splash)
        
    def get_current_progress(self):
        """Retourne la progression actuelle"""
        width = self.progress_fill.winfo_width()
        max_width = self.progress_bg.winfo_width() - 4
        return width / max_width if max_width > 0 else 0
        
    def update_progress(self, progress):
        """Met à jour la barre de progression"""
        max_width = self.progress_bg.winfo_width() - 4
        new_width = int(max_width * progress)
        
        # Animation fluide
        current_width = self.progress_fill.winfo_width()
        if new_width > current_width:
            self.progress_fill.configure(width=new_width)
            
        # Mettre à jour le pourcentage
        percentage = int(progress * 100)
        self.percentage_label.configure(text=f"{percentage}%")
        
        # Effet glow sur la barre
        if percentage % 10 == 0:
            self.progress_fill.configure(fg_color=self.accent_color)
            self.root.after(100, lambda: self.progress_fill.configure(fg_color=self.primary_color))
            
    def add_terminal_text(self, text):
        """Ajoute du texte au terminal"""
        self.terminal_text_widget.configure(state="normal")
        self.terminal_text_widget.insert("end", text + "\n")
        self.terminal_text_widget.see("end")
        self.terminal_text_widget.configure(state="disabled")
        
        # Effet de frappe
        self.terminal_text_widget.configure(text_color=self.secondary_color)
        self.root.after(50, lambda: self.terminal_text_widget.configure(text_color=self.primary_color))
        
    def close_splash(self):
        """Ferme le splash screen avec animation"""
        # Animation de fondu
        def fade_out(alpha):
            if alpha >= 0:
                self.root.attributes('-alpha', alpha)
                self.root.after(20, lambda: fade_out(alpha - 0.05))
            else:
                self.root.destroy()
                self.on_complete()
                
        fade_out(1.0)
        
    def run(self):
        """Lance le splash screen"""
        self.root.mainloop()

# Test du splash screen
if __name__ == "__main__":
    def on_complete():
        print("🚀 Chargement terminé !")
        sys.exit(0)
        
    print("🎬 Lancement du splash screen EVA AI...")
    splash = EvaSplashScreen(on_complete)
    splash.run()