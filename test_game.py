import unittest

from core.game import Game


class GameTest(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.assertTrue(self.game.creer_personnage("guerrier", "A", 1))
        self.assertTrue(self.game.creer_personnage("mage", "B", 2))
        self.assertTrue(self.game.demarrer_combat())

    def test_attack_reduces_hp_and_passes_turn(self):
        self.game.executer_action("attaquer")
        self.assertEqual(self.game.joueur2.pv, 85)
        self.assertEqual(self.game.get_etat_combat()["tour"], 2)

    def test_reported_damage_cannot_exceed_remaining_hp(self):
        self.game.joueur2.pv = 5
        self.game.executer_action("attaquer")
        self.assertEqual(self.game.joueur2.pv, 0)
        self.assertTrue(any("(-5 PV)" in ligne for ligne in self.game.historique))
        self.assertFalse(any("(-15 PV)" in ligne for ligne in self.game.historique))

    def test_ai_uses_a_special_then_returns_the_turn(self):
        self.game.executer_action("attaquer")
        ok, fini = self.game.executer_action_ia()
        self.assertTrue(ok)
        self.assertFalse(fini)
        self.assertEqual(self.game.joueur2.energie, 20)
        self.assertEqual(self.game.get_etat_combat()["tour"], 1)

    def test_ai_recharges_when_it_cannot_pay(self):
        self.game.executer_action("attaquer")
        self.game.executer_action_ia()
        self.game.executer_action("attaquer")
        ok, fini = self.game.executer_action_ia()
        self.assertTrue(ok)
        self.assertFalse(fini)
        self.assertEqual(self.game.joueur2.energie, 30)
        self.assertEqual(self.game.get_etat_combat()["tour"], 1)


if __name__ == "__main__":
    unittest.main()
