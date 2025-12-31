🎤 Zodiac - Assistant Vocal Intelligent
https://img.shields.io/badge/Python-3.8+-blue.svg
https://img.shields.io/badge/Version-1.0.0-orange.svg
https://img.shields.io/badge/License-MIT-green.svg
https://img.shields.io/badge/Status-Active-brightgreen.svg

Assistant vocal français avec architecture modulaire, reconnaissance vocale et interface moderne.

✨ Démo Rapide
bash
# Installation
git clone https://github.com/tvcraft01/zodiac
cd zodiac
pip install -r requirements.txt

# Lancement
python main.py

# Commandes vocales :
# "Zodiac, ouvre Chrome"
# "Zodiac, musique suivante"
# "Zodiac, quelle heure est-il ?"
🏗️ Architecture Modulaire
Module	Description	Statut
🏗️ core/	Cœur système, gestion vocale	✅ Actif
🤖 ai/	Intelligence artificielle	🚧 En développement
🎨 ui/	Interface utilisateur	✅ Actif
⚡ tools/	Outils productivité	📅 Planifié
🎮 media/	Contrôle multimédia	📅 Planifié
🚀 Installation
Windows (Recommandé)
bash
# Double-clique sur :
installe.bat
Installation Manuelle
bash
git clone https://github.com/tvcraft01/zodiac.git
cd zodiac
pip install -r requirements.txt
python main.py
Avec voix complète
bash
pip install -r requirements_voice.txt
🎯 Fonctionnalités
🎤 Reconnaissance Vocale
Activation par mot-clé "Zodiac"

Support français natif

Écoute continue/ponctuelle

🤖 Intelligence
Conversation contextuelle

Recherche web intelligente

Mémoire des sessions

🎨 Interface
Interface Tkinter moderne

Logs en temps réel

Thèmes personnalisables

⚡ Commandes Système
Lancement d'applications

Contrôle multimédia

Informations système (CPU, RAM)

Recherche Google

📁 Structure du Projet
text
zodiac/
├── main.py                    # Point d'entrée
├── setup.py                   # Installation
├── requirements.txt           # Dépendances
│
├── core/                      # Noyau système
│   ├── assistant.py           # Assistant principal
│   ├── voice_engine.py        # Reconnaissance vocale
│   └── command_handler.py     # Gestion des commandes
│
├── ai/                        # Intelligence
│   ├── conversation.py        # Dialogue
│   └── web_search.py          # Recherche internet
│
├── ui/                        # Interface
│   ├── main_window.py         # Fenêtre principale
│   └── widgets.py             # Composants UI
│
├── tools/                     # Productivité
│   └── (modules à venir)
│
├── media/                     # Multimédia
│   └── (modules à venir)
│
├── config/                    # Configuration
└── data/                      # Données utilisateur
🎮 Utilisation
Mode Vocal
Lancez Zodiac : python main.py

Dites "Zodiac" pour activer

Donnez votre commande

Exemples de Commandes
bash
# Applications
"Zodiac, ouvre Chrome"
"Zodiac, lance Spotify"

# Musique
"Zodiac, musique suivante"
"Zodiac, pause musique"

# Système
"Zodiac, état du système"
"Zodiac, quelle heure est-il ?"

# Web
"Zodiac, recherche Python programming"
Mode Texte
Utilisez la zone de saisie dans l'interface

Appuyez sur Entrée pour envoyer

🔧 Pour les Développeurs
Contribuer
Fork le projet

Créez une branche : git checkout -b feature/nouvelle-fonctionnalite

Commitez : git commit -m 'Ajout de...'

Push : git push origin feature/nouvelle-fonctionnalite

Ouvrez une Pull Request

Installation Développement
bash
git clone https://github.com/tvcraft01/zodiac.git
cd zodiac
pip install -r requirements.txt
pip install -r requirements_voice.txt  # Optionnel
Créer un Exécutable
bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
📊 Roadmap
✅ Phase 1 : Fondations (Terminée)
Architecture modulaire

Reconnaissance vocale de base

Interface utilisateur

🚧 Phase 2 : Intelligence (En cours)
IA conversationnelle avancée

Recherche web contextuelle

Mémoire à long terme

📅 Phase 3 : Productivité (Planifiée)
Prise de notes vocale

Minuteur/alarmes

Automatisations personnalisées

🤝 Contribution
Les contributions sont les bienvenues !
Consultez les issues pour voir les tâches en cours.

🐛 Signaler un Problème
Si vous trouvez un bug ou avez une suggestion :

Vérifiez si le problème existe déjà dans les issues

Sinon, créez une nouvelle issue avec :

Description claire du problème

Étapes pour reproduire

Comportement attendu

📞 Contact
Auteur : tvcraft01

Repository : https://github.com/tvcraft01/zodiac

Issues : https://github.com/tvcraft01/zodiac/issues

📄 Licence
Ce projet est sous licence MIT.
Voir le fichier LICENSE pour plus de détails.

<div align="center">
⭐ Soutenez le projet en lui donnant une étoile sur GitHub !
Développé avec ❤️ par tvcraft01

⬆ Retour en haut

</div>
