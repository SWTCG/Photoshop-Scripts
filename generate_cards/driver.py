import time
import warnings
from comtypes import COMError

import process_text


def generate_cards(card_df):
    failure_idx = []
    for idx in card_df.index:
        card = card_df['card_object'].loc[idx]
        try:
            exit_code = card.write_psd(save=True, export=True, auto_close=True)
            if exit_code == 0:
                try:
                    print(card.number, card.name, sep="\t")
                except AttributeError:
                    print(card.name)
            else:
                failure_idx.append(idx)
        except COMError:
            try:
                warnings.warn(f"Unhandled exception in {card.number} {card.name}.")
            except AttributeError:
                warnings.warn(f"Unhandled exception in {card.name}.")
    failures = card_df.loc[failure_idx]
    failures.drop(columns=['card_object'], inplace=True)
    failures.to_csv('failures.tsv', sep="\t")
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
