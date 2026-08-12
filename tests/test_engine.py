import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from hanoi_crossing.engine import has_won, observe, step
from hanoi_crossing.model import GameState, Lift, Place, Player, Pole, Skip


class TestStep(unittest.TestCase):
    def test_example_n1(self):
        state = GameState(1)

        self.assertTrue(step(state, Player.A, Lift(Pole.ONE)))
        self.assertEqual(state.hand_a, 1)
        self.assertEqual(state.pole_1a, [])

        self.assertTrue(step(state, Player.B, Lift(Pole.ONE)))
        self.assertEqual(state.hand_b, 2)

        self.assertTrue(step(state, Player.A, Place(Pole.THREE)))
        self.assertIsNone(state.hand_a)
        self.assertEqual(state.pole_3a, [1])
        self.assertTrue(has_won(observe(state, Player.A)))

    def test_illegal_lift_leaves_state_unchanged(self):
        state = GameState(1)
        before = (list(state.pole_1a), state.hand_a)

        self.assertFalse(step(state, Player.A, Lift(Pole.TWO)))
        self.assertEqual((list(state.pole_1a), state.hand_a), before)

    def test_illegal_place_leaves_state_unchanged(self):
        state = GameState(2)
        step(state, Player.A, Lift(Pole.ONE))
        step(state, Player.A, Place(Pole.TWO))
        step(state, Player.A, Lift(Pole.ONE))

        self.assertFalse(step(state, Player.A, Place(Pole.TWO)))
        self.assertEqual(state.hand_a, 3)
        self.assertEqual(state.pole_2, [1])

    def test_skip(self):
        state = GameState(1)
        before = (list(state.pole_1a), list(state.pole_1b))
        self.assertTrue(step(state, Player.A, Skip()))
        self.assertEqual((list(state.pole_1a), list(state.pole_1b)), before)


if __name__ == "__main__":
    unittest.main()
