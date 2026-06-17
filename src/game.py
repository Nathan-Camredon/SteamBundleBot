class Game:
    """
    Représente un jeu Steam avec ses attributs liés aux cartes.
    """
    def __init__(self, app_id: int, title: str, total_card: int) -> None:
        if total_card < 0:
            raise ValueError("Le nombre total de cartes ne peut pas être négatif.")
            
        self.app_id = app_id
        self.title = title
        self.total_card = total_card

    def drop_available(self) -> int:
        """
        Calcule le nombre de cartes qu'un joueur peut obtenir gratuitement (la moitié du total).
        """
        return self.total_card // 2