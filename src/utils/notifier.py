import requests
import os
from typing import List, Dict, Any
from src.utils.safeLog import redact

MAX_DESCRIPTION: int = 4000  # Limite Discord : 4096 caractères par description d'embed

class DiscordNotifier:
    """
    Gère l'envoi de notifications via un Webhook Discord.
    C'est la méthode la plus simple et sans authentification lourde (pas besoin de SMTP).
    """
    def __init__(self) -> None:
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    def _post(self, payload: Dict[str, Any]) -> bool:
        """
        Envoie un payload au webhook. Renvoie True si Discord répond 2xx.
        """
        try:
            headers = {"User-Agent": "SteamBundleBot/1.0"}
            response = requests.post(self.webhook_url, json=payload, headers=headers, timeout=10)
            if not response.ok:
                print(f"❌ Erreur HTTP {response.status_code} de Discord : {response.text}")
                return False
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur de connexion lors de l'envoi Discord : {redact(e)}")
            return False

    @staticmethod
    def _chunk_lines(header: str, lines: List[str]) -> List[str]:
        """
        Découpe le texte en blocs <= MAX_DESCRIPTION caractères (limite Discord des embeds).
        """
        chunks: List[str] = []
        current = header
        for line in lines:
            if len(current) + len(line) > MAX_DESCRIPTION and current.strip():
                chunks.append(current)
                current = ""
            current += line
        if current.strip():
            chunks.append(current)
        return chunks

    def send_recap(self, profitable_offers: List[Dict[str, Any]]) -> bool:
        """
        Envoie un récapitulatif des offres rentables trouvées aujourd'hui.
        Renvoie True uniquement si tous les messages ont été livrés.
        """
        if not self.webhook_url:
            print("⚠️ DISCORD_WEBHOOK_URL manquant dans le .env, notification ignorée.")
            return False

        if not profitable_offers:
            messages = ["✅ Le scan quotidien est terminé. Aucune offre rentable trouvée aujourd'hui."]
            color = 16711680 # Red
        else:
            header = f"🎉 Le scan quotidien est terminé ! **{len(profitable_offers)}** offre(s) rentable(s) trouvée(s) :\n\n"
            lines = [
                f"🔹 **{offer['title']}** ({offer['type']}) -> Profit estimé : **{offer['profit']}€**\n"
                for offer in profitable_offers
            ]
            messages = self._chunk_lines(header, lines)
            color = 65280 # Green

        all_sent = True
        for message in messages:
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
            all_sent = self._post(payload) and all_sent

        if all_sent:
            print("📩 Notification Discord envoyée avec succès.")
        return all_sent

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
        
        return self._post(payload)
