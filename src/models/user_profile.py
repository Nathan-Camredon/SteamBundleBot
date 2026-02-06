# class UserProfile: Définit l'utilisateur

class UserProfile:
    def __init__(self, json):
        self.owned_games = set()
    
    def add_game(self, game_id):
        self.owned_games.add(game_id)

    def has_game(self, game_id):
        return game_id in self.owned_games
