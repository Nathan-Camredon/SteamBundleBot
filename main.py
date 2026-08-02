import os
import time
import schedule
from dotenv import load_dotenv

from src.storeFetcher import StoreFetcher
from src.humbleFetcher import HumbleFetcher
from src.marketFetcher import MarketFetcher
from src.profitCalculator import ProfitCalculator
from src.databaseManager import DatabaseManager
from src.game import Game
from src.bundle import Bundle
from src.utils.notifier import DiscordNotifier

class SteamScannerBot:
    """
    Orchestrateur principal du bot SteamBundleBot.
    """
    def __init__(self) -> None:
        self.store_fetcher = StoreFetcher()
        self.humble_fetcher = HumbleFetcher()
        self.market_fetcher = MarketFetcher()
        self.calculator = ProfitCalculator()
        self.db = DatabaseManager()
        self.notifier = DiscordNotifier()

    def run_daily_batch(self) -> None:
        """
        Exécute le workflow principal:
        1. Fetch jeux possédés (pour les exclure)
        2. Fetch bundles réels
        3. Extract games & check trading cards
        4. Fetch market prices & Calculate profit
        5. Save & Notify profitable offers
        """
        print("\n🚀 Lancement du Batch SteamScannerBot...")
        
        steam_api_key = os.getenv("STEAM_API_KEY", "")
        steam_id = os.getenv("STEAM_ID", "")
        
        owned_games = self.store_fetcher.get_owned_games(steam_api_key, steam_id)
        print(f"✅ {len(owned_games)} jeux possédés récupérés (seront exclus de l'analyse).")

        print("🔍 Récupération des jeux uniques en promotion sur le store...")
        single_games_data = self.store_fetcher.fetch_single_games()
        
        print("🔍 Récupération des bundles sur le store...")
        bundles_data = self.store_fetcher.fetch_bundles()
        
        print("🔍 Récupération des bundles sur Humble Bundle...")
        humble_bundles = self.humble_fetcher.fetch_bundles()
        bundles_data.extend(humble_bundles)
        
        nb_bundles = len(bundles_data)
        nb_single_games = len(single_games_data)
        
        print(f"📦 {nb_bundles} bundles et {nb_single_games} jeux uniques récupérés.")
        self.notifier.send_startup_stats(nb_bundles, nb_single_games)
        
        profitable_offers = []

        # --- 1. Analyse des jeux uniques ---
        for g_data in single_games_data:
            app_id = g_data["app_id"]
            name = g_data["name"]
            price = g_data["price"]
            url = g_data["url"]
            
            print(f"\n🎮 Analyse du Jeu: {name} (Prix d'achat: {price}€)")
            
            if app_id in owned_games:
                print(f"   ⏩ Jeu {app_id} ignoré (déjà possédé).")
                continue
                
            if not self.store_fetcher.has_card(app_id):
                print(f"   ❌ {name} n'a pas de cartes Steam.")
                continue
                
            print(f"   🃏 {name} a des cartes.")
            avg_price, total_cards = self.market_fetcher.get_average_card_price(app_id)
            game = Game(app_id=app_id, title=name, total_card=total_cards)
            print(f"      Prix moyen carte: {avg_price}€ (Total cartes: {total_cards})")
            
            profit = self.calculator.is_solo_game_profitable(game, avg_price, price)
            roi = ((profit + price) / price) * 100 if price > 0 else 100
            
            if profit > 0 or roi >= 95:
                if self.db.is_offer_notified(str(app_id)):
                    print(f"   💸 JEU ({profit}€ / ROI {roi:.1f}%) déjà notifié précédemment.")
                else:
                    if profit > 0:
                        print(f"   💰 JEU RENTABLE ! Profit estimé net : {profit}€ (ROI {roi:.1f}%)")
                        offer_type = "Jeu Unique"
                    else:
                        print(f"   💎 JEU PRESQUE GRATUIT ! Profit : {profit}€ (ROI {roi:.1f}%)")
                        offer_type = "Jeu Unique (Presque Gratuit)"
                    
                    self.db.save_profitable_offer("Game", str(app_id), profit)
                    profitable_offers.append({"title": name, "type": offer_type, "profit": profit})
            else:
                print(f"   📉 Jeu Non rentable (Déficit de {abs(profit)}€, ROI {roi:.1f}%)")

        # --- 2. Analyse des bundles ---
        for b_data in bundles_data:
            bundle_id = b_data["bundle_id"]
            name = b_data["name"]
            price = b_data["price"]
            app_ids = b_data["app_ids"]
            
            print(f"\n📦 Analyse du Bundle: {name} (Prix d'achat: {price}€)")
            
            games = []
            card_prices = {}
            for app_id in app_ids:
                if app_id in owned_games:
                    print(f"   ⏩ Jeu {app_id} ignoré (déjà possédé).")
                    continue
                
                if self.store_fetcher.has_card(app_id):
                    print(f"   🃏 App_{app_id} a des cartes.")
                    avg_price, total_cards = self.market_fetcher.get_average_card_price(app_id)
                    game = Game(app_id=app_id, title=f"App_{app_id}", total_card=total_cards)
                    games.append(game)
                    card_prices[game.app_id] = avg_price
                    print(f"      Prix moyen carte App_{app_id}: {avg_price}€ (Total cartes: {total_cards})")
                else:
                    print(f"   ❌ App_{app_id} n'a pas de cartes.")

            if not games:
                print(f"   📉 Bundle '{name}' ignoré (aucun jeu valide non-possédé).")
                continue

            bundle = Bundle(bundle_id=bundle_id, name=name, total_price=price, list_of_games=games)
            
            valid_games_list = bundle.get_valid_games()[0]
            if not valid_games_list:
                print(f"   📉 Bundle '{name}' ignoré (jeux valides mais aucun drop disponible).")
                continue
                
            profit = self.calculator.is_bundle_profitable(bundle, card_prices)
            roi = ((profit + price) / price) * 100 if price > 0 else 100
            
            if profit > 0 or roi >= 95:
                if self.db.is_offer_notified(bundle_id):
                    print(f"   💸 BUNDLE ({profit}€ / ROI {roi:.1f}%) déjà notifié précédemment.")
                else:
                    if profit > 0:
                        print(f"   💰 BUNDLE RENTABLE ! Profit estimé net : {profit}€ (ROI {roi:.1f}%)")
                        offer_type = "Bundle"
                    else:
                        print(f"   💎 BUNDLE PRESQUE GRATUIT ! Profit : {profit}€ (ROI {roi:.1f}%)")
                        offer_type = "Bundle (Presque Gratuit)"
                        
                    self.db.save_bundle(bundle)
                    self.db.save_profitable_offer("bundle", bundle_id, profit)
                    profitable_offers.append({"title": name, "type": offer_type, "profit": profit})
            else:
                print(f"   📉 Bundle Non rentable (Déficit de {abs(profit)}€, ROI {roi:.1f}%)")

        # Envoi de la notification
        self.notifier.send_recap(profitable_offers)
        print("✅ Batch terminé.")


def job():
    bot = SteamScannerBot()
    bot.run_daily_batch()

def main() -> None:
    load_dotenv()
    print("🤖 Bot démarré. Planification du job tous les jours à 21h00.")
    # Planification
    schedule.every().day.at("21:00").do(job)
    
    # Exécution immédiate au lancement du script
    print("⚙️ Exécution immédiate du batch à l'initialisation...")
    job()
    print("\n⏳ En attente des prochaines exécutions programmées... (Ctrl+C pour quitter)")

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
