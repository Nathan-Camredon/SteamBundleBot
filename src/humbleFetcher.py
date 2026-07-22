import requests
import time
import json
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional

class HumbleFetcher:
    """
    Module responsable de la récupération des bundles sur Humble Bundle.
    """
    def __init__(self) -> None:
        self.url_bundles: str = "https://www.humblebundle.com/bundles"
        self.headers: Dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        self.steam_apps_cache: Dict[str, int] = {}
        self._load_steam_apps()

    def _load_steam_apps(self) -> None:
        """
        Charge la liste de toutes les apps Steam pour résoudre les noms en app_id.
        """
        print("🔄 Chargement du cache des applications Steam (HumbleFetcher)...")
        try:
            response = requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2/", timeout=15)
            response.raise_for_status()
            data = response.json()
            apps = data.get("applist", {}).get("apps", [])
            for app in apps:
                # Store lowercased names for easier matching
                self.steam_apps_cache[app["name"].lower()] = app["appid"]
        except Exception as e:
            print(f"⚠️ Impossible de charger la liste des applications Steam: {e}")

    def _resolve_steam_app_id(self, game_name: str) -> Optional[int]:
        """
        Tente de trouver l'app_id Steam à partir du nom du jeu.
        """
        if not game_name:
            return None
            
        name_lower = game_name.lower().strip()
        if name_lower in self.steam_apps_cache:
            return self.steam_apps_cache[name_lower]
            
        return None

    def fetch_bundles(self) -> List[Dict[str, Any]]:
        """
        Récupère les bundles actifs sur Humble Bundle.
        """
        bundles_found = []
        try:
            response = requests.get(self.url_bundles, headers=self.headers, timeout=15)
            if response.status_code == 403:
                print("⚠️ Accès refusé à Humble Bundle (Cloudflare/403).")
                return bundles_found
                
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Recherche des données JSON intégrées
            scripts = soup.find_all('script')
            json_data = None
            for script in scripts:
                content = script.string
                if not content:
                    continue
                    
                if script.get('id') == '__NEXT_DATA__':
                    try:
                        json_data = json.loads(content)
                        break
                    except json.JSONDecodeError:
                        pass
                elif 'window.client_view_data' in content:
                    # Extraction rudimentaire d'une assignation globale
                    try:
                        start_idx = content.find('{')
                        end_idx = content.rfind('}') + 1
                        if start_idx != -1 and end_idx != -1:
                            json_data = json.loads(content[start_idx:end_idx])
                        break
                    except json.JSONDecodeError:
                        pass
                elif 'webpack-bundle-data' in content:
                    try:
                        json_data = json.loads(content)
                        break
                    except:
                        pass

            if json_data:
                print("💡 Données JSON Humble Bundle trouvées, mais l'extraction des Tiers nécessite une structure spécifique.")
                # Le format de Humble Bundle change fréquemment.
                # Pour l'instant, on n'ajoute rien à bundles_found pour éviter un plantage
                # avec des données non documentées.
                pass
            else:
                print("⚠️ Impossible d'extraire les données JSON de Humble Bundle (Format inconnu ou Cloudflare).")

        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur réseau lors de la récupération des bundles Humble : {e}")
        except Exception as e:
            print(f"❌ Erreur inattendue : {e}")

        return bundles_found
