# class Bundle: Définit ce qu'est un bundle
from .game import Game

class Bundle:
    def __init__(self, bundle_id, name, price, games):
        self.bundle_id = bundle_id
        self.name = name
        self.price = price
        self.games = games if games else []

