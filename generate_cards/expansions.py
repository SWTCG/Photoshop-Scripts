from collections import OrderedDict

from generate_cards.constants import TENTH_ANNIVERSARY


class Expansion:
    def __init__(self, size, year, layer):
        self.size = size
        self.year = year
        self.layer = layer


EXPANSIONS = OrderedDict({
    'AOTC': Expansion(size=180, year=2002, layer="01 Attack of the Clones"),
    'SR': Expansion(size=90, year=2002, layer="02 Sith Rising"),
    'ANH': Expansion(size=180, year=2002, layer="03 A New Hope"),
    'BOY': Expansion(size=105, year=2003, layer="04 Battle of Yavin"),
    'JG': Expansion(size=105, year=2003, layer="05 Jedi Guardians"),
    'ESB': Expansion(size=210, year=2003, layer="06 The Empire Strikes Back"),
    'RAS': Expansion(size=105, year=2004, layer="07 Rogues and Scoundrels"),
    'PM': Expansion(size=90, year=2004, layer="08 The Phantom Menace"),
    'ROTJ': Expansion(size=110, year=2004, layer="09 Return of the Jedi"),
    'ROTS': Expansion(size=110, year=2005, layer="10 Revenge of the Sith"),
    'FOTR': Expansion(size=120, year=2006, layer="11 Fall of the Republic"),
    'SAV': Expansion(size=90, year=2006, layer="12 Scum and Villainy"),
    'BOE': Expansion(size=180, year=2007, layer="13 Battle of Endor"),
    'RAW': Expansion(size=120, year=2008, layer="14 Clone Wars: Republic at War"),
    'ION': Expansion(size=180, year=2009, layer="15 Invasion of Naboo"),
    'BOH': Expansion(size=60, year=2009, layer="16 Battle of Hoth"),
    'BH': Expansion(size=75, year=2010, layer="17 Legacy of the Force: Bounty Hunters"),
    'MAND': Expansion(size=75, year=2011, layer="18 Legacy of the Force: Mandalorians"),
    'SITH': Expansion(size=75, year=2011, layer="19 Legacy of the Force: Sith"),
    'SMUG': Expansion(size=75, year=2013, layer="20 Legacy of the Force: Smugglers"),
    'JEDI': Expansion(size=75, year=2013, layer="21 Legacy of the Force: Jedi"),
    'RO2': Expansion(size=90, year=2014, layer="22 Rule of Two"),
    'TOR': Expansion(size=120, year=2014, layer="23 The Old Republic"),
    'CWSO': Expansion(size=90, year=2015, layer="24 Clone Wars: Separatist Offensive"),
    'RS': Expansion(size=180, year=2015, layer="25 Rogue Squadron"),
    'ER': Expansion(size=120, year=2015, layer="26 Empire Rising"),
    'EE': Expansion(size=90, year=2015, layer="27 Empire Eternal"),
    'AGD': Expansion(size=270, year=2016, layer="28 The Clone Wars: A Galaxy Divided"),
    'TDT': Expansion(size=300, year=2016, layer="29 The Dark Times"),
    'CAD': Expansion(size=120, year=2016, layer="30 Clones and Droids"),
    # 'TEN': Expansion(size=40, year=2016, layer=TENTH_ANNIVERSARY),
    'TFA': Expansion(size=180, year=2016, layer="31 The Force Awakens"),
    'VP': Expansion(size=180, year=2016, layer="32 The New Jedi Order: Vector Prime"),
    'TAL': Expansion(size=240, year=2017, layer="33 The Old Republic: Tales and Legends"),
    'SBS': Expansion(size=120, year=2017, layer="34 The New Jedi Order: Star by Star"),
    'DAN': Expansion(size=150, year=2017, layer="35 The Old Republic: Days and Nights"),
    'BL': Expansion(size=270, year=2018, layer="36 The Clone Wars: Battle Lines"),
    'RO': Expansion(size=180, year=2018, layer="37 Rogue One"),
    'BOSB': Expansion(size=105, year=2018, layer="38 Battle of Starkiller Base"),
    'TLJ': Expansion(size=210, year=2018, layer="39 The Last Jedi"),
    'SOR': Expansion(size=180, year=2019, layer="40 Spark of Rebellion"),
    'BF': Expansion(size=90, year=2019, layer="41 Battlefront"),
    'JK': Expansion(size=90, year=2019, layer="42 Jedi Knight"),
    'TUF': Expansion(size=120, year=2019, layer="43 The New Jedi Order: The Unifying Force"),
    'BOC': Expansion(size=150, year=2020, layer="44 Battle of Crait"),
    'SOLO': Expansion(size=180, year=2020, layer="45 Solo"),
    'KAE': Expansion(size=180, year=2020, layer="46 The Old Republic: Knights and Exiles")
})
