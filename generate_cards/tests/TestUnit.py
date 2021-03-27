import unittest

from generate_cards.Unit import Unit


class TestUnit(unittest.TestCase):
    def test_7pt(self):
        dash_rendar_b = Unit(
            name="Dash Rendar",
            typeline="Character - Independent Smuggler",
            expansion="SAV",
            side="N",
            rarity="R",
            image=None,
            cost="7",
            speed="40",
            power="5",
            health="5",
            number="5",
            game_text="Bounty: Draw a card.\rDash gets +1 power and +1 health for each Equipment attached to him.",
            flavor_text="Dash's impressive arsenal of weaponry earned him respect and fear from fellow mercenaries.",
            version="B"
        )
        dash_rendar_b.wrap_text()
        dash_rendar_b.write_psd()

    def test_6_5pt(self):
        boba_fett_i = Unit(
            name="Boba Fett",
            typeline="Character - Bounty Hunter",
            expansion="SAV",
            side="N",
            rarity="R",
            image=None,
            cost="8",
            speed="50",
            power="6",
            health="6",
            number="1",
            game_text="Bounty: You may search your deck for a Boba Fett card, show it to your opponent, and put it "
                      "into your hand. Shuffle your deck\rArmor\rWhen the Character battle step starts, choose one: "
                      "Boba gets +20 speed until end of turn. Or: Boba gets +2 power until end of turn.",
            flavor_text="\"Reality doesn't care if you believe it.\"",
            version="I"
        )
        boba_fett_i.wrap_text()
        boba_fett_i.write_psd()

    def test_tap_arrow(self):
        jango_fett_h = Unit(
            name="Jango Fett",
            typeline="Character - Bounty Hunter",
            expansion="SAV",
            side="D",
            rarity="R",
            image=None,
            cost="7",
            speed="40",
            power="6",
            health="5",
            number="13",
            game_text="Stealth <i>(Jango cannot be attacked unless he is tapped or damaged.)</i>\r[tap], Do one damage "
                      "to Jango -> Disrupt a Battle or Mission card.",
            flavor_text="Jango's toxic darts silenced Zam Wesell and nearly left Obi-Wan and Anakin at a dead end.",
            version="H"
        )
        jango_fett_h.wrap_text()
        jango_fett_h.write_psd()

    def test_tap_array_small(self):
        darth_sidious_i = Unit(
            name="Darth Sidious",
            typeline="Character - Dark Jedi Master Sith Lord",
            expansion="FOTR",
            side="D",
            rarity="R",
            image=None,
            cost="9",
            speed="40",
            power="4",
            health="5",
            number="12",
            game_text="Pay 2 Force -> Evade 2\r[tap], Pay X Force -> Gain control of one of your opponent's Clone "
                      "units with total build cost X until end of game. If your opponent has no Clone units in play, "
                      "put a Clone unit card with total build cost X from your hand into its arena untapped. Sidious "
                      "can't untap until the next turn ends.",
            flavor_text="\"The time has come. Execute Order Sixty-Six\"",
            version="I"
        )
        darth_sidious_i.wrap_text()
        darth_sidious_i.write_psd()

    def test_pilot_bullet(self):
        nym_a = Unit(
            name="Nym",
            typeline="Character - Feeorin Pirate",
            expansion="SAV",
            side="N",
            rarity="R",
            image="SAV021_Nym_A",
            cost="5",
            speed="30",
            power="5",
            health="4",
            number="21",
            game_text="[Pilot] Starfighter Pilot. The Starfighter gets:\r\u2022 +1 power\r\u2022 Armor",
            flavor_text="\"Furious!\"",
            version="A"
        )
        nym_a.wrap_text()
        nym_a.write_psd()

    def test_photoshop_image(self):
        commander_iden_versio_a = Unit(
            name="Commander Iden Versio",
            typeline="Character - Imperial Officer",
            expansion="BF",
            side="D",
            rarity="R",
            image="BF005_Commander_Iden_Versio_A.psd",
            cost="6",
            speed="60",
            power="5",
            health="5",
            number="5",
            game_text="When the battle phase starts, if Dio is not in play, take 1 70/2/1 Dio Subordinate with "
                      "\"Critical Hit 2\" and put it into the Character arena.\r[Pilot] Squad, Squadron, and "
                      "Starfighter Pilot. The Squad, Squadron, or Starfighter gets:\r\u2022 +3 power\r\u2022 Avenge X, "
                      "where X is this unit's total power.",
            flavor_text="\"Avenge our Emperor!\"",
            version="A"
        )
        commander_iden_versio_a.wrap_text()
        commander_iden_versio_a.write_psd()

    def test_photoshop_image2(self):
        climate_disruption_array = Unit(
            name="Climate Disruption Array",
            typeline="Space - Imperial Fortification",
            expansion="BF",
            side="D",
            rarity="R",
            image="BF003_Climate_Disruption_Array.psd",
            cost="4",
            speed="20",
            power="2",
            health="5",
            number="3",
            game_text="[tap] -> One of your opponent's Locations loses its game text until end of turn. Play only "
                      "during your build step.\rPay 2 Force -> Choose one: Disrupt a Space unit's activated ability. "
                      "Or: Remove 1 counter from your opponent's Resource.",
            flavor_text="\"The satellites are aligned.\" \u2014Imperial officer"
        )
        climate_disruption_array.wrap_text()
        climate_disruption_array.write_psd()

    def test_tap_quote(self):
        emperor_palpatine_q = Unit(
            name="Emperor Palpatine",
            typeline="Character - Imperial Dark Jedi Master - Sith Lord",
            expansion="BF",
            side="D",
            rarity="R",
            image="BF012_Emperor_Palpatine_Q.psd",
            cost="10",
            speed="30",
            power="7",
            health="6",
            number="12",
            game_text="Forewarning: Gain 3 Force.\rWhen you deploy Palpatine or whenever he is attacked, you may pay "
                      "3 Force. If you do, take 1 30/3/3 Imperial Royal Guards Subordinate with \"Armor\" and \"[tap] "
                      "-> Protect 3\" and put it into the Ground or Character arena.\rPay 3 Force -> Deflect 2",
            flavor_text="\"Your master has arrived.\"",
            version="Q"
        )
        emperor_palpatine_q.wrap_text()
        emperor_palpatine_q.write_psd()

    def test_name_italics(self):
        corvus_b = Unit(
            name="<i>Corvus</i>",
            typeline="Space - New Republic Capital Ship",
            expansion="BF",
            side="L",
            rarity="R",
            image="BF008_Corvus_B.psd",
            cost="8",
            speed="30",
            power="5",
            health="5",
            number="8",
            game_text="Damage Control 2\rInspiration\r<i>Corvus</i> gets +1 power and Ferocity when attacking a Dark "
                      "Side unit.\rBombard 3",
            flavor_text="After Iden Versio's defection to the Rebels, the <i>Corvus</i> serves the New Republic.",
            version="B"
        )
        corvus_b.wrap_text()
        corvus_b.write_psd()

    def test_long_typeline(self):
        inferno_squad_b = Unit(
            name="Inferno Squad",
            typeline="Space/Ground - New Republic Soldier Squad - Squadron",
            expansion="BF",
            side="L",
            rarity="R",
            image="BF019_Inferno_Squad_B.psd",
            cost="8",
            speed="50",
            power="6",
            health="7",
            number="19",
            game_text="Switch: Shields 1/Focus 1, Precision\rReduced Cost 7: If you have a unit in the Character "
                      "arena. <i>(Inferno Squad's build cost is 7 if the listed condition is met.)</i>\rResilience 2",
            flavor_text="\"We've been fighting our whole lives. It's taken us too long to realize that we were "
                        "fighting for the wrong side. . . .\" \u2014Commander Iden Versio",
            version="B"
        )
        inferno_squad_b.wrap_text()
        inferno_squad_b.write_psd()
