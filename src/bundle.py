from src.game import Game
from typing import List, Tuple

class Bundle:
    """
    Représente un bundle Steam contenant plusieurs jeux.
    """
    def __init__(self, bundle_id: str, name: str, total_price: float, list_of_games: List[Game]) -> None:
        if total_price < 0:
            raise ValueError("Le prix d'un bundle ne peut pas être négatif.")
            
        self.id = bundle_id
        self.name = name
        self.total_price = total_price
        self.list_of_games = list_of_games

    def get_valid_games(self) -> Tuple[List[Game], List[Game]]:
        """
        Trie les jeux du bundle.
        Renvoie deux listes:
        - Les jeux valides (ceux qui droppent des cartes, i.e., drop_available > 0).
        - Les jeux qui ne droppent pas de cartes.
        """
        list_valid_games: List[Game] = []
        list_no_card_games: List[Game] = []
        
        for game in self.list_of_games:
            if game.drop_available() > 0:
                list_valid_games.append(game)
            else:
                list_no_card_games.append(game)
                
        return list_valid_games, list_no_card_games