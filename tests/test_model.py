import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from hanoi_crossing.engine import has_won, observe
from hanoi_crossing.model import GameState, Player


class TestModel(unittest.TestCase):
    def test_game_requires_at_least_one_disk(self):
        with self.assertRaises(ValueError):
            GameState(0)

    def test_new_game_n1(self):
        state = GameState(1)
        self.assertEqual(state.pole_1a, [1])
        self.assertEqual(state.pole_1b, [2])
        self.assertEqual(state.pole_2, [])

    def test_observe_hides_opponent_poles(self):
        state = GameState(1)
        obs_a = observe(state, Player.A)
        obs_b = observe(state, Player.B)

        self.assertEqual(obs_a.pole_1, [1])
        self.assertEqual(obs_a.pole_2, [])
        self.assertEqual(obs_a.pole_3, [])
        self.assertIsNone(obs_a.hand)

        self.assertEqual(obs_b.pole_1, [2])
        self.assertEqual(obs_b.pole_2, [])
        self.assertEqual(obs_b.pole_3, [])

    def test_nobody_wins_at_start(self):
        state = GameState(1)
        self.assertFalse(has_won(observe(state, Player.A)))
        self.assertFalse(has_won(observe(state, Player.B)))


if __name__ == "__main__":
    unittest.main()
