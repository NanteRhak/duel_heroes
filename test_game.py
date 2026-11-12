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

    def test_defend_halves_next_hit_once(self):
        self.game.executer_action("defendre")
        self.game.executer_action("attaquer")
        self.assertEqual(self.game.joueur1.pv, 90)
        self.game.executer_action("attaquer")
        self.assertEqual(self.game.joueur2.pv, 85)
        self.game.executer_action("attaquer")
        self.assertEqual(self.game.joueur1.pv, 70)

    def test_special_without_energy_is_refused_and_keeps_the_turn(self):
        self.game.executer_action("special")
        self.game.executer_action("recharger")
        self.game.executer_action("special")
        self.game.executer_action("recharger")
        pv_avant = self.game.joueur2.pv
        ok, fini = self.game.executer_action("special")
        self.assertFalse(ok)
        self.assertFalse(fini)
        self.assertEqual(self.game.joueur1.energie, 10)
        self.assertEqual(self.game.joueur2.pv, pv_avant)
        self.assertEqual(self.game.get_etat_combat()["tour"], 1)

    def test_recharge_caps_at_maximum(self):
        self.game.executer_action("recharger")
        self.assertEqual(self.game.joueur1.energie, 50)
        self.assertEqual(self.game.get_etat_combat()["tour"], 2)

    def test_duel_ends_and_names_the_right_winner(self):
        g = Game()
        self.assertTrue(g.creer_personnage("guerrier", "C", 1))
        self.assertTrue(g.creer_personnage("guerrier", "D", 2))
        self.assertTrue(g.demarrer_combat())

        fini = False
        for _ in range(50):
            ok, fini = g.executer_action("attaquer")
            self.assertTrue(ok)
            if fini:
                break
            ok, fini = g.executer_action_ia()
            self.assertTrue(ok)
            if fini:
                break

        self.assertTrue(fini)
        self.assertIs(g.gagnant, g.joueur1)
        self.assertEqual(g.joueur2.pv, 0)
        self.assertGreater(g.joueur1.pv, 0)

    def test_new_duel_resets_both_heroes(self):
        self.game.executer_action("attaquer")
        self.game.executer_action_ia()
        self.game.executer_action("defendre")

        self.assertTrue(self.game.demarrer_combat())

        for joueur in (self.game.joueur1, self.game.joueur2):
            self.assertEqual(joueur.pv, joueur.pv_max)
            self.assertEqual(joueur.energie, joueur.energie_max)
            self.assertFalse(joueur.is_defending)
        self.assertEqual(self.game.get_etat_combat()["tour"], 1)
        self.assertIsNone(self.game.gagnant)

    def test_ai_never_makes_an_illegal_move_in_a_full_duel(self):
        fini = False
        for _ in range(60):
            ok, fini = self.game.executer_action("attaquer")
            self.assertTrue(ok)
            if fini:
                break
            ok, fini = self.game.executer_action_ia()
            self.assertTrue(ok)
            if fini:
                break

        self.assertTrue(fini)
        self.assertEqual(min(self.game.joueur1.pv, self.game.joueur2.pv), 0)
        self.assertGreaterEqual(self.game.joueur2.energie, 0)


if __name__ == "__main__":
    unittest.main()
