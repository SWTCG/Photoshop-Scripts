from numpy import inf
from PIL import ImageFont

import generate_cards.symbols as symbols


class CardText:
    FORMATTERS = ["<i>", "</i>"]

    def __init__(self, text, font, font_size, **kwargs):
        if text is not None:
            text = text.replace(" | ", "\r")
        self.text = text
        self.font = font
        self.font_size = font_size
        self.__dict__.update(kwargs)

        self.lines = text.split("\r") if text is not None else []

    def text_width(self, text, ppi, scale=0.89):
        syms = [s(ppi, self.font_size) for s in symbols.SYMBOLS]
        symbol_counts = {symbol.string: text.count(symbol.string) for symbol in syms}
        kern_adjustment = 0
        for symbol in syms:
            # Search the text for any kern-able characters and apply the necessary kern adjustment
            pos = self.text_positions(text, symbol.string)
            temp_text = text.replace(symbol.string, "\0")
            pos = [i for i in pos if i < len(temp_text) - 1]
            kern_adjustment += sum([
                symbol.right_kern[temp_text[i + 1]] for i in pos
                if temp_text[i + 1] in symbol.right_kern.keys()
            ])

            text = text.replace(symbol.string, "")

        for f in self.FORMATTERS:
            text = text.replace(f, "")
        font_size = int(round(self.font_size * ppi, 0))
        width = ImageFont.truetype(self.font, font_size).getsize(text, features=['kern'])[0] / 72
        width *= scale
        for symbol in syms:
            width += symbol_counts[symbol.string] * symbol.width
        return width + kern_adjustment

    def line_height(self, ppi):
        return self.font_size * 10 * ppi / 600

    def position_symbol(self, symbol, ppi, align='left'):
        if align == 1:
            align = 'left'
        elif align == 2:
            align = 'center'
        elif align == 3:
            align = 'right'

        shifts = []
        line_count = 0
        for line in self.lines:
            line_len = self.text_width(line, ppi)
            substrings = line.split(symbol.string)
            for i in range(len(substrings) - 1):
                x_shift = self.text_width(symbol.string.join(substrings[0:i + 1]), ppi)
                if align.lower() == 'left':
                    pass
                elif align.lower() == 'center':
                    x_shift -= line_len / 2
                elif align.lower() == 'right':
                    x_shift -= line_len
                else:
                    raise Exception("Invalid value for `align`: {}".format(align))
                y_shift = line_count * self.line_height(ppi) - (symbol.height + symbol.baseline_shift)
                shifts.append((x_shift, y_shift))
            line_count += 1
        string_positions = self.psd_text_positions(self.text, symbol.string)
        return shifts, string_positions

    @staticmethod
    def text_positions(string, substring):
        return [i for i, ltr in enumerate(string.replace(substring, "\0")) if ltr == "\0"]

    @staticmethod
    def psd_text_positions(string, substring):
        text = CardText._psd_text(string.replace(substring, "\0")).replace("\0", substring)
        return CardText.text_positions(text, substring)

    @staticmethod
    def _psd_text(text):
        syms = [s() for s in symbols.SYMBOLS]
        for symbol in syms:
            text = text.replace(symbol.string, symbol.replacement)
        for formatter in CardText.FORMATTERS:
            text = text.replace(formatter, "")
        return text

    def psd_text(self):
        return self._psd_text(self.text)

    def wrap_text(self, ppi, line_lengths, inplace=False):
        lines = self.lines.copy()
        new_lines = []
        line_number = 0
        while line_number < len(lines):
            line = lines[line_number]

            # Check to see if the line contains a quote attribution. If it does, the entire attribution
            # should be treated as one word. For example, the quote "I am your father." —Darth Vader
            # shouldn't be split onto separate lines between 'Darth' and 'Vader'. It should be split
            # before '—Darth Vader'.
            # \u2014 is unicode for the em-dash (—)
            quote = line.rsplit(" \u2014", 1)
            if len(quote) == 2:
                speaker = "\u2014" + quote[1]
                words = quote[0].split(" ")
                words.append(speaker)
            else:
                words = line.split(" ")

            words_removed = 0
            if len(new_lines) + 1 > len(line_lengths):
                line_length = inf
            else:
                line_length = line_lengths[len(new_lines)]
            while self.text_width(line, ppi) > line_length:
                words_removed += 1
                line = " ".join(words[:-words_removed])
            new_lines.append(line)
            if words_removed > 0:
                line_remainder = " ".join(words[-words_removed:])
                lines[line_number] = line_remainder
            else:
                line_number += 1
        new_text = None if new_lines == [] else "\r".join(new_lines)

        if inplace:
            self.text = new_text
            self.lines = new_lines
            return None
        else:
            return new_text, new_lines
