from game import Game
from typing import List

class bundle:
    def __init__(self, id, name, total_price, list_of_games: List[Game]):
        self.id = id
        self.name = name
        self.total_price = total_price
        self.list_of_games = list_of_games

    def get_valid_games(self):
        list_valid_games = []
        list_games_not_in_collection = []
        for game in self.list_of_games:
            if game.total_card // 2 > 0:
                list_valid_games.append(game)
            if game.total_card == 0:
                list_games_not_in_collection.append(game)
        
    