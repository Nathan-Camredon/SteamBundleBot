import json
import os

class JsonStorage:
    """
    Gère la persistance des données en JSON.
    """
    def __init__(self, data_folder="data"):
        self.data_folder = data_folder
        # S'assure que le dossier existe
        os.makedirs(self.data_folder, exist_ok=True)

    def save(self, filename: str, data):
        """Sauvegarde les données dans un fichier JSON."""
        file_path = os.path.join(self.data_folder, filename)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"💾 Sauvegarde réussie : {file_path}")
            return True
        except Exception as e:
            print(f"❌ Erreur sauvegarde {filename} : {e}")
            return False

    def load(self, filename: str):
        """Charge les données depuis un fichier JSON."""
        file_path = os.path.join(self.data_folder, filename)
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Erreur lecture {filename} : {e}")
            return None
