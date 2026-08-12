from hanoi_crossing.model import GameState, Observation, Player


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
