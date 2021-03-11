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

    def test_mission(self):
        extraction = NonUnit(
            name="Extraction",
            typeline="Mission",
            expansion="BF",
            side="N",
            rarity="C",
            image="BF073_Extraction.psd",
            number="73",
            cost="X",
            game_text="Shuffle X+1 cards from your discard pile into your deck.\rPay X build points -> Meditate"
        )
        extraction.wrap_text()
        extraction.write_psd()

    def test_location(self):
        endor_battlefront = NonUnit(
            name="Endor Battlefront",
            typeline="Location - Ground - Endor Forest Battlefield",
            expansion="BF",
            side="N",
            rarity="R",
            image="BF013_Endor_Battlefront.psd",
            number="13",
            cost="3",
            game_text="Each Endor and Forest unit gets \"Pay 1 Force -> Ambush 1.\"\rEach Imperial gets Critical Hit 1 "
                      "and Resilience 1.\rEach Rebel gets +1 power and Lucky 1.",
            flavor_text="\"Oh, I told you it was dangerous here!\" \u2014C-3PO"
        )
        endor_battlefront.wrap_text()
        endor_battlefront.write_psd()
