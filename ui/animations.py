"""
Système d'animations pour Zodiac OS - Style EVA AI
Auteur: tvcraft01
"""
import customtkinter as ctk
import random
import math
from PIL import Image, ImageDraw, ImageTk
import time

class ZodiacAnimations:
    def __init__(self, root):
        self.root = root
        self.canvas = None
        self.effects = []
        
    def setup_canvas(self, parent):
        """Configure le canvas pour les animations"""
        self.canvas = ctk.CTkCanvas(
            parent,
            bg="#000011",
            highlightthickness=0
        )
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.canvas.lower()  # Mettre en arrière-plan
        
    def start_background_effects(self):
        """Démarre les effets de fond"""
        self.create_cyberpunk_grid()
        self.create_floating_particles()
        self.create_data_streams()
        
    def create_cyberpunk_grid(self):
        """Crée une grille cyberpunk animée"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # Grille principale
        grid_lines = []
        for i in range(0, width, 30):
            line = self.canvas.create_line(i, 0, i, height, fill="#00FFFF11", width=1)
            grid_lines.append(line)
        for i in range(0, height, 30):
            line = self.canvas.create_line(0, i, width, i, fill="#00FFFF11", width=1)
            grid_lines.append(line)
            
        # Animation de la grille
        def animate_grid():
            for line in grid_lines:
                # Variation légère de l'opacité
                current_color = self.canvas.itemcget(line, "fill")
                if random.random() > 0.95:
                    new_color = "#00FFFF22" if "11" in current_color else "#00FFFF11"
                    self.canvas.itemconfig(line, fill=new_color)
            self.root.after(1000, animate_grid)
            
        animate_grid()
        
    def create_floating_particles(self):
        """Crée des particules flottantes"""
        colors = ["#00FFFF", "#FF00FF", "#00FFAA", "#FFAA00"]
        
        for _ in range(30):
            x = random.randint(0, self.canvas.winfo_width())
            y = random.randint(0, self.canvas.winfo_height())
            size = random.randint(2, 5)
            color = random.choice(colors)
            
            particle = self.canvas.create_oval(
                x, y, x + size, y + size,
                fill=color,
                outline=""
            )
            
            self.effects.append({
                "type": "particle",
                "id": particle,
                "x": x,
                "y": y,
                "dx": random.uniform(-0.3, 0.3),
                "dy": random.uniform(-0.3, 0.3),
                "color": color,
                "alpha": random.uniform(0.3, 0.8)
            })
            
        self.animate_particles()
        
    def animate_particles(self):
        """Anime les particules"""
        for effect in self.effects:
            if effect["type"] == "particle":
                # Déplacer
                self.canvas.move(effect["id"], effect["dx"], effect["dy"])
                effect["x"] += effect["dx"]
                effect["y"] += effect["dy"]
                
                # Rebond sur les bords
                if effect["x"] <= 0 or effect["x"] >= self.canvas.winfo_width():
                    effect["dx"] *= -1
                if effect["y"] <= 0 or effect["y"] >= self.canvas.winfo_height():
                    effect["dy"] *= -1
                    
                # Variation d'opacité
                effect["alpha"] += random.uniform(-0.02, 0.02)
                effect["alpha"] = max(0.1, min(1.0, effect["alpha"]))
                
        self.root.after(50, self.animate_particles)
        
    def create_data_streams(self):
        """Crée des flux de données (effet Matrix)"""
        width = self.canvas.winfo_width()
        
        for _ in range(10):
            x = random.randint(0, width)
            length = random.randint(20, 100)
            speed = random.uniform(1, 3)
            
            stream = self.canvas.create_line(
                x, 0, x, length,
                fill="#00FFAA",
                width=2
            )
            
            self.effects.append({
                "type": "stream",
                "id": stream,
                "x": x,
                "y": 0,
                "length": length,
                "speed": speed
            })
            
        self.animate_data_streams()
        
    def animate_data_streams(self):
        """Anime les flux de données"""
        for effect in self.effects:
            if effect["type"] == "stream":
                # Déplacer vers le bas
                self.canvas.move(effect["id"], 0, effect["speed"])
                effect["y"] += effect["speed"]
                
                # Réinitialiser en haut si hors écran
                if effect["y"] > self.canvas.winfo_height():
                    self.canvas.coords(effect["id"], effect["x"], 0, effect["x"], effect["length"])
                    effect["y"] = 0
                    
        self.root.after(30, self.animate_data_streams)
        
    def create_scan_effect(self, widget):
        """Crée un effet de scan sur un widget"""
        x, y = widget.winfo_rootx() - self.root.winfo_rootx(), widget.winfo_rooty() - self.root.winfo_rooty()
        width, height = widget.winfo_width(), widget.winfo_height()
        
        scan_line = self.canvas.create_line(
            x, y, x + width, y,
            fill="#00FFFF",
            width=2
        )
        
        def animate_scan():
            current_y = self.canvas.coords(scan_line)[1]
            if current_y < y + height:
                self.canvas.coords(scan_line, x, current_y + 5, x + width, current_y + 5)
                self.root.after(10, animate_scan)
            else:
                self.canvas.delete(scan_line)
                
        animate_scan()
        
    def create_pulse_effect(self, widget, color="#00FFFF"):
        """Crée un effet de pulsation sur un widget"""
        x, y = widget.winfo_rootx() - self.root.winfo_rootx(), widget.winfo_rooty() - self.root.winfo_rooty()
        width, height = widget.winfo_width(), widget.winfo_height()
        
        center_x, center_y = x + width//2, y + height//2
        max_radius = max(width, height) // 2
        
        circles = []
        
        def create_circle(radius, alpha):
            circle = self.canvas.create_oval(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                outline=color,
                width=2
            )
            circles.append((circle, radius, alpha))
            
        # Créer plusieurs cercles concentriques
        for i in range(3):
            create_circle(10 + i*20, 0.5 - i*0.15)
            
        def animate_pulse():
            for i, (circle, radius, alpha) in enumerate(circles):
                # Agrandir le cercle
                new_radius = radius + 2
                new_alpha = alpha - 0.05
                
                if new_alpha > 0:
                    self.canvas.coords(
                        circle,
                        center_x - new_radius, center_y - new_radius,
                        center_x + new_radius, center_y + new_radius
                    )
                    circles[i] = (circle, new_radius, new_alpha)
                else:
                    self.canvas.delete(circle)
                    circles[i] = None
                    
            # Nettoyer les cercles supprimés
            circles[:] = [c for c in circles if c is not None]
            
            if circles:
                self.root.after(30, animate_pulse)
                
        animate_pulse()
        
    def create_typing_effect(self, label, text, speed=50):
        """Effet de frappe pour le texte"""
        current_text = ""
        label.configure(text="")
        
        def type_char(i):
            nonlocal current_text
            if i < len(text):
                current_text += text[i]
                label.configure(text=current_text + "█")
                self.root.after(speed, lambda: type_char(i + 1))
            else:
                label.configure(text=text)
                
        type_char(0)
        
    def create_transition_effect(self, callback):
        """Effet de transition entre les onglets"""
        overlay = ctk.CTkFrame(
            self.root,
            fg_color="#000011",
            corner_radius=0
        )
        overlay.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Lignes de scan
        scan_lines = []
        for i in range(20):
            line = self.canvas.create_line(
                0, i * 30,
                self.canvas.winfo_width(), i * 30,
                fill="#00FFFF",
                width=1
            )
            scan_lines.append(line)
            
        def animate_transition():
            # Animer les lignes
            for line in scan_lines:
                self.canvas.move(line, 0, 5)
                
            # Vérifier si terminé
            coords = self.canvas.coords(scan_lines[0])
            if coords[1] > self.canvas.winfo_height():
                # Transition terminée
                overlay.destroy()
                for line in scan_lines:
                    self.canvas.delete(line)
                callback()
            else:
                self.root.after(16, animate_transition)
                
        animate_transition()