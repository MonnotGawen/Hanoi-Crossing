import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from hanoi_crossing.engine import Game
from hanoi_crossing.model import Lift, Place, Player, Pole, Skip


class TestGame(unittest.TestCase):
    def test_legal_actions_with_empty_hand(self):
        game = Game(1, [Player.A])
        actions = game.legal_actions()

        self.assertEqual(len(actions), 2)
        self.assertTrue(any(isinstance(action, Skip) for action in actions))
        self.assertTrue(
            any(
                isinstance(action, Lift) and action.pole is Pole.ONE
                for action in actions
            )
        )

    def test_legal_actions_with_disk_in_hand(self):
        game = Game(1, [Player.A, Player.A])
        game.step(Lift(Pole.ONE))
        actions = game.legal_actions()

        places = [action.pole for action in actions if isinstance(action, Place)]
        self.assertEqual(places, [Pole.ONE, Pole.TWO, Pole.THREE])

    def test_legal_actions_excludes_invalid_place(self):
        game = Game(1, [Player.A, Player.A, Player.B, Player.B])
        game.step(Lift(Pole.ONE))
        game.step(Place(Pole.TWO))
        game.step(Lift(Pole.ONE))

        places = [
            action.pole
            for action in game.legal_actions()
            if isinstance(action, Place)
        ]
        self.assertNotIn(Pole.TWO, places)

    def test_game_follows_external_turn_order(self):
        game = Game(1, [Player.A, Player.B, Player.A, Player.B])

        game.step(Lift(Pole.ONE))
        self.assertEqual(game.current_player, Player.B)
        game.step(Lift(Pole.ONE))
        self.assertEqual(game.current_player, Player.A)
        game.step(Place(Pole.THREE))

        self.assertTrue(game.done)
        self.assertEqual(game.winner, Player.A)
        self.assertIsNone(game.current_player)
        self.assertFalse(game.step(Skip()))

    def test_player_b_can_win(self):
        game = Game(1, [Player.B, Player.A, Player.B])

        game.step(Lift(Pole.ONE))
        game.step(Lift(Pole.ONE))
        game.step(Place(Pole.THREE))

        self.assertEqual(game.winner, Player.B)
        self.assertTrue(game.done)

    def test_illegal_action_wastes_turn(self):
        game = Game(1, [Player.A, Player.B])

        self.assertFalse(game.step(Lift(Pole.TWO)))
        self.assertEqual(game.current_player, Player.B)

    def test_shared_pole_blocks_victory(self):
        game = Game(1, [Player.B, Player.A, Player.B, Player.A])

        game.step(Lift(Pole.ONE))
        game.step(Lift(Pole.ONE))
        game.step(Place(Pole.TWO))
        game.step(Place(Pole.THREE))

        self.assertIsNone(game.winner)
        self.assertTrue(game.done)

    def test_both_players_can_use_shared_pole(self):
        game = Game(1, [Player.A, Player.A, Player.B])

        game.step(Lift(Pole.ONE))
        game.step(Place(Pole.TWO))
        game.step(Lift(Pole.TWO))

        state = game.snapshot()
        self.assertEqual(state["poles"]["2"], [])
        self.assertEqual(state["hands"]["B"], 1)


if __name__ == "__main__":
    unittest.main()
