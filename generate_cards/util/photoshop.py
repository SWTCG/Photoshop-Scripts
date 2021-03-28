from math import sqrt

import photoshop.api as ps
from photoshop.api.action_list import ActionList

ADJUSTMENT_LAYERS = [
    ps.LayerKind.BrightnessContrastLayer,
    ps.LayerKind.LevelsLayer,
    ps.LayerKind.CurvesLayer,
    ps.LayerKind.ExposureLayer,
    ps.LayerKind.Vibrance,
    ps.LayerKind.HueSaturationLayer,
    ps.LayerKind.ColorBalanceLayer,
    ps.LayerKind.BlackAndWhiteLayer,
    ps.LayerKind.PhotoFilterLayer,
    ps.LayerKind.ChannelMixerLayer,
    ps.LayerKind.ColorLookup,
    ps.LayerKind.InversionLayer,
    ps.LayerKind.PosterizeLayer,
    ps.LayerKind.ThresholdLayer,
    ps.LayerKind.SelectiveColorLayer,
    ps.LayerKind.GradientMapLayer
]


def get_layers(document, layers=None):
    """
    Puts all layers in a Photoshop document into a dictionary for easier by-name referencing.
    """
    if layers is None:
        layers = {}

    for artLayer in document.artLayers:
        layers[artLayer.name] = artLayer
    for layerSet in document.layerSets:
        layers[layerSet.name] = layerSet
        if [ls for ls in layerSet.layerSets] or [al for al in layerSet.artLayers]:
            get_layers(layerSet, layers)
        else:
            return layers
    return layers


def fixed_font_size(text_layer):
    """
    Returns the correct font size, in points, of the text in `text_layer`.
    """
    app = ps.Application()
    app.activeDocument.activeLayer = text_layer
    size = app.activeDocument.activeLayer.textItem.size
    r = ps.ActionReference()
    r.putProperty(app.stringIDToTypeID("property"), app.stringIDToTypeID("textKey"))
    r.putEnumerated(app.stringIDToTypeID("layer"), app.stringIDToTypeID("ordinal"), app.stringIDToTypeID("targetEnum"))
    try:
        transform = app.executeActionGet(r).getObjectValue(app.stringIDToTypeID("textKey")).getObjectValue(
            app.stringIDToTypeID("transform"))
        yy = transform.getDouble(app.stringIDToTypeID("yy"))
        yx = transform.getDouble(app.stringIDToTypeID("yx"))
    except:
        yy = 1
        yx = 0
    coeff = sqrt(yy * yy + yx * yx)
    return size * coeff


