import requests
import os



class SteamClient:
    """
    Gère les communications avec l'API Web de Steam.
    """
    def __init__(self):
        self.api_key = os.getenv("STEAM_API_KEY")
        self.base_url = "http://api.steampowered.com"

    def get_owned_games(self, steam_id):
        """
        Récupère la liste des jeux possédés par un utilisateur.
        Documentation : IPlayerService/GetOwnedGames/v0001/
        """
        url = self.base_url + "/IPlayerService/GetOwnedGames/v0001/"
        
        params = {
            'key' : self.api_key,
            'steamid' : steam_id,
            'format' : 'json',
            'include_appinfo': True,
            'include_played_free_games' :  True
        }
        
        response = requests.get(url, params=params)
        return response.json()['response']['games']

if __name__ == "__main__":
    from dotenv import load_dotenv
    import sys
    
    # Ajoute le dossier racine au path pour pouvoir importer src.utils
    sys.path.append(os.getcwd())
    from src.utils.database import JsonStorage

    load_dotenv()
    
    # Test rapide
    # Ton ID Steam doit être dans le .env sous STEAM_ID, sinon remplace le ici
    my_steam_id = os.getenv("STEAM_ID")
    
    if not my_steam_id:
        print("Erreur: Ajoute STEAM_ID=ton_id_steam dans le fichier .env pour tester !")
    else:
        client = SteamClient()
        storage = JsonStorage() # On initialise le stockage
        
        try:
            games = client.get_owned_games(my_steam_id)
            print(f"✅ Succès ! {len(games)} jeux trouvés sur le compte.")
            if games:
                print(f"Premier jeu trouvé : {games[0]['name']} (ID: {games[0]['appid']})")
                
                # Sauvegarde dans data/steam_library.json
                storage.save("steam_library.json", games)
                
        except Exception as e:
            print(f"❌ Erreur : {e}")
