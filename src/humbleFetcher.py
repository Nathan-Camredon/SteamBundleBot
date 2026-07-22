import os
import requests
import cloudscraper
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
        self.scraper = cloudscraper.create_scraper()
        self.steam_apps_cache: Dict[str, int] = {}
        self._load_steam_apps()

    def _load_steam_apps(self) -> None:
        """
        Charge la liste de toutes les apps Steam pour résoudre les noms en app_id.
        Utilise IStoreService/GetAppList/v1/ avec pagination.
        """
        api_key = os.getenv("STEAM_API_KEY")
        if not api_key:
            print("⚠️ STEAM_API_KEY manquante, impossible de charger le cache Steam pour Humble Bundle.")
            return
            
        print("🔄 Chargement du cache des applications Steam (HumbleFetcher)...")
        url = "https://api.steampowered.com/IStoreService/GetAppList/v1/"
        last_appid = 0
        has_more = True
        
        try:
            while has_more:
                params = {
                    "key": api_key,
                    "max_results": 50000,
                    "last_appid": last_appid,
                    "include_games": True,
                    "include_dlc": False,
                    "include_hardware": False,
                    "include_software": False,
                    "include_videos": False
                }
                response = requests.get(url, params=params, timeout=15)
                response.raise_for_status()
                data = response.json().get("response", {})
                apps = data.get("apps", [])
                
                for app in apps:
                    if "name" in app and "appid" in app:
                        self.steam_apps_cache[app["name"].lower()] = app["appid"]
                        
                has_more = data.get("have_more_results", False)
                last_appid = data.get("last_appid", last_appid)
                time.sleep(0.5) # Anti rate-limit Steam
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
        Récupère les bundles actifs sur Humble Bundle et extrait les Tiers comme des bundles distincts.
        """
        bundles_found = []
        try:
            response = self.scraper.get(self.url_bundles, headers=self.headers, timeout=15)
            if response.status_code == 403:
                print("⚠️ Accès refusé à Humble Bundle (Cloudflare/403).")
                return bundles_found
                
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 1. Extraire les URLs des bundles de jeux depuis la page d'accueil
            script_landing = soup.find('script', id='landingPage-json-data')
            if not script_landing or not script_landing.string:
                print("⚠️ Impossible de trouver landingPage-json-data sur Humble Bundle.")
                return bundles_found
                
            data = json.loads(script_landing.string)
            games_data = data.get('data', {}).get('games', {})
            mosaics = games_data.get('mosaic', [])
            if not mosaics:
                print("⚠️ Aucun mosaic de jeux trouvé sur Humble Bundle.")
                return bundles_found
                
            products = mosaics[0].get('products', [])
            bundle_urls = ["https://www.humblebundle.com" + p['product_url'] for p in products if 'product_url' in p]
            
            # 2. Explorer chaque bundle pour en extraire les Tiers
            for bundle_url in bundle_urls:
                try:
                    b_response = self.scraper.get(bundle_url, headers=self.headers, timeout=15)
                    b_response.raise_for_status()
                    b_soup = BeautifulSoup(b_response.text, 'html.parser')
                    b_script = b_soup.find('script', id='webpack-bundle-page-data')
                    if not b_script or not b_script.string:
                        continue
                        
                    b_data = json.loads(b_script.string).get('bundleData', {})
                    human_name = b_data.get('basic_data', {}).get('human_name', 'Humble Bundle')
                    machine_name = b_data.get('machine_name', 'unknown_bundle')
                    
                    tier_display = b_data.get('tier_display_data', {})
                    tier_pricing = b_data.get('tier_pricing_data', {})
                    tier_items = b_data.get('tier_item_data', {})
                    
                    for identifier, display_data in tier_display.items():
                        # Récupérer le prix
                        price_data = tier_pricing.get(identifier, {})
                        amount = price_data.get('price|money', {}).get('amount')
                        if amount is None:
                            continue
                        price = float(amount)
                        
                        # Récupérer les jeux du Tier
                        machine_names = display_data.get('tier_item_machine_names', [])
                        app_ids = []
                        for m_name in machine_names:
                            item_info = tier_items.get(m_name, {})
                            game_title = item_info.get('human_name', '')
                            
                            app_id = self._resolve_steam_app_id(game_title)
                            if app_id:
                                app_ids.append(app_id)
                        
                        if app_ids:
                            bundles_found.append({
                                "name": f"{human_name} ({identifier})",
                                "url": bundle_url,
                                "price": price,
                                "app_ids": app_ids,
                                "bundle_id": f"hb_{machine_name}_{identifier}"
                            })
                            
                    time.sleep(1) # Anti rate-limit Humble
                except Exception as e:
                    print(f"⚠️ Erreur lors du parsing du bundle {bundle_url}: {e}")
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur réseau lors de la récupération des bundles Humble : {e}")
        except Exception as e:
            print(f"❌ Erreur inattendue : {e}")

        return bundles_found
