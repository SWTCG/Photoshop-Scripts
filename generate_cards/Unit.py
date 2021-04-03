import os
import warnings

import photoshop.api as ps
from numpy import array

import generate_cards.util.photoshop as ps_util
from generate_cards.expansions import EXPANSIONS
from generate_cards.TextSpaceLimit import TextSpaceLimit
from generate_cards.SWTCGCard import SWTCGCard


class Unit(SWTCGCard):
    IMAGE_WINDOW = array([69, 252, 1417, 1382])  # (upper-left x, upper-left y, bottom-right x, bottom-right y)
    NAME_WIDTH = 1010
    TYPELINE_WIDTH = 1010

    def __init__(self, name, typeline, expansion, side, rarity, cost, speed, power, health, number, image,
                 game_text=None, flavor_text=None, version=None, icon=True, ppi=600):
        super().__init__(name, typeline, expansion, side, rarity, image, Unit,
                         game_text, flavor_text, version, icon, ppi)
        self.cost = cost
        self.speed = speed
        self.power = power
        self.health = health
        self.number = number

    def wrap_text(self):
        if not self.version:
            pixel_limits_default = array([1025, 1050, 1075, 1088, 1088, 1075, 1055, 1025])
            pixel_limits_small = array([1029, 1050, 1072, 1083, 1093, 1083, 1072, 1050, 1040])
        elif len(self.version) == 1:
            pixel_limits_default = array([1025, 1050, 1075, 1088, 1088, 1075, 1050, 1025])
            pixel_limits_small = array([1029, 1050, 1072, 1083, 1093, 1083, 1072, 1045, 1040])
        else:
            pixel_limits_default = array([1025, 1050, 1075, 1088, 1088, 1075, 1025, 1025])
            pixel_limits_small = array([1029, 1050, 1072, 1083, 1093, 1083, 1072, 1025, 1040])
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

        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter('always')
            self._write_psd(doc)
        if len(warning_list) > 0:
            for w in warning_list:
                warnings.showwarning(w.message, w.category, w.filename, w.lineno, w.file, w.line)
            if export:
                export = False
                warnings.warn(f"{self.expansion}{self.number} {self.name} was not exported due to errors that"
                              f" occurred during the generating process.")

        layer_dict = ps_util.get_layers(doc)

        layer_dict["Build"].textItem.contents = self.cost
        layer_dict["Speed"].textItem.contents = self.speed
        layer_dict["Power"].textItem.contents = self.power
        layer_dict["Health"].textItem.contents = self.health
        if self.number is not None:  # Promo cards may not have a number
            layer_dict["Number"].textItem.contents = "{}/{}".format(self.number, cards_in_set)

        image_count = len([x for x in layer_dict["Card Image"].layers if x.kind not in ps_util.ADJUSTMENT_LAYERS])
        if image_count > 1 and export:
            export = False
            warnings.warn(f"{self.expansion}{self.number} {self.name} was not exported due to "
                          f"multiple image layers in `Card Image`")

        self.save_and_close(doc, save, export, auto_close, auto_quit)
        return len(warning_list)
