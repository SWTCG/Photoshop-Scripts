import os

import photoshop.api as ps
from numpy import array

import generate_cards.util.photoshop
from generate_cards.SWTCGCard import SWTCGCard


class Subordinate(SWTCGCard):
    def __init__(self, name, typeline, expansion, side, rarity, speed, power, health, image,
                 game_text=None, flavor_text=None, version=None, icon=True, ppi=600):
        super().__init__(name, typeline, expansion, side, rarity, image, game_text, flavor_text, version, icon, ppi)
        self.speed = speed
        self.power = power
        self.health = health

    def wrap_text(self):
        line_lengths = {
            7: array([1265, 1200, 1165]) * self.ppi / 600,
            6.5: array([1265, 1200, 1165]) * self.ppi / 600
        }
        self._wrap_text(line_lengths)
        return None

    def write_psd(self, auto_close=False, auto_quit=False):
        app = ps.Application()
        app.load(os.path.join(SWTCGCard.TEMPLATE_DIR, self.template))
        doc = app.activeDocument(self.template)
        self._write_psd(doc)

        layer_dict = generate_cards.util.photoshop.get_layers(doc)

        layer_dict["Speed"].textItem.contents = self.speed
        layer_dict["Power"].textItem.contents = self.power
        layer_dict["Health"].textItem.contents = self.health

        if auto_close:
            doc.close(ps.DialogModes.DisplayErrorDialogs)  # Close file without saving
        if auto_quit:
            app.quit()  # Exit Photoshop
        return None
