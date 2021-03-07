import os

import photoshop.api as ps
from numpy import array

import generate_cards.util.photoshop
from generate_cards.expansions import EXPANSIONS
from generate_cards.SWTCGCard import SWTCGCard


class NonUnit(SWTCGCard):
    def __init__(self, name, typeline, expansion, side, rarity, number, image,
                 cost=None, game_text=None, flavor_text=None, version=None, icon=True, ppi=600):
        super().__init__(name, typeline, expansion, side, rarity, image, game_text, flavor_text, version, icon, ppi)
        self.number = number
        self.cost = cost
        self.version = version

    def wrap_text(self):
        line_lengths = {
            7: array([1650, 1675, 1685, 1675, 1650]) * self.ppi / 600,
            6.5: array([1650, 1680, 1690, 1680, 1660]) * self.ppi / 600
        }
        self._wrap_text(line_lengths)
        return None

    def write_psd(self, auto_close=False, auto_quit=False):
        cards_in_set = EXPANSIONS[self.expansion].size

        app = ps.Application()
        app.load(os.path.join(SWTCGCard.TEMPLATE_DIR, self.template))
        doc = app.activeDocument(self.template)
        self._write_psd(doc)

        layer_dict = generate_cards.util.photoshop.get_layers(doc)

        if self.cost is not None:
            layer_dict["Build"].textItem.contents = self.cost
        if self.number is not None:  # Promo cards may not have a number
            layer_dict["Number"].textItem.contents = "{}/{}".format(self.number, cards_in_set)

        if auto_close:
            doc.close(ps.DialogModes.DisplayErrorDialogs)  # Close file without saving
        if auto_quit:
            app.quit()  # Exit Photoshop
        return None
