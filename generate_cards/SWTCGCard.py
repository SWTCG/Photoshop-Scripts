import os
import warnings

import photoshop.api as ps
import yaml

import generate_cards.symbols as symbols
import generate_cards.util.photoshop as ps_util
from generate_cards.CardText import CardText
from generate_cards.expansions import EXPANSIONS


class SWTCGCard:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'config.yaml'), 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)
    DAX_REG = config['fonts']['Dax']['Regular']
    DAX_ITAL = config['fonts']['Dax']['Italic']
    TEMPLATE_DIR = config['template_dir']
    IMAGE_DIR = config['image_dir']

    SIDES = {"D": "Dark", "L": "Light", "N": "Neutral"}
    RARITIES = {"R": "Rare", "U": "Uncommon", "C": "Common", "P": "Promo", "S": "Subordinate"}
    DEFAULT_FONT_SIZE = 7  # In points
    SMALL_FONT_SIZE = 6.5  # In points
    # Could go as small as 6 pt to get 10 lines on a unit card. Darth Sidious (G) is precedent.

    def __init__(self, name, typeline, expansion, side, rarity, image,
                 game_text=None, flavor_text=None, version=None, icon=True, ppi=600):
        self.name = name
        self.typeline = typeline
        self.expansion = expansion
        self.side = side
        self.rarity = rarity
        self.image = image
        self.icon = icon
        self.ppi = ppi

        self.game_text = CardText(game_text, SWTCGCard.DAX_REG, SWTCGCard.DEFAULT_FONT_SIZE)
        self.flavor_text = CardText(flavor_text, SWTCGCard.DAX_ITAL, SWTCGCard.DEFAULT_FONT_SIZE)
        self.version = version

        self.type = typeline.split(" - ")[0]
        self.subtypes = typeline.split(" - ")[1:]
        self.template = self.choose_template()

    def is_multi_arena(self):
        for type_text in self.type:
            is_space = type_text.capitalize().find("Space") != -1
            is_ground = type_text.capitalize().find("Ground") != -1
            is_character = type_text.capitalize().find("Character") != -1
            if is_space or is_ground or is_character:
                if type_text.find("/") != -1:
                    return True
        return False

    def choose_template(self):
        card_type = self.type
        is_multi_arena = self.is_multi_arena()

        if is_multi_arena:
            template = "Multi-Arena"
        else:
            template = card_type

        if card_type in ["Location", "Subordinate"]:
            if is_multi_arena:
                template = card_type + " - Multi-Arena"
            else:
                template = card_type + " - " + self.subtypes[0]

        if card_type == "Mission" and self.subtypes:
            template = card_type + " - " + self.subtypes[0]

        if card_type == "Equipment":
            for subtype in ["Trait", "Skill"]:
                if subtype in self.subtypes:
                    template = card_type + " - " + subtype

        return template + " Template.psd"

    def _wrap_text(self, text_limits):
        for index, limit in enumerate(text_limits):
            self.game_text.font_size = limit.font_size
            self.game_text.scale = limit.horizontal_scale
            self.flavor_text.font_size = limit.font_size
            self.flavor_text.scale = limit.horizontal_scale
            line_lengths = limit.line_length_limits

            new_game_lines = self.game_text.wrap_text(self.ppi, line_lengths)[1]
            new_flavor_lines = self.flavor_text.wrap_text(self.ppi, line_lengths[len(new_game_lines) + 1:])[1]

            line_count = len(new_game_lines) + len(new_flavor_lines)
            if len(new_flavor_lines) > 0:
                line_count += 1

            if line_count <= limit.line_count:
                self.game_text.text = "\r".join(new_game_lines)
                self.flavor_text.text = "\r".join(new_flavor_lines)
                self.game_text.lines = new_game_lines
                self.flavor_text.lines = new_flavor_lines
                return 0
            elif index == len(text_limits) - 1:
                # Issue warning if maximum line count is exceeded even after checking all text formatting
                # options.
                self.game_text.text = "\r".join(new_game_lines)
                self.flavor_text.text = "\r".join(new_flavor_lines)
                self.game_text.lines = new_game_lines
                self.flavor_text.lines = new_flavor_lines
                warnings.warn(f"{self.name} exceeds maximum line count")
                return 1

    def _write_psd(self, document):
        layer_dict = ps_util.get_layers(document)

        layer_dict["Card Name"].textItem.contents = self.name
        layer_dict["Typeline"].textItem.contents = self.typeline

        if self.game_text.text is None or self.game_text.text == "":
            layer_dict["Game Text"].visible = False  # Hide Game Text layer
            flavor_shift = 0
        else:
            # Set game text and font size
            layer_dict["Game Text"].visible = True
            layer_dict["Game Text"].textItem.contents = self.game_text.psd_text()
            layer_dict["Game Text"].textItem.size = self.game_text.font_size
            layer_dict["Game Text"].textItem.horizontalScale = self.game_text.scale * 100

            line_gap = layer_dict["Game Text"].textItem.position[1] - layer_dict["Game Text"].bounds[1]
            flavor_shift = len(self.game_text.lines) * self.game_text.font_size * 10 * self.ppi / 600 + line_gap

        if self.flavor_text.text is None or self.flavor_text.text == "":
            layer_dict["Flavour Text"].visible = False  # Hide Flavour Text layer
        else:
            # Set flavor text and font size
            layer_dict["Flavour Text"].visible = True
            layer_dict["Flavour Text"].textItem.contents = self.flavor_text.psd_text()
            layer_dict["Flavour Text"].textItem.size = self.flavor_text.font_size
            layer_dict["Flavour Text"].textItem.horizontalScale = self.flavor_text.scale * 100
            # Position flavor text
            layer_dict["Flavour Text"].textItem.position = [
                layer_dict["Game Text"].textItem.position[0],
                layer_dict["Game Text"].textItem.position[1] + flavor_shift
            ]

        if self.version is None:
            if "Unique" in layer_dict.keys():
                layer_dict["Unique"].visible = False  # Hide Unique layer set
        else:
            layer_dict["Unique"].visible = True
            layer_dict["Version Letter"].textItem.contents = self.version

        # Show correct side layer and hide the rest.
        for s in SWTCGCard.SIDES:
            if s == self.side:
                layer_dict[SWTCGCard.SIDES[s]].visible = True
            else:
                layer_dict[SWTCGCard.SIDES[s]].visible = False

        # Show correct rarity layer and hide the rest.
        for r in SWTCGCard.RARITIES:
            if r == self.rarity:
                layer_dict[SWTCGCard.RARITIES[r]].visible = True
            else:
                if SWTCGCard.RARITIES[r] in layer_dict.keys():
                    layer_dict[SWTCGCard.RARITIES[r]].visible = False

        # Show correct expansion symbol and hide the rest.
        for e in EXPANSIONS:
            if e == self.expansion:
                layer_dict[EXPANSIONS[e].layer].visible = True
            else:
                if EXPANSIONS[e].layer in layer_dict.keys():
                    layer_dict[EXPANSIONS[e].layer].visible = False

        # Position tap symbols, pilot symbols, arrows, and bullet points, if any.
        self.place_symbol(symbols.Tap(self.ppi, self.game_text.font_size), layer_dict)
        self.place_symbol(symbols.Pilot(self.ppi, self.game_text.font_size), layer_dict)
        self.place_symbol(symbols.Arrow(self.ppi, self.game_text.font_size), layer_dict)
        self.place_symbol(symbols.Bullet(self.ppi, self.game_text.font_size), layer_dict)

        # Italicize words in game and flavor text
        for i in zip(CardText.psd_text_positions(self.game_text.text, "<i>"),
                     CardText.psd_text_positions(self.game_text.text, "</i>")):
            ps_util.partial_text_format(layer_dict["Game Text"], i[0], i[1], font="Dax-Italic")

        for i in zip(CardText.psd_text_positions(self.flavor_text.text, "<i>"),
                     CardText.psd_text_positions(self.flavor_text.text, "</i>")):
            ps_util.partial_text_format(layer_dict["Flavour Text"], i[0], i[1], font="Dax-Regular")

        # Insert release year into copyright.
        self.copyright(layer_dict)

        # Place image.
        if self.image is not None:
            self.place_image(document, layer_dict)

        # Set IDC/Promo icon
        for icon_layer in layer_dict["IDC/Promo Icons"].layers:
            layer_dict[icon_layer.name].visible = False
        if self.icon is True:
            if EXPANSIONS[self.expansion].year >= 2010:
                if self.rarity == "P":
                    layer_dict["IDC Promo Icon (Revised)"].visible = True
                else:
                    layer_dict["IDC Icon (Revised)"].visible = True
            elif 2006 <= EXPANSIONS[self.expansion].year < 2010:
                if self.rarity == "P":
                    layer_dict["IDC Promo Icon (Original)"].visible = True
                else:
                    layer_dict["IDC Icon (Original)"].visible = True
            else:
                if self.rarity == "P":
                    layer_dict["Promo Icon"].visible = True
        elif self.icon:
            layer_dict[self.icon].visible = True
        else:
            pass

        # Text should probably be cleaned for proper bullet point characters, é characters, en dashes in front of
        # numbers, etc. before getting to this function.

        # Save PSD
        # Export as PNG

        return None

    def place_symbol(self, symbol, layers):
        symbol_count = self.game_text.text.count(symbol.string)
        psd_text = self.game_text.psd_text()
        if symbol_count > 0:
            layers[symbol.layer_name].visible = True
            bounds = layers[symbol.layer_name].bounds
            resize_pct = (symbol.width / (bounds[2] - bounds[0]) * 100,
                          symbol.height / (bounds[3] - bounds[1]) * 100)
            layers[symbol.layer_name].resize(*resize_pct)
            for i in range(symbol_count):
                if i > 0:
                    # Duplicate symbol layer if there is more than one of the symbol in the game text.
                    layer_name = symbol.layer_name + " " + str(i + 1)
                    if layer_name in layers.keys():
                        layers[layer_name].visible = True
                        bounds = layers[layer_name].bounds
                        resize_pct = (symbol.width / (bounds[2] - bounds[0]) * 100,
                                      symbol.height / (bounds[3] - bounds[1]) * 100)
                        layers[layer_name].resize(*resize_pct)
                    else:
                        layers[layer_name] = layers[symbol.layer_name].duplicate()
                    layers[layer_name].name = layer_name
                else:
                    layer_name = symbol.layer_name
                init_pos = layers["Game Text"].textItem.position
                text_alignment = layers["Game Text"].textItem.justification
                xy_pos, text_pos = self.game_text.position_symbol(symbol, self.ppi, align=text_alignment)
                ps_util.move_layer_to(layers[layer_name], init_pos[0] + xy_pos[i][0], init_pos[1] + xy_pos[i][1])

                space_width = self.game_text.text_width(" ", self.ppi, scale=1)
                next_char = psd_text[text_pos[i] + 1] if text_pos[i] < len(psd_text) else ""
                space_scale = (symbol.width + symbol.right_kern.get(next_char, 0)) / space_width
                ps_util.partial_text_format(layers["Game Text"], text_pos[i], text_pos[i],
                                            horizontal_scale=space_scale * 100)
        else:
            layers[symbol.layer_name].visible = False

        # Clean up unneeded layers
        symbol_layers = []
        for layer in layers.keys():
            if layer.find(symbol.layer_name + " ") > -1:
                symbol_layers.append(layer)
        for layer in symbol_layers:
            try:
                if int(layer[-1]) > symbol_count:
                    layers[layer].delete()
            except ValueError:
                pass

    def copyright(self, layer_dict):
        # \u00a9 is the copyright sign. \u00ae is the registered sign
        year = EXPANSIONS[self.expansion].year
        copyright_text = "\u00a9 {} LUCASFILM LTD. & \u00ae or TM. GAME DESIGN: WIZARDS.".format(year)
        ps_util.set_text(layer_dict["Copyright"], copyright_text)

    def place_image(self, document, layer_dict):
        app = ps.Application()
        app.load(os.path.join(self.IMAGE_DIR, self.image))
        doc2 = app.activeDocument(self.image)
        layer_dict2 = ps_util.get_layers(doc2)

        # Grab all of the images under Card Image
        layer_num = 0
        for card_image in layer_dict2["Card Image"].layers:
            layer_num += 1
            app.activeDocument = doc2
            layer_dict2[card_image.name].duplicate(layer_dict["Card Image"], ps.ElementPlacement.PlaceAtEnd)
            layer_dict = ps_util.get_layers(document)
            # Resize image to 99.2% of its original size to compensate for difference in card sizes.
            resize_pct = 99.2
            app.activeDocument = document
            layer_dict[card_image.name].resize(resize_pct, resize_pct, ps.AnchorPosition.TopLeft)
        layer_dict["Gamma Correction"].visible = True
        return None
