from hanoi_crossing.model import (
    GameState,
    Lift,
    Observation,
    Place,
    Player,
    Pole,
    Skip,
)


def observe(state, player):
    if player is Player.A:
        return Observation(
            player,
            list(state.pole_1a),
            list(state.pole_2),
            list(state.pole_3a),
            state.hand_a,
        )
    return Observation(
        player,
        list(state.pole_1b),
        list(state.pole_2),
        list(state.pole_3b),
        state.hand_b,
    )


def has_won(obs):
    return (
        obs.hand is None
        and not obs.pole_1
        and not obs.pole_2
        and bool(obs.pole_3)
    )


def legal_actions(obs):
    actions = [Skip()]
    poles = {
        Pole.ONE: obs.pole_1,
        Pole.TWO: obs.pole_2,
        Pole.THREE: obs.pole_3,
    }

    if obs.hand is None:
        for pole, stack in poles.items():
            if stack:
                actions.append(Lift(pole))
    else:
        for pole, stack in poles.items():
            if not stack or stack[-1] > obs.hand:
                actions.append(Place(pole))

    return actions


def _pole_stack(state, player, pole):
    if pole is Pole.TWO:
        return state.pole_2
    if player is Player.A:
        return state.pole_1a if pole is Pole.ONE else state.pole_3a
    return state.pole_1b if pole is Pole.ONE else state.pole_3b


def _hand(state, player):
    if player is Player.A:
        return state.hand_a
    return state.hand_b


def _set_hand(state, player, disk):
    if player is Player.A:
        state.hand_a = disk
    else:
        state.hand_b = disk


def step(state, player, action):
    if isinstance(action, Skip):
        return True

    hand = _hand(state, player)

    if isinstance(action, Lift):
        if hand is not None:
            return False
        stack = _pole_stack(state, player, action.pole)
        if not stack:
            return False
        _set_hand(state, player, stack.pop())
        return True

    if isinstance(action, Place):
        if hand is None:
            return False
        stack = _pole_stack(state, player, action.pole)
        if stack and stack[-1] <= hand:
            return False
        stack.append(hand)
        _set_hand(state, player, None)
        return True

    return False


class Game:
    def __init__(self, n, turn_order):
        self._state = GameState(n)
        self._turn_order = list(turn_order)
        self._turn = 0
        self.winner = None

    @property
    def done(self):
        return self.winner is not None or self._turn >= len(self._turn_order)

    @property
    def current_player(self):
        if self.done:
            return None
        return self._turn_order[self._turn]

    def observe(self):
        if self.done:
            return None
        return observe(self._state, self.current_player)

    def legal_actions(self):
        observation = self.observe()
        if observation is None:
            return []
        return legal_actions(observation)

    def snapshot(self):
        return {
            "poles": {
                "1a": list(self._state.pole_1a),
                "2": list(self._state.pole_2),
                "3a": list(self._state.pole_3a),
                "1b": list(self._state.pole_1b),
                "3b": list(self._state.pole_3b),
            },
            "hands": {
                "A": self._state.hand_a,
                "B": self._state.hand_b,
            },
        }

    def step(self, action):
        if self.done:
            return False

        player = self.current_player
        applied = step(self._state, player, action)

        if applied and has_won(observe(self._state, player)):
            self.winner = player

        self._turn += 1
        return applied
