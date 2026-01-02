class ScreenManager:
    def __init__(self):
        # Configuration utilisateur
        self.config = {
            "language": "fr",
            "apps_permissions": {},
            "system_access": True,
            "privacy_mode": False,
            "scan_complete": False,
            "ai_choice": "local",  # Nouveau
            "api_key": "",         # Nouveau
            "use_internet": True   # Nouveau
        }