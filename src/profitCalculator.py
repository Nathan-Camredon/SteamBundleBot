from src.game import Game
from src.bundle import Bundle
from typing import Dict

class ProfitCalculator:
    """
    Calcule la rentabilité d'un achat par rapport à la vente des cartes sur le marché Steam.
    """
    
    def calculate_net_fee(self, gross_price: float) -> float:
        """
        Calcule l'argent réel reçu après la taxe de 15% de Steam.
        """
        # Taxe Steam de 15% environ (le vendeur reçoit gross_price / 1.15)
        # Pour des montants très faibles (<0.04), Steam impose un minimum de 0.02,
        # mais la formule /1.15 est une approximation suffisante ici.
        net_price = gross_price / 1.15
        return round(net_price, 2)

    def _calculate_game_ev(self, game: Game, avg_card_price: float) -> float:
        """
        Calcule l'Expected Value (EV) des drops d'un jeu.
        """
        net_card_price = self.calculate_net_fee(avg_card_price)
        return net_card_price * game.drop_available()

    def is_solo_game_profitable(self, game: Game, avg_card_price: float, game_cost: float) -> float:
        """
        Vérifie si un jeu individuel est rentable.
        Renvoie le profit net (positif si rentable).
        """
        ev = self._calculate_game_ev(game, avg_card_price)
        return round(ev - game_cost, 2)

    def is_bundle_profitable(self, bundle: Bundle, dict_card_prices: Dict[int, float]) -> float:
        """
        Calcule le profit total généré par les jeux valides d'un bundle.
        """
        valid_games, _ = bundle.get_valid_games()
        total_ev = 0.0
        
        for game in valid_games:
            avg_price = dict_card_prices.get(game.app_id, 0.0)
            total_ev += self._calculate_game_ev(game, avg_price)
            
        profit = total_ev - bundle.total_price
        return round(profit, 2)
