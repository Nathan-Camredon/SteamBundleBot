import requests
import time
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any, List

class StoreFetcher:
    """
    Module responsable des appels vers l'API Steam Store et Steam Web API.
    """
    def __init__(self) -> None:
        self.url_store: str = "https://store.steampowered.com/api/featuredcategories"
        self.url_app: str = "https://store.steampowered.com/api/appdetails"
        self.url_player_service: str = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
        self.headers: Dict[str, str] = {"User-Agent": "SteamBundleBot/1.0"}

    def get_owned_games(self, api_key: str, steam_id: str) -> List[int]:
        """
        Récupère la liste des app_id possédés par l'utilisateur via la Steam Web API.
        """
        if not api_key or not steam_id:
            print("⚠️ Clés Steam manquantes pour récupérer les jeux possédés.")
            return []
            
        try:
            params = {
                'key': api_key,
                'steamid': steam_id,
                'format': 'json',
                'include_played_free_games': True
            }
            response = requests.get(self.url_player_service, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            games = data.get("response", {}).get("games", [])
            owned_ids = [g["appid"] for g in games]
            return owned_ids
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des jeux possédés : {e}")
            return []

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

    def fetch_bundles(self) -> List[Dict[str, Any]]:
        """
        Scrape la page Steam des bundles (category1=996) pour trouver les vrais bundles.
        """
        url = "https://store.steampowered.com/search/?category1=996"
        bundles_found = []
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # search_result_row correspond aux entrées de la liste de recherche
            rows = soup.find_all('a', {'class': 'search_result_row'})
            for row in rows[:5]:  # Limite de 5 pour les tests
                bundle_url = row.get('href', '')
                title_span = row.find('span', {'class': 'title'})
                title = title_span.text if title_span else "Unknown Bundle"
                
                price_div = row.find('div', {'class': 'discount_final_price'})
                if not price_div:
                    continue
                    
                price_text = price_div.text.replace('€', '').replace('$', '').replace(',', '.').strip()
                try:
                    price = float(price_text)
                except ValueError:
                    continue
                
                app_ids_str = row.get('data-ds-appid', '')
                app_ids = [int(i) for i in app_ids_str.split(',') if i.isdigit()]
                
                if bundle_url and app_ids:
                    bundles_found.append({
                        "name": title,
                        "url": bundle_url,
                        "price": price,
                        "app_ids": app_ids,
                        "bundle_id": row.get('data-ds-packageid', str(app_ids[0])) 
                    })
                    
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des bundles : {e}")
            
        return bundles_found

    def has_card(self, app_id: int) -> bool:
        """
        Vérifie si un jeu (app_id) possède des cartes Steam (category id: 29).
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
        except Exception:
            return False