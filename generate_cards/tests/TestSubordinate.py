import unittest

from generate_cards.Subordinate import Subordinate


class TestUnit(unittest.TestCase):
    def test_flavor(self):
        imperial_sentinel_messenger = Subordinate(
            name="Imperial Sentinel Messenger",
            typeline="Subordinate - Character - Imperial Droid",
            expansion="BF",
            side="D",
            rarity="S",
            image=None,
            speed="20",
            power="1",
            health="1",
            game_text="Upkeep: Gain 1 build point.",
            flavor_text="\"Operation: Cinder is to begin at once.\""
        )
        imperial_sentinel_messenger.wrap_text()
        imperial_sentinel_messenger.write_psd()

    def test_unique(self):
        dio_b = Subordinate(
            name="Dio",
            typeline="Subordinate - Character - Rebel Spy Droid",
            expansion="BF",
            side="L",
            rarity="S",
            image=None,
            speed="70",
            power="2",
            health="1",
            game_text="Stun 3",
            version="B"
        )
        dio_b.wrap_text()
        dio_b.write_psd()

    def test_tap(self):
        imperial_royal_guards = Subordinate(
            name="Imperial Royal Guards",
            typeline="Subordinate - Ground/Character - Imperial Bodyguard Squad",
            expansion="BF",
            side="D",
            rarity="S",
            image=None,
            speed="30",
            power="3",
            health="3",
            game_text="Armor\r[tap] -> Protect 3"
        )
        imperial_royal_guards.wrap_text()
        imperial_royal_guards.write_psd()

    def test_two_abilities(self):
        rebel_soldier = Subordinate(
            name="Rebel Soldier",
            typeline="Subordinate - Ground/Character - Rebel Soldier",
            expansion="BF",
            side="L",
            rarity="S",
            image=None,
            speed="40",
            power="2",
            health="2",
            game_text="Accuracy 1\rFocus 1"
        )
        rebel_soldier.wrap_text()
        rebel_soldier.write_psd()

    def test_three_lines(self):
        tri_fighter_squadron = Subordinate(
            name="Tri-Fighter Squadron",
            typeline="Subordinate - Space/Character - Separatist Trade Federation Droid Squadron",
            expansion="BF",
            side="D",
            rarity="S",
            image=None,
            speed="60",
            power="4",
            health="2",
            game_text="Whenever this unit is attacked, take 1 60/1/1 Elite Buzz Droid Subordinate with \"Foresight: "
                      "Do 1 damage to the defending unit\" and put it into the Space arena."
        )
        tri_fighter_squadron.wrap_text()
        tri_fighter_squadron.write_psd()
