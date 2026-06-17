import requests
import time
from typing import Optional, Dict, Any

class StoreFetcher:
    """
    Module responsable des appels vers l'API Steam Store.
    """
    def __init__(self) -> None:
        self.url_store: str = "https://store.steampowered.com/api/featuredcategories"
        self.url_app: str = "https://store.steampowered.com/api/appdetails"
        self.headers: Dict[str, str] = {"User-Agent": "SteamBundleBot/1.0"}

    def fetch_store(self) -> Optional[Dict[str, Any]]:
        """
        Récupère les données de la page d'accueil (featuredcategories).
        """
        try:
            response = requests.get(self.url_store, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur lors de la requête API Store : {e}")
            return None

    def has_card(self, app_id: int) -> bool:
        """
        Vérifie si un jeu (app_id) possède des cartes Steam (category id: 29).
        Intègre un délai de sécurité pour éviter le rate-limiting.
        """
        time.sleep(1.5)  # Respect du rate-limit Steam
        try:
            params = {'appids': app_id}
            response = requests.get(self.url_app, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            app_data = data.get(str(app_id), {})
            
            if not app_data.get('success'):
                return False
                
            categories = app_data.get('data', {}).get('categories', [])
            for cat in categories:
                if cat.get('id') == 29:
                    return True
                    
            return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur réseau lors de la vérification des cartes pour {app_id}: {e}")
            return False
        except Exception as e:
            print(f"❌ Erreur inattendue pour {app_id}: {e}")
            return False