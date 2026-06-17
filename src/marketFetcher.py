import requests
import time
from typing import Optional

class MarketFetcher:
    """
    Récupère les prix des objets sur le Steam Community Market.
    """
    def __init__(self) -> None:
        self.base_url: str = "https://steamcommunity.com/market/search/render/"
        self.headers = {"User-Agent": "SteamBundleBot/1.0"}
        
    def _sleep_to_prevent_ban(self) -> None:
        """Délai de sécurité pour éviter le rate-limit du Market."""
        time.sleep(3)

    def get_average_card_price(self, app_id: int, card_name: str = "") -> float:
        """
        Recherche le prix moyen des cartes pour un jeu donné en utilisant l'API search du Market.
        """
        self._sleep_to_prevent_ban()
        try:
            params = {
                "appid": 753, # Steam inventory app
                "category_753_Game[]": f"tag_app_{app_id}",
                "category_753_item_class[]": "tag_item_class_2", # Trading cards
                "norender": 1,
                "count": 5
            }
            if card_name:
                params["query"] = card_name

            response = requests.get(self.base_url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = data.get("results", [])
            if not results:
                return 0.0
                
            total_price = 0.0
            valid_items = 0
            for item in results:
                # sell_price_text "0,04€" -> float
                price_text = item.get("sell_price_text", "0")
                price_text = price_text.replace("€", "").replace("$", "").replace(",", ".").strip()
                try:
                    price = float(price_text)
                    total_price += price
                    valid_items += 1
                except ValueError:
                    continue
                    
            if valid_items == 0:
                return 0.0
                
            return round(total_price / valid_items, 2)

        except Exception as e:
            print(f"❌ Erreur lors de la récupération du prix marché pour app_id {app_id}: {e}")
            return 0.0
