

import process_text


file = "BF.txt"
cards = process_text.import_lackey_file(file)
for card in cards['card_object'].head():
    card.write_psd(auto_close=False)