def partial_text_format(text_layer, start, end, font=None, font_size=None, horizontal_scale=None, vertical_scale=None,
                        faux_bold=None, faux_italic=None, rgb=None, anti_alias=None, tracking=None):
    """
    Formats a portion of the text in `text_layer` as defined by the `start` and `end` characters.

    :param text_layer: the Photoshop text layer to be formatted
    :param start: 0-indexed position number of first character in text to be formatted
    :param end: 0-indexed position number of last character in text to be formatted
    :param font: PostScript name of font
    :param font_size: font size in points
    :param horizontal_scale: horizontal scaling percentage of text in percent (e.g. 50, not 0.5)
    :param vertical_scale: vertical scaling percentage of text in percent (e.g. 50, not 0.5)
    :param faux_bold: use faux bold formatting (True or False)
    :param faux_italic: use faux italic formatting (True or False)
    :param rgb: (red, green, blue) tuple of text color values
    :param anti_alias: the anti-aliasing method to use
    :param tracking: the tracking value. This parameter controls the space between characters.
    :return: dictionary of formatting settings?
    """
    app = ps.Application()
    app.activeDocument.activeLayer = text_layer

    action_list = ActionList()

    desc61 = ps.ActionDescriptor()
    # Create reference
    idnull = app.charIDToTypeID("null")
    ref2 = ps.ActionReference()
    idTxLr = app.charIDToTypeID("TxLr")
    idOrdn = app.charIDToTypeID("Ordn")
    idTrgt = app.charIDToTypeID("Trgt")
    ref2.putEnumerated(idTxLr, idOrdn, idTrgt)
    desc61.putReference(idnull, ref2)

    desc62 = ps.ActionDescriptor()
    # Set anti-aliasing method
    idAnno = app.charIDToTypeID("Anno")
    idantiAliasSharp = app.stringIDToTypeID("antiAliasSharp")
    idAnCr = app.charIDToTypeID("AnCr")
    idAnSt = app.charIDToTypeID("AnSt")
    idAnSm = app.charIDToTypeID("AnSm")
    anti_alias_ids = {
        "none": idAnno,
        "sharp": idantiAliasSharp,
        "crisp": idAnCr,
        "strong": idAnSt,
        "smooth": idAnSm,
        1: idAnno,
        2: idantiAliasSharp,
        3: idAnCr,
        4: idAnSt,
        5: idAnSm
    }
    if anti_alias is None:
        anti_alias = text_layer.textItem.antiAliasMethod
    idAntA = app.charIDToTypeID("AntA")
    idAnnt = app.charIDToTypeID("Annt")
    desc62.putEnumerated(idAntA, idAnnt, anti_alias_ids[anti_alias])

    # Set character range to format
    text_range = ps.ActionDescriptor()
    idFrom = app.charIDToTypeID("From")
    text_range.putInteger(idFrom, start)
    idT = app.charIDToTypeID("T   ")
    text_range.putInteger(idT, end + 1)

    desc77 = ps.ActionDescriptor()

    # Set whether style sheet has a parent
    # Seems to be unnecessary, but keeping in case it is needed in the future.
    #
    # idstyleSheetHasParent = app.stringIDToTypeID("styleSheetHasParent")
    # desc77.putBoolean(idstyleSheetHasParent, True)

    # Set font by PostScript name
    if font is None:
        font = text_layer.textItem.font
    idfontPostScriptName = app.stringIDToTypeID("fontPostScriptName")
    desc77.putString(idfontPostScriptName, font)

    # Set font name
    # Redundant due to setting by PostScript name above. Keeping in case it is needed in the future.
    #
    # idFntN = app.charIDToTypeID("FntN")
    # desc77.putString(idFntN, """Dax""")

    # Set font style
    # Redundant due to setting by PostScript name above. Keeping in case it is needed in the future.
    #
    # idFntS = app.charIDToTypeID("FntS")
    # desc77.putString(idFntS, """Italic""")

    # Set font size
    if font_size is None:
        font_size = fixed_font_size(text_layer)
    idimpliedFontSize = app.stringIDToTypeID("impliedFontSize")
    idPnt = app.charIDToTypeID("#Pnt")
    desc77.putUnitDouble(idimpliedFontSize, idPnt, font_size)

    # Set horizontal scaling
    if horizontal_scale is None:
        horizontal_scale = text_layer.textItem.horizontalScale
    idHrzS = app.charIDToTypeID("HrzS")
    desc77.putDouble(idHrzS, horizontal_scale)

    # Set vertical scaling
    if vertical_scale is None:
        vertical_scale = text_layer.textItem.verticalScale
    idVrtS = app.charIDToTypeID("VrtS")
    desc77.putDouble(idVrtS, vertical_scale)

    # Set Faux Bold
    if faux_bold is None:
        faux_bold = text_layer.textItem.fauxBold
    idsyntheticBold = app.stringIDToTypeID("syntheticBold")
    desc77.putBoolean(idsyntheticBold, faux_bold)

    # Set Faux Italic
    if faux_italic is None:
        faux_italic = text_layer.textItem.fauxItalic
    idsyntheticItalic = app.stringIDToTypeID("syntheticItalic")
    desc77.putBoolean(idsyntheticItalic, faux_italic)

    # Set font color
    if rgb is None:
        red = text_layer.textItem.color.rgb.red
        green = text_layer.textItem.color.rgb.green
        blue = text_layer.textItem.color.rgb.blue
        rgb = (red, green, blue)

    idClr = app.charIDToTypeID("Clr ")
    font_color = ps.ActionDescriptor()
    idRd = app.charIDToTypeID("Rd  ")
    font_color.putDouble(idRd, rgb[0])
    idGrn = app.charIDToTypeID("Grn ")
    font_color.putDouble(idGrn, rgb[1])
    idBl = app.charIDToTypeID("Bl  ")
    font_color.putDouble(idBl, rgb[2])
    idRGBC = app.charIDToTypeID("RGBC")
    desc77.putObject(idClr, idRGBC, font_color)

    # Set the tracking
    if tracking is None:
        tracking = text_layer.textItem.tracking
    idTrck = app.charIDToTypeID("Trck")
    desc77.putInteger(idTrck, tracking)

    # These do not seem to be necessary for my current purposes, but I am keeping them in case they
    # are needed for something in the future.
    '''
    # Set leading
    auto_leading = text_layer.textItem.useAutoLeading
    idautoLeading = app.stringIDToTypeID("autoLeading")
    desc77.putBoolean(idautoLeading, auto_leading)
    
    # Set the baseline shift
    idBsln = charIDToTypeID("Bsln")
    idPnt = charIDToTypeID("#Pnt")
    desc77.putUnitDouble(idBsln, idPnt, 0.000000)
    
    idimpliedBaselineShift = stringIDToTypeID("impliedBaselineShift")
    idPnt = charIDToTypeID("#Pnt")
    desc77.putUnitDouble(idimpliedBaselineShift, idPnt, 0.000000)
    
    idAtKr = charIDToTypeID("AtKr")
    idAtKr = charIDToTypeID("AtKr")
    idmetricsKern = stringIDToTypeID("metricsKern")
    desc77.putEnumerated(idAtKr, idAtKr, idmetricsKern)
    
    idfontCaps = stringIDToTypeID("fontCaps")
    idfontCaps = stringIDToTypeID("fontCaps")
    idNrml = charIDToTypeID("Nrml")
    desc77.putEnumerated(idfontCaps, idfontCaps, idNrml)
    
    idbaseline = stringIDToTypeID("baseline")
    idbaseline = stringIDToTypeID("baseline")
    idNrml = charIDToTypeID("Nrml")
    desc77.putEnumerated(idbaseline, idbaseline, idNrml)
    
    idotbaseline = stringIDToTypeID("otbaseline")
    idotbaseline = stringIDToTypeID("otbaseline")
    idNrml = charIDToTypeID("Nrml")
    desc77.putEnumerated(idotbaseline, idotbaseline, idNrml)
    
    idstrikethrough = stringIDToTypeID("strikethrough")
    idstrikethrough = stringIDToTypeID("strikethrough")
    idstrikethroughOff = stringIDToTypeID("strikethroughOff")
    desc77.putEnumerated(idstrikethrough, idstrikethrough, idstrikethroughOff)
    
    idUndl = charIDToTypeID("Undl")
    idUndl = charIDToTypeID("Undl")
    idunderlineOff = stringIDToTypeID("underlineOff")
    desc77.putEnumerated(idUndl, idUndl, idunderlineOff)
    
    idligature = stringIDToTypeID("ligature")
    desc77.putBoolean(idligature, true)
    
    idaltligature = stringIDToTypeID("altligature")
    desc77.putBoolean(idaltligature, false)
    
    idbaselineDirection = stringIDToTypeID("baselineDirection")
    idbaselineDirection = stringIDToTypeID("baselineDirection")
    idwithStream = stringIDToTypeID("withStream")
    desc77.putEnumerated(idbaselineDirection, idbaselineDirection, idwithStream)
    
    idtextLanguage = stringIDToTypeID("textLanguage")
    idtextLanguage = stringIDToTypeID("textLanguage")
    idenglishLanguage = stringIDToTypeID("englishLanguage")
    desc77.putEnumerated(idtextLanguage, idtextLanguage, idenglishLanguage)
    
    idmojiZume = stringIDToTypeID("mojiZume")
    desc77.putDouble(idmojiZume, 0.000000)
    
    idgridAlignment = stringIDToTypeID("gridAlignment")
    idgridAlignment = stringIDToTypeID("gridAlignment")
    idroman = stringIDToTypeID("roman")
    desc77.putEnumerated(idgridAlignment, idgridAlignment, idroman)
    
    idnoBreak = stringIDToTypeID("noBreak")
    desc77.putBoolean(idnoBreak, false)
    
    idstrokeColor = app.stringIDToTypeID("strokeColor")
    desc79 = ps.ActionDescriptor()
    idRd = app.charIDToTypeID("Rd  ")
    desc79.putDouble(idRd, 40)
    idGrn = app.charIDToTypeID("Grn ")
    desc79.putDouble(idGrn, 50)
    idBl = app.charIDToTypeID("Bl  ")
    desc79.putDouble(idBl, 60)
    idRGBC = app.charIDToTypeID("RGBC")
    desc77.putObject(idstrokeColor, idRGBC, desc79)
    
    idFl = app.charIDToTypeID("Fl  ")
    desc77.putBoolean(idFl, True)
    
    idStrk = app.charIDToTypeID("Strk")
    desc77.putBoolean(idStrk, False)
    
    idfillFirst = app.stringIDToTypeID("fillFirst")
    desc77.putBoolean(idfillFirst, False)
    
    idlineWidth = app.stringIDToTypeID("lineWidth")
    idPnt = app.charIDToTypeID("#Pnt")
    desc77.putUnitDouble(idlineWidth, idPnt, 0.120000)
    '''

    idTxtS = app.charIDToTypeID("TxtS")
    text_range.putObject(idTxtS, idTxtS, desc77)
    idTxtt = app.charIDToTypeID("Txtt")
    action_list.putObject(idTxtt, text_range)

    desc62.putList(idTxtt, action_list)
    desc61.putObject(idT, idTxLr, desc62)
    idsetd = app.charIDToTypeID("setd")
    app.executeAction(idsetd, desc61)
    return None


