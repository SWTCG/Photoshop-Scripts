import time
from comtypes import COMError

import process_text


def generate_cards(card_df):
    for card in card_df['card_object'].iloc[35:36]:
        try:
            card.write_psd(save=True, export=True, auto_close=True)
            try:
                print(card.number, card.name, sep="\t")
            except AttributeError:
                print(card.name)
        except COMError:
            try:
                print(f"Unhandled exception in {card.number} {card.name}.")
            except AttributeError:
                print(f"Unhandled exception in {card.name}.")
    return None


def generate_expansion(expansion):
    file = expansion + ".txt"
    cards = process_text.import_lackey_file(file)
    generate_cards(cards)
    return None


if __name__ == "__main__":
    start = time.time()

    generate_expansion("BF")

    end = time.time()
    runtime = round(end - start)
    print(f"Competed in {runtime} seconds.")
