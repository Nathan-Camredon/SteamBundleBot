import aiohttp
import asyncio
from typing import Optional

class MarketFetcher:
    """
    Récupère les prix des objets sur le Steam Community Market.
    """
    def __init__(self) -> None:
        self.base_url: str = "https://steamcommunity.com/market/search/render/"
        self.headers = {"User-Agent": "SteamBundleBot/1.0"}

    async def get_average_card_price(self, session: aiohttp.ClientSession, app_id: int, card_name: str = "") -> tuple[float, int]:
        """
        Recherche le prix moyen des cartes pour un jeu donné en utilisant l'API search du Market.
        """
        # Délai de sécurité pour éviter le rate-limit du Market.
        await asyncio.sleep(1.5)
        try:
            params = {
                "appid": 753, # Steam inventory app
                "category_753_Game[]": f"tag_app_{app_id}",
                "category_753_item_class[]": "tag_item_class_2", # Trading cards
                "category_753_cardborder[]": "tag_cardborder_0", # Normal border (exclut les cartes Foil)
                "norender": 1,
                "count": 5
            }
            if card_name:
                params["query"] = card_name

            async with session.get(self.base_url, headers=self.headers, params=params, timeout=10) as response:
                response.raise_for_status()
                data = await response.json()
            
            total_count = data.get("total_count", 0)
            results = data.get("results", [])
            if not results:
                return 0.0, 0
                
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
                return 0.0, 0
                
            return round(total_price / valid_items, 2), total_count

        except Exception as e:
            print(f"❌ Erreur lors de la récupération du prix marché pour app_id {app_id}: {e}")
            return 0.0, 0
