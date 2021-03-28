import os
from collections import OrderedDict

import photoshop.api as ps
from numpy import array

import generate_cards.util.photoshop
from generate_cards.TextSpaceLimit import TextSpaceLimit
from generate_cards.SWTCGCard import SWTCGCard


class Subordinate(SWTCGCard):
    IMAGE_WINDOW = array([93, 109, 1394, 1539])
    NAME_WIDTH = 1140
    TYPELINE_WIDTH = 1235

    def __init__(self, name, typeline, expansion, side, rarity, speed, power, health, image,
                 game_text=None, flavor_text=None, version=None, icon=True, ppi=600):
        if flavor_text is not None or "":
            flavor_text = flavor_text.replace("<i>", "%temp%").replace("</i>", "<i>").replace("%temp%", "</i>")
            game_text = f"{game_text}\r<i>{flavor_text}</i>"
        super().__init__(name, typeline, expansion, side, rarity, image, Subordinate, game_text,
                         None, version, icon, ppi)
        self.speed = speed
        self.power = power
        self.health = health

    def wrap_text(self):
        if not self.version:
            pixel_limits_2lines = array([1220, 1155])
            pixel_limits_3lines = array([1270, 1220, 1150])
        elif len(self.version) == 1:
            pixel_limits_2lines = array([1200, 1155])
            pixel_limits_3lines = array([1270, 1200, 1150])
        else:
            pixel_limits_2lines = array([1150, 1150])
            pixel_limits_3lines = array([1270, 1150, 1150])
        text_limits = [
            TextSpaceLimit(7, 0.89, pixel_limits_2lines * self.ppi / 600),
            TextSpaceLimit(6.5, 0.89, pixel_limits_2lines * self.ppi / 600),
            TextSpaceLimit(6.5, 0.89, pixel_limits_3lines * self.ppi / 600)
        ]
        text_limits += [TextSpaceLimit(6.5, scale / 100, pixel_limits_3lines * self.ppi / 600)
                        for scale in range(88, 74, -1)]
        self._wrap_text(text_limits)
        return None

    def write_psd(self, save=None, export=None, auto_close=False, auto_quit=False):
        app = ps.Application()
        app.load(os.path.join(SWTCGCard.TEMPLATE_DIR, self.template))
        doc = app.activeDocument(self.template)
        self._write_psd(doc)

        layer_dict = generate_cards.util.photoshop.get_layers(doc)

        if len(self.game_text.lines) > 2:
            y = 1813 * self.ppi / 600 - layer_dict["Game Text"].textItem.position[1]
        else:
            y = 1868 * self.ppi / 600 - layer_dict["Game Text"].textItem.position[1]
        layer_dict["Game Text"].translate(0, y)

        layer_dict["Speed"].textItem.contents = self.speed
        layer_dict["Power"].textItem.contents = self.power
        layer_dict["Health"].textItem.contents = self.health

        self.save_and_close(doc, save, export, auto_close, auto_quit)
        return None
