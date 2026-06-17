import requests
import time

class StoreFetcher:
    def __init__(self):
        self.urlStore = "https://store.steampowered.com/api/featuredcategories"
        self.urlapp = "https://store.steampowered.com/api/appdetails"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    def fetchStore(self):
        try:
            response = requests.get(self.urlStore, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête : {e}")
            return None
        

    def HasCard(self):
        time.sleep(2)
    