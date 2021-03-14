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

    def test_equipment(self):
        pulse_cannon = NonUnit(
            name="Pulse Cannon",
            typeline="Equipment - Ground/Character - Blaster Weapon",
            expansion="BF",
            side="N",
            rarity="U",
            image="BF047_Pulse_Cannon.psd",
            number="47",
            cost="3",
            game_text="Pay 1 build point -> Equip\rEquipped Character or Squad gets +1 power, Critical Hit 2, Overkill "
                      "and \"Whenever this unit attacks, the defending unit loses Armor for that attack.\"",
            flavor_text="\"Think that armor's gonna help?\" \u2014Rebel soldier"
        )
        pulse_cannon.wrap_text()
        pulse_cannon.write_psd()

    def test_equipment_unique(self):
        boba_fett_s_jetpack_a = NonUnit(
            name="Boba Fett's Jetpack",
            typeline="Equipment - Character",
            expansion="SAV",
            side="N",
            rarity="R",
            image=None,
            number="2",
            cost="2",
            game_text="Pay 1 build point -> Equip\rEquipped Character unit gets +20 speed.\rEquipped Boba Fett also "
                      "gets \"Pay 0 Force -> Evade 1.\"",
            flavor_text="Boba Fett's Mitrinomon Z-6 jetpack has saved the bouty hunter's life on numerous occasions.",
            version="A"
        )
        boba_fett_s_jetpack_a.wrap_text()
        boba_fett_s_jetpack_a.write_psd()

    def test_skill(self):
        sharpshooter_training = NonUnit(
            name="Sharpshooter Training",
            typeline="Equipment - Ground/Character - Skill",
            expansion="BF",
            side="N",
            rarity="R",
            image="BF028_Sharpshooter_Training.psd",
            number="28",
            cost="3",
            game_text="Remove 1 counter from your Resource -> Equip\rEquipped Character or Squad gets Accuracy 1 and "
                      "Precision.\rEquipped unique Character or Squad also gets \"This unit can attack Ground units "
                      "and Characters in your opponent's build zone.\""
        )
        sharpshooter_training.wrap_text()
        sharpshooter_training.write_psd()

    def test_resource(self):
        imperial_production_line = NonUnit(
            name="Imperial Production Line",
            typeline="Resource",
            expansion="BF",
            side="D",
            rarity="U",
            image="BF042_Imperial_Production_Line.psd",
            number="42",
            cost="5",
            game_text="Add 2 counters -> Gain 1 build point and draw a card. Play only if you have a Location in any "
                      "arena and only during your build step.\rRemove 6 counters -> Reveal up to 3 partially built "
                      "Imperial unit cards in your build zone to your opponent and put up to 3 total build counters "
                      "divided as you choose on them. Play only during your build step."
        )
        imperial_production_line.wrap_text()
        imperial_production_line.write_psd()

    def test_event(self):
        battlefront = NonUnit(
            name="Battlefront",
            typeline="Event",
            expansion="BF",
            side="N",
            rarity="R",
            image="BF001_Battlefront.psd",
            number="1",
            game_text="Each player can have 1 Location in each arena at the same time.\rWhenever a player completes "
                      "a Location, don't discard another player's Location <i>(if any)</i> in the same arena.\r"
                      "As long as a player controls an arena, his or her opponent's Location in that arena loses its "
                      "game text."
        )
        battlefront.wrap_text()
        battlefront.write_psd()

    def test_trap(self):
        sabotage = NonUnit(
            name="Sabotage",
            typeline="Mission - Trap",
            expansion="BF",
            side="N",
            rarity="U",
            image="BF049_Sabotage.psd",
            number="49",
            cost="X",
            game_text="When you deploy or put a Spy or a unit with Stealth into any arena, remove X counters from a "
                      "partially built card in your opponent's build zone.\rPay X+2 Force -> Meditate"
        )
        sabotage.wrap_text()
        sabotage.write_psd()

    def test_campaign(self):
        operation_cinder = NonUnit(
            name="Operation: Cinder",
            typeline="Mission - Campaign",
            expansion="BF",
            side="D",
            rarity="U",
            image="BF046_Operation_Cinder.psd",
            number="46",
            cost="3",
            game_text="When each turn starts, if your opponent has more units in the Ground arena than you do, you "
                      "may take 1 20/1/1 Imperial Sentinel Messenger Subordinate with \"Upkeep: Gain 1 build point\" "
                      "and put it into the Character arena. If you do, put 1 damage counter on one of your units in "
                      "the Ground or Character arena."
        )
        operation_cinder.wrap_text()
        operation_cinder.write_psd()

    def test_scaling(self):
        trained_in_the_arts = NonUnit(
            name="Trained in the Arts",
            typeline="Battle",
            expansion="FOTR",
            side="N",
            rarity="C",
            image=None,
            number="109",
            game_text="Pay 1 Force -> Choose one of your units in any arena. That unit gets Parry 1 until end of turn. "
                      "<i>(When that unit is attacked, prevent 1 damage if the attacking unit rolls at least one "
                      "natural 1.)</i>\rEnhance: Pay 3 more Force -> Each of your units in that arena gets Parry 1 "
                      "until end of turn instead.",
            flavor_text="\"You fool! I've been trained in your Jedi arts by Count Dooku.\" \u2014General Grievous"
        )
        trained_in_the_arts.wrap_text()
        trained_in_the_arts.write_psd()
