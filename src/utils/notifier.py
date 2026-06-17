import requests
import os
from typing import List, Dict, Any

class DiscordNotifier:
    """
    Gère l'envoi de notifications via un Webhook Discord.
    C'est la méthode la plus simple et sans authentification lourde (pas besoin de SMTP).
    """
    def __init__(self) -> None:
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    def send_recap(self, profitable_offers: List[Dict[str, Any]]) -> bool:
        """
        Envoie un récapitulatif des offres rentables trouvées aujourd'hui.
        """
        if not self.webhook_url:
            print("⚠️ DISCORD_WEBHOOK_URL manquant dans le .env, notification ignorée.")
            return False

        if not profitable_offers:
            message = "✅ Le scan quotidien est terminé. Aucune offre rentable trouvée aujourd'hui."
            color = 16711680 # Red
        else:
            message = f"🎉 Le scan quotidien est terminé ! **{len(profitable_offers)}** offre(s) rentable(s) trouvée(s) :\n\n"
            for offer in profitable_offers:
                message += f"🔹 **{offer['title']}** ({offer['type']}) -> Profit estimé : **{offer['profit']}€**\n"
            color = 65280 # Green

        payload = {
            "username": "SteamBundleBot",
            "embeds": [
                {
                    "title": "📊 Récapitulatif Quotidien - SteamBundleBot",
                    "description": message,
                    "color": color
                }
            ]
        }

        try:
            headers = {"User-Agent": "SteamBundleBot/1.0"}
            response = requests.post(self.webhook_url, json=payload, headers=headers, timeout=10)
            
            # Si le code HTTP n'est pas 2xx, on lève une exception manuellement pour récupérer le texte de l'erreur
            if not response.ok:
                print(f"❌ Erreur HTTP {response.status_code} de Discord : {response.text}")
                return False
                
            print("📩 Notification Discord envoyée avec succès.")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur de connexion lors de l'envoi Discord : {e}")
            return False

    def send_startup_stats(self, nb_bundles: int, nb_single_games: int) -> bool:
        """
        Envoie un message de statut au démarrage de l'analyse.
        """
        if not self.webhook_url:
            return False
            
        message = f"Le bot commence son scan quotidien !\n\nIl a détecté **{nb_bundles} bundles** et **{nb_single_games} jeux en promotion à l'unité**.\n\n*L'analyse de rentabilité est en cours, merci de patienter...* ⏳"
        
        payload = {
            "username": "SteamBundleBot",
            "embeds": [
                {
                    "title": "🔍 Démarrage de l'analyse",
                    "description": message,
                    "color": 3447003 # Bleu
                }
            ]
        }
        
        try:
            headers = {"User-Agent": "SteamBundleBot/1.0"}
            response = requests.post(self.webhook_url, json=payload, headers=headers, timeout=10)
            if not response.ok:
                print(f"❌ Erreur HTTP {response.status_code} de Discord : {response.text}")
                return False
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur de connexion lors de l'envoi Discord : {e}")
            return False
