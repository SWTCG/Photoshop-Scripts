class Symbol:
    def __init__(self, string, width, height, replacement, layer_name=None,
                 ppi=600, font_size=7.0, baseline_shift=0, right_kern={}):
        """
        :param string:         The character string representing the symbol, e.g. '->' for the
                               activated ability arrow.
        :param width:          The width, in pixels, of the symbol image.
        :param height:         The height, in pixels, of the symbol image.
        :param replacement:    The character that replaces the `string` representation in the actual
                               text written to the PSD.
        :param layer_name:     The name of the PSD layer holding the symbol image.
        :param ppi:            The pixels per inch at which the `width` and `height` are valid.
        :param font_size:      The font size, in points, at which the `width` and `height` are valid.
        :param baseline_shift: The amount, in pixels, to shift the symbol image above the text
                               baseline. Negative values shift below the baseline.
        :param right_kern:     A dictionary defining how many pixels to shift the text to the right of
                               the symbol if it is followed by any of the characters in the dictionary.
                               Positive values shift the text to the right, while negative shift to the
                               left.
        """
        self.string = string
        self.width = width
        self.height = height
        self.replacement = replacement
        self.ppi = ppi
        self.font_size = font_size
        self.layer_name = layer_name
        self.baseline_shift = baseline_shift
        self.right_kern = right_kern

    def scale(self, ppi, font_size):
        scale_factor = ppi / self.ppi * font_size / self.font_size
        self.width = round(self.width * scale_factor)
        self.height = round(self.height * scale_factor)
        self.baseline_shift = round(self.baseline_shift * scale_factor)
        self.right_kern = {k: round(self.right_kern[k] * scale_factor) for k in self.right_kern.keys()}
        return None


class Tap(Symbol):
    def __init__(self, ppi=600, font_size=7):
        super().__init__(string="[tap]", width=46, height=46, replacement=" ", layer_name="Tap Symbol", ppi=600,
                         font_size=7, baseline_shift=-3, right_kern={',': -3})
        self.scale(ppi, font_size)


class Pilot(Symbol):
    def __init__(self, ppi=600, font_size=7):
        super().__init__(string="[Pilot]", width=54, height=45, replacement=" ", layer_name="Pilot Symbol", ppi=600,
                         font_size=6.5, baseline_shift=-1)
        self.scale(ppi, font_size)


class Arrow(Symbol):
    def __init__(self, ppi=600, font_size=7):
        # \u00a7 is the unicode section symbol (§). \uf08e is unicode for the Wingdings 3 arrow.
        # The arrow symbol is 8.35 pt Dax Regular text copyright for 7 pt game text
        super().__init__(string="->", width=85, height=29, replacement=" ", layer_name="Activated Ability Arrow",
                         ppi=600, font_size=7, baseline_shift=4)
        self.scale(ppi, font_size)


class Bullet(Symbol):
    def __init__(self, ppi=600, font_size=7):
        super().__init__(string="\u2022", width=13, height=13, replacement=" ", layer_name="Bullet Point", ppi=600,
                         font_size=6.5, baseline_shift=13)
        self.scale(ppi, font_size)


SYMBOLS = [Tap, Pilot, Arrow, Bullet]
