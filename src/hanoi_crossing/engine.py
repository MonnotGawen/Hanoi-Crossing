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
        and obs.pole_3
    )


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
