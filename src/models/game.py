# class Game: Définit ce qu'est un jeu

class Game:
    def __init__(self, app_id, name, price, card_price, drop_count):
        self.app_id = app_id
        self.name = name
        self.price = price           # Prix du jeu
        self.card_price = card_price # Prix moyen d'une carte
        self.drop_count = drop_count # Nombre de cartes récupérées

    def get_card_value(self):
        return self.card_price * self.drop_count

     