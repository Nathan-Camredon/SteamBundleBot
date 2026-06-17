import sqlite3
import os
from typing import List, Tuple, Optional
from src.game import Game
from src.bundle import Bundle

class DatabaseManager:
    """
    Gère la persistance des données via SQLite.
    """
    def __init__(self, db_path: str = "data/steambundlebot.db") -> None:
        # S'assure que le dossier data/ existe
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.setup_tables()

    def _get_connection(self) -> sqlite3.Connection:
        """
        Ouvre et renvoie une connexion à la base de données.
        """
        return sqlite3.connect(self.db_path)

    def setup_tables(self) -> None:
        """
        Initialise les tables si elles n'existent pas.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Table pour les jeux avec cartes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS games_with_cards (
                    app_id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    total_card INTEGER NOT NULL
                )
            ''')
            
            # Table pour les bundles contenant des jeux avec cartes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bundles_with_cards (
                    bundle_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    total_price REAL NOT NULL
                )
            ''')
            
            # Table pour stocker les offres rentables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS profitable_offers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    offer_type TEXT NOT NULL, -- 'game' ou 'bundle'
                    item_id TEXT NOT NULL,
                    profit REAL NOT NULL,
                    date_found TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def save_game(self, game: Game) -> None:
        """
        Sauvegarde un jeu possédant des cartes.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO games_with_cards (app_id, title, total_card)
                VALUES (?, ?, ?)
            ''', (game.app_id, game.title, game.total_card))
            conn.commit()

    def save_bundle(self, bundle: Bundle) -> None:
        """
        Sauvegarde un bundle contenant des jeux valides.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO bundles_with_cards (bundle_id, name, total_price)
                VALUES (?, ?, ?)
            ''', (bundle.id, bundle.name, bundle.total_price))
            conn.commit()

    def save_profitable_offer(self, offer_type: str, item_id: str, profit: float) -> None:
        """
        Sauvegarde une offre rentable trouvée.
        offer_type doit être 'game' ou 'bundle'.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO profitable_offers (offer_type, item_id, profit)
                VALUES (?, ?, ?)
            ''', (offer_type, str(item_id), profit))
            conn.commit()

    def is_game_scanned(self, app_id: int) -> bool:
        """
        Vérifie si un jeu est déjà dans la base.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM games_with_cards WHERE app_id = ?', (app_id,))
            return cursor.fetchone() is not None
