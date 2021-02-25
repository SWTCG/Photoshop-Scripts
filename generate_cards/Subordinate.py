from generate_cards.SWTCGCard import SWTCGCard


class Subordinate(SWTCGCard):
    def __init__(self, name, typeline, expansion, side, rarity, speed, power, health,
                 game_text=None, flavor_text=None, version=None, ppi=600):
        super().__init__(name, typeline, expansion, side, rarity, ppi)
        self.speed = speed
        self.power = power
        self.health = health

        self.version = version
