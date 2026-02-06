import requests
import os

class SteamClient:
    """
    Gère les communications avec l'API Web de Steam.
    """
    def __init__(self):
        # TA MISSION : Récupérer la clé API depuis les variables d'environnement
        # Indice : os.getenv("NOM_DE_LA_VAR")
        self.api_key = ...
        self.base_url = "http://api.steampowered.com"

    def get_owned_games(self, steam_id):
        """
        Récupère la liste des jeux possédés par un utilisateur.
        Documentation : IPlayerService/GetOwnedGames/v0001/
        """
        # TA MISSION :
        # 1. Construire l'URL (self.base_url + endpoint...)
        # 2. Préparer les paramètres (key, steamid, format='json', include_appinfo=1)
        # 3. Envoyer la requête (requests.get)
        # 4. Retourner la liste des jeux (response.json()['response']['games'])
        pass
