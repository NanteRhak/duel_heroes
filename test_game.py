import unittest

from core.game import Game


class GameTest(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.assertTrue(self.game.create_character("warrior", "A", 1))
        self.assertTrue(self.game.create_character("mage", "B", 2))
        self.assertTrue(self.game.start_combat())

    def test_attack_reduces_hp_and_passes_turn(self):
        self.game.perform_action("attack")
        self.assertEqual(self.game.player2.hp, 85)
        self.assertEqual(self.game.get_state()["turn"], 2)

    def test_reported_damage_cannot_exceed_remaining_hp(self):
        self.game.player2.hp = 5
        self.game.perform_action("attack")
        self.assertEqual(self.game.player2.hp, 0)
        self.assertTrue(any("(-5 HP)" in line for line in self.game.history))
        self.assertFalse(any("(-15 HP)" in line for line in self.game.history))

    def test_ai_uses_a_special_then_returns_the_turn(self):
        self.game.perform_action("attack")
        ok, finished = self.game.perform_ai_action()
        self.assertTrue(ok)
        self.assertFalse(finished)
        self.assertEqual(self.game.player2.energy, 20)
        self.assertEqual(self.game.get_state()["turn"], 1)

    def test_ai_recharges_when_it_cannot_pay(self):
        self.game.perform_action("attack")
        self.game.perform_ai_action()
        self.game.perform_action("attack")
        ok, finished = self.game.perform_ai_action()
        self.assertTrue(ok)
        self.assertFalse(finished)
        self.assertEqual(self.game.player2.energy, 30)
        self.assertEqual(self.game.get_state()["turn"], 1)

    def test_defend_halves_next_hit_once(self):
        self.game.perform_action("defend")
        self.game.perform_action("attack")
        self.assertEqual(self.game.player1.hp, 90)
        self.game.perform_action("attack")
        self.assertEqual(self.game.player2.hp, 85)
        self.game.perform_action("attack")
        self.assertEqual(self.game.player1.hp, 70)

    def test_special_without_energy_is_refused_and_keeps_the_turn(self):
        self.game.perform_action("special")
        self.game.perform_action("recharge")
        self.game.perform_action("special")
        self.game.perform_action("recharge")
        hp_before = self.game.player2.hp
        ok, finished = self.game.perform_action("special")
        self.assertFalse(ok)
        self.assertFalse(finished)
        self.assertEqual(self.game.player1.energy, 10)
        self.assertEqual(self.game.player2.hp, hp_before)
        self.assertEqual(self.game.get_state()["turn"], 1)

    def test_recharge_caps_at_maximum(self):
        self.game.perform_action("recharge")
        self.assertEqual(self.game.player1.energy, 50)
        self.assertEqual(self.game.get_state()["turn"], 2)

    def test_duel_ends_and_names_the_right_winner(self):
        g = Game()
        self.assertTrue(g.create_character("warrior", "C", 1))
        self.assertTrue(g.create_character("warrior", "D", 2))
        self.assertTrue(g.start_combat())

        finished = False
        for _ in range(50):
            ok, finished = g.perform_action("attack")
            self.assertTrue(ok)
            if finished:
                break
            ok, finished = g.perform_ai_action()
            self.assertTrue(ok)
            if finished:
                break

        self.assertTrue(finished)
        self.assertIs(g.winner, g.player1)
        self.assertEqual(g.player2.hp, 0)
        self.assertGreater(g.player1.hp, 0)

    def test_new_duel_resets_both_heroes(self):
        self.game.perform_action("attack")
        self.game.perform_ai_action()
        self.game.perform_action("defend")

        self.assertTrue(self.game.start_combat())

        for player in (self.game.player1, self.game.player2):
            self.assertEqual(player.hp, player.max_hp)
            self.assertEqual(player.energy, player.max_energy)
            self.assertFalse(player.is_defending)
        self.assertEqual(self.game.get_state()["turn"], 1)
        self.assertIsNone(self.game.winner)

    def test_new_duel_after_a_win_is_playable(self):
        finished = False
        for _ in range(50):
            ok, finished = self.game.perform_action("attack")
            self.assertTrue(ok)
            if finished:
                break
            ok, finished = self.game.perform_ai_action()
            self.assertTrue(ok)
            if finished:
                break
        self.assertTrue(finished)
        self.assertIsNotNone(self.game.winner)

        self.assertTrue(self.game.start_combat())
        ok, finished = self.game.perform_action("attack")
        self.assertTrue(ok)
        self.assertFalse(finished)

    def test_ai_never_makes_an_illegal_move_in_a_full_duel(self):
        finished = False
        for _ in range(60):
            ok, finished = self.game.perform_action("attack")
            self.assertTrue(ok)
            if finished:
                break
            ok, finished = self.game.perform_ai_action()
            self.assertTrue(ok)
            if finished:
                break

        self.assertTrue(finished)
        self.assertEqual(min(self.game.player1.hp, self.game.player2.hp), 0)
        self.assertGreaterEqual(self.game.player2.energy, 0)


if __name__ == "__main__":
    unittest.main()
