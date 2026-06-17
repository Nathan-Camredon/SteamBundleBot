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
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            print("📩 Notification Discord envoyée avec succès.")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur lors de l'envoi Discord : {e}")
            return False
