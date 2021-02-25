from generate_cards.SWTCGCard import SWTCGCard


class NonUnit(SWTCGCard):
    def __init__(self, name, typeline, expansion, side, rarity, number,
                 cost=None, game_text=None, flavor_text=None, version=None, ppi=600):
        super().__init__(name, typeline, expansion, side, rarity, ppi)
        self.number = number

        self.cost = cost
        self.version = version
