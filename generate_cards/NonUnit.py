import os

import photoshop.api as ps
from numpy import array

import generate_cards.util.photoshop
from generate_cards.expansions import EXPANSIONS
from generate_cards.TextSpaceLimit import TextSpaceLimit
from generate_cards.SWTCGCard import SWTCGCard


class NonUnit(SWTCGCard):
    IMAGE_WINDOW = array([115, 233, 2006, 1087])
    NAME_WIDTH = 1470
    TYPELINE_WIDTH = 1470

    def __init__(self, name, typeline, expansion, side, rarity, number, image,
                 cost=None, game_text=None, flavor_text=None, version=None, icon=True, ppi=600):
        if cost == "":
            cost = None
        super().__init__(name, typeline, expansion, side, rarity, image, NonUnit,
                         game_text, flavor_text, version, icon, ppi)
        self.number = number
        self.cost = cost

    def wrap_text(self):
        if not self.version:
            pixel_limits_default = array([1661, 1675, 1685, 1675, 1650])
            pixel_limits_small = array([1661, 1680, 1690, 1680, 1660])
        elif len(self.version) == 1:
            pixel_limits_default = array([1661, 1675, 1685, 1650, 1650])
            pixel_limits_small = array([1661, 1680, 1690, 1680, 1655])
        else:
            pixel_limits_default = array([1661, 1675, 1685, 1630, 1630])
            pixel_limits_small = array([1661, 1680, 1690, 1645, 1635])
        text_limits = [
            TextSpaceLimit(7, 0.89, pixel_limits_default * self.ppi / 600),
            TextSpaceLimit(6.5, 0.89, pixel_limits_small * self.ppi / 600)
        ]
        text_limits += [TextSpaceLimit(6.5, scale / 100, pixel_limits_small * self.ppi / 600)
                        for scale in range(88, 74, -1)]
        self._wrap_text(text_limits)
        return None

    def write_psd(self, save=None, export=None, auto_close=False, auto_quit=False):
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

        self.save_and_close(doc, save, export, auto_close, auto_quit)
        return None
