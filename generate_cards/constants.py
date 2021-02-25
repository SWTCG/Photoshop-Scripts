# The number of (non-subordinate) cards in each expansion
EXPANSION_SIZES = {
    'AOTC': 180, 'SR': 90, 'ANH': 180, 'BOY': 105, 'JG': 105,
    'ESB': 210, 'RAS': 105, 'PM': 90, 'ROTJ': 110, 'ROTS': 110,
    'FOTR': 120, 'SAV': 90, 'BOE': 180, 'RAW': 120, 'ION': 180,
    'BOH': 60, 'BH': 75, 'MAND': 75, 'SITH': 75, 'SMUG': 75,
    'JEDI': 75, 'RO2': 90, 'TOR': 120, 'CWSO': 90, 'RS': 180,
    'ER': 120, 'EE': 90, 'AGD': 270, 'TDT': 300, 'CAD': 120,
    'TFA': 180, 'VP': 180, 'TAL': 240, 'SBS': 120, 'DAN': 150,
    'BL': 270, 'RO': 180, 'BOSB': 105, 'TLJ': 210, 'SOR': 180,
    'BF': 90, 'JK': 90, 'TUF': 120, 'BOC': 150, 'SOLO': 180,
    'KAE': 180
}

EXPANSION_LAYERS = {
    'AOTC': '01 Attack of the Clones',
    'SR': '02 Sith Rising',
    'ANH': '03 A New Hope',
    'BOY': '04 Battle of Yavin',
    'JG': '05 Jedi Guardians',
    'ESB': '06 The Empire Strikes Back',
    'RAS': '07 Rogues and Scoundrels',
    'PM': '08 The Phantom Menace',
    'ROTJ': '09 Return of the Jedi',
    'ROTS': '10 Revenge of the Sith',
    'FOTR': '11 Fall of the Republic',
    'SAV': '12 Scum and Villainy'
}

# The 10th Anniversary set (TEN) does not have its own expansion symbol. Instead, it contains promo
# cards for other expansions. This dictionary stores which expansion's symbol should be displayed
# on each card.
TENTH_ANNIVERSARY = {
    'Darth Nihilus (B)': 'SITH', 'Darth Plagueis (A)': 'SITH',
    'Skywalker Twins (A)': 'JEDI', 'Solo Twins (B)': 'JEDI',
    'Shan Family (A)': 'TOR', 'Slicer': 'TOR',
    'Brotherhood of Darkness (B)': 'RO2', 'Darth Tenebrous (A)': 'RO2',
    'Corellian HT-2200 Freighter': 'SMUG', 'Salacious B. Crumb (B)': 'SMUG',
    "Jabba's Sail Barge (B)": 'SAV', 'Jawa Mining Operation': 'SAV',
    'Grand Army of the Republic (A)': 'RAW', 'Kill or Be Killed': 'RAW',
    'Nelvaan Markings': 'CWSO', 'Orvos (B)': 'CWSO',
    'Blade Squadron (A)': 'BOE', 'Rebel Victory': 'BOE',
    'Bothan Males': 'RS', 'Wraith Squadron (A)': 'RS',
    'A-wing Slash': 'ER', 'Honoghr': 'ER',
    'Kuat Drive Yards': 'EE', 'Republic Observer': 'EE',
    "Augie's Great Municipal Band (A)": 'ION', 'Captain Tarpals (C)': 'ION',
    'Lord Starkiller Attacks': 'BOH', "Wedge's Snowspeeder (B)": 'BOH',
    'Clan Fett (A)': 'BH', 'On the Hunt': 'BH',
    'Clan Vizsla (A)': 'MAND', 'Sabine Wren (A)': 'MAND',
    'Clone Superiority': 'CAD', 'Droid Swarm': 'CAD',
    'Pirate Gang': 'AGD', 'Separatist Droid Army (A)': 'AGD',
    'Sith Legend': 'FOTR', 'Subtleties of the Force': 'FOTR',
    'Alliance High Command (A)': 'TDT', 'True Power of the Empire': 'TDT'
}
