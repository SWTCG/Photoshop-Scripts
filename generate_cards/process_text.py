import os
import re

import numpy as np
import pandas as pd

from read_config import CONFIG
from NonUnit import NonUnit
from Subordinate import Subordinate
from Unit import Unit


def import_lackey_file(file_name):
    file_path = os.path.join(CONFIG['card_data_dir'], file_name)
    cards = pd.read_csv(file_path, sep='\t', encoding='utf-8', usecols=list(range(15)), dtype=str)

    # Create unique index
    cards.loc[cards['Rarity'] != 'S', 'id'] = cards['Set'].str.cat(cards['Number'].astype(str).str.zfill(3), sep='_')
    cards.loc[cards['Rarity'] == 'S', 'id'] = 'SUB_' + cards['Number'].astype(str).str.zfill(4)
    cards.set_index('id', inplace=True)

    # Create properly named columns
    cards['version'] = cards['Name'].map(lambda x: x[x.rfind("(") + 1: -1] if x[-1] == ")" else "")
    cards['name'] = cards['Name'].map(lambda x: x[:x.rfind("(")] if x[-1] == ")" else x)
    cards['name'] = cards['name'].map(lambda x: x[:x.rfind("{")] if x[-1] == "}" else x)
    cards.loc[~cards['Subtype'].isna(), 'typeline'] = cards['Type'] + " - " + cards['Subtype']
    cards.loc[cards['Subtype'].isna(), 'typeline'] = cards['Type']
    cards['image'] = cards['ImageFile'] + ".psd"
    column_names = {'Set': 'expansion', 'Side': 'side', 'Rarity': 'rarity', 'Text': 'game_text',
                    'Cost': 'cost', 'Speed': 'speed', 'Power': 'power', 'Health': 'health',
                    'Number': 'number'}
    cards.rename(columns=column_names, inplace=True)

    # Merge flavor text
    expansions = cards['expansion'].unique()
    for expansion in expansions:
        expansion_flavor = pd.read_csv(f'card_data/flavor/{expansion}.csv', sep=',', encoding='utf-8', index_col='id')
        cards.loc[cards['expansion'] == expansion, 'flavor_text'] = (
            cards[cards['expansion'] == expansion]
            .merge(expansion_flavor, how='left', left_index=True, right_index=True)['flavor_text']
        )

    # Drop unneeded columns
    keep_columns = ['name', 'typeline', 'expansion', 'side', 'rarity', 'image', 'cost', 'speed', 'power', 'health',
                    'number', 'game_text', 'flavor_text', 'version']
    cards = cards[keep_columns]

    cards.fillna("", inplace=True)
    cards = exclude_promos(cards)
    cards = clean_text(cards)
    cards = text_replacement(cards)
    cards = card_kind(cards)
    cards = card_object(cards)
    return cards


def exclude_promos(card_df):
    """
    Exclude promo cards. Those can be handled separately since it doesn't make sense to create
    separate PSDs for them.
    """
    return card_df[card_df['rarity'] != 'P']


def replace_with_bullets(game_text):
    if game_text.find("gets:") != -1:
        abilities = game_text.split(" | ")
        for i, ability in enumerate(abilities):
            if ability.find("gets:") != -1:
                abilities[i] = re.sub(r"\s*-\s*([^>])", "\r\u2022 \\1", ability)
        game_text = " | ".join(abilities)
    return game_text


def clean_text(card_df):
    """
    Perform string replacements to properly format the game text and ensure the correct
    characters are used.
    """
    # Relevant Unicode Characters
    # \u00e9: acute accented e
    # \u2013: en dash
    # \u2014: em dash
    # \u2022: bullet
    card_df['game_text'] = (
        card_df['game_text']
        # Replace hyphens used as list markers with bullets
        .map(replace_with_bullets)
        # Accent the e on Padmé
        .str.replace("Padme", "Padm\u00e9", regex=False)
        # Italicize words in parentheses
        .str.replace(r"(\([^(]+\))", "<i>\\1</i>", regex=True)
        # Replace instances of hyphen followed by a number with an en dash, e.g. -1
        .str.replace(r"(^| )-(\d+\b)", "\\1\u2013\\2", regex=True)
        # Separate abilities with a carriage return
        .str.replace(" | ", "\r", regex=False)
    )
    return card_df


def text_replacement(card_df):
    """
    Handle text replacement not taken care of by `clean_text` method. Text replacements are
    manually defined in replacements.csv
    """
    replacements = pd.read_csv('card_data/replacements.csv', sep=',', encoding='utf-8')
    replacements = replacements[replacements['card_id'].isin(card_df.index)]
    for i in range(len(replacements)):
        original_text = replacements['original_text'].iloc[i]
        replacement_text = replacements['replacement_text'].iloc[i]
        name = card_df['name'].loc[replacements['card_id'].iloc[i]]
        game_text = card_df['game_text'].loc[replacements['card_id'].iloc[i]]
        card_df.loc[replacements['card_id'].iloc[i], 'name'] = name.replace(original_text, replacement_text)
        card_df.loc[replacements['card_id'].iloc[i], 'game_text'] = game_text.replace(original_text, replacement_text)
    return card_df


def card_kind(card_df):
    """
    Add column for card type and kind (whether each card is a unit, non-unit, or subordinate).
    """
    card_df['type'] = card_df['typeline'].map(lambda x: x.split(" - ")[0])
    card_df.loc[card_df['rarity'] == 'S', 'kind'] = 'subordinate'
    card_df.loc[card_df['type'].map(lambda x: x.split("/")[0]).isin(["Space", "Ground", "Character"]), 'kind'] = 'unit'
    card_df.loc[(card_df['kind'] != 'subordinate') & (card_df['kind'] != 'unit'), 'kind'] = 'non-unit'
    return card_df


def card_object(card_df):
    """
    Add column containing the correct card object for each kind of card
    """
    unit_args = ['name', 'typeline', 'expansion', 'side', 'rarity', 'cost', 'speed', 'power', 'health', 'number',
                 'image', 'game_text', 'flavor_text', 'version']
    nonunit_args = ['name', 'typeline', 'expansion', 'side', 'rarity', 'cost', 'number', 'image', 'game_text',
                    'flavor_text', 'version']
    subordinate_args = ['name', 'typeline', 'expansion', 'side', 'rarity', 'speed', 'power', 'health', 'image',
                        'game_text', 'flavor_text', 'version']
    card_df.loc[card_df['kind'] == 'unit', 'card_object'] = np.vectorize(Unit)(
        **card_df.loc[card_df['kind'] == 'unit', unit_args]
    )
    card_df.loc[card_df['kind'] == 'non-unit', 'card_object'] = np.vectorize(NonUnit)(
        **card_df.loc[card_df['kind'] == 'non-unit', nonunit_args]
    )
    card_df.loc[card_df['kind'] == 'subordinate', 'card_object'] = np.vectorize(Subordinate)(
        **card_df.loc[card_df['kind'] == 'subordinate', subordinate_args]
    )
    card_df['card_object'].map(lambda x: x.wrap_text())
    return card_df