def move_layer_to(layer, x, y):
    """
    Author: Max Kielland
    Translated to Python by Matt Haechrel

    Moves layer to the absolute position (x, y). The unit of x and y are the same as the
    ruler setting.
    """
    position = list(layer.bounds)
    position[0] = x - position[0]
    position[1] = y - position[1]

    layer.translate(position[0], position[1])
    return None


def move_text_to(text_layer, x, y):
    """
    Similar to method `move_layer_to` but instead of positioning the layer based on its bounds,
    this method positions it based on the position of the text baseline.
    """
    position = text_layer.textItem.position
    position[0] = x - position[0]
    position[1] = y - position[1]

    text_layer.translate(position[0], position[1])
    return None


def set_text(layer, text):
    """
    Set the text content of a layer without changing any of the formatting.
    :param layer: The PhotoShop text layer object.
    :param text: The text to set.
    """
    app = ps.Application()
    app.activeDocument.activeLayer = layer

    r = ps.ActionReference()
    idTxLr = app.charIDToTypeID("TxLr")
    idOrdn = app.charIDToTypeID("Ordn")
    idTrgt = app.charIDToTypeID("Trgt")
    r.putEnumerated(idTxLr, idOrdn, idTrgt)
    textKey = app.executeActionGet(r).getObjectValue(app.stringIDToTypeID("textKey"))
    textKey.putString(app.stringIDToTypeID("textKey"), text)

    d = ps.ActionDescriptor()
    d.putReference(app.stringIDToTypeID("null"), r)
    d.putObject(app.stringIDToTypeID("to"), app.stringIDToTypeID("textLayer"), textKey)

    app.executeAction(app.stringIDToTypeID("set"), d)
    return None
