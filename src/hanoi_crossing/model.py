from enum import Enum


class Player(Enum):
    A = "A"
    B = "B"


class Pole(Enum):
    ONE = "1"
    TWO = "2"
    THREE = "3"


class Lift:
    def __init__(self, pole):
        self.pole = pole


class Place:
    def __init__(self, pole):
        self.pole = pole


class Skip:
    pass


class Observation:
    def __init__(self, player, pole_1, pole_2, pole_3, hand):
        self.player = player
        self.pole_1 = pole_1
        self.pole_2 = pole_2
        self.pole_3 = pole_3
        self.hand = hand


class GameState:
    def __init__(self, n):
        self.pole_1a = [2 * i - 1 for i in range(n, 0, -1)]
        self.pole_2 = []
        self.pole_3a = []
        self.pole_1b = [2 * i for i in range(n, 0, -1)]
        self.pole_3b = []
        self.hand_a = None
        self.hand_b = None
