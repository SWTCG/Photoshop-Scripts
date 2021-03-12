import os
from collections import OrderedDict

import photoshop.api as ps
from numpy import array

import generate_cards.util.photoshop
from generate_cards.TextSpaceLimit import TextSpaceLimit
from generate_cards.SWTCGCard import SWTCGCard


class Subordinate(SWTCGCard):
    def __init__(self, name, typeline, expansion, side, rarity, speed, power, health, image,
                 game_text=None, flavor_text=None, version=None, icon=True, ppi=600):
        if flavor_text is not None:
            flavor_text = flavor_text.replace("<i>", "%temp%").replace("</i>", "<i>").replace("%temp%", "</i>")
            game_text = f"{game_text}\r<i>{flavor_text}</i>"
        super().__init__(name, typeline, expansion, side, rarity, image, game_text, None, version, icon, ppi)
        self.speed = speed
        self.power = power
        self.health = health

    def wrap_text(self):
        text_limits = [
            TextSpaceLimit(7, 0.89, array([1200, 1155]) * self.ppi / 600),
            TextSpaceLimit(6.5, 0.89, array([1200, 1155]) * self.ppi / 600),
            TextSpaceLimit(6.5, 0.89, array([1270, 1220, 1150]) * self.ppi / 600)
        ]
        text_limits += [TextSpaceLimit(6.5, scale / 100, array([1270, 1220, 1150]) * self.ppi / 600)
                        for scale in range(88, 84, -1)]
        self._wrap_text(text_limits)
        return None

    def write_psd(self, auto_close=False, auto_quit=False):
        app = ps.Application()
        app.load(os.path.join(SWTCGCard.TEMPLATE_DIR, self.template))
        doc = app.activeDocument(self.template)
        self._write_psd(doc)

        layer_dict = generate_cards.util.photoshop.get_layers(doc)

        if len(self.game_text.lines) > 2:
            layer_dict["Game Text"].translate(0, -55 * self.ppi / 600)

        layer_dict["Speed"].textItem.contents = self.speed
        layer_dict["Power"].textItem.contents = self.power
        layer_dict["Health"].textItem.contents = self.health

        if auto_close:
            doc.close(ps.DialogModes.DisplayErrorDialogs)  # Close file without saving
        if auto_quit:
            app.quit()  # Exit Photoshop
        return None
