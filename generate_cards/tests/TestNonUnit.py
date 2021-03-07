import unittest

from generate_cards.NonUnit import NonUnit


class TestNonUnit(unittest.TestCase):
    def test_battle_card(self):
        our_finest_hour = NonUnit(
            name="Our Finest Hour",
            typeline="Battle",
            expansion="BF",
            side="D",
            rarity="R",
            image="BF023_Our_Finest_Hour.psd",
            number="23",
            game_text="Pay 5 Force -> One of your unique Imperials gets Inspiration until it is discarded.\r"
                      "Pay 5 Force -> Meditate",
            flavor_text="\"As the Rebels fled, the 501st gathered around a burning bunker and let out a cheer that "
                        "shook the stars.\" \u2014Retired 501st trooper"
        )
        our_finest_hour.wrap_text()
        our_finest_hour.write_psd()
