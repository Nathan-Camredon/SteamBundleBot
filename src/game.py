class Game:
    def __init__(self, app_id, tittle, total_card):
        self.app_id = app_id
        self.tittle = tittle
        self.total_card = total_card

    def drop_available(self):
        return self.total_card // 2