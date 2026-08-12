import random


def play_random(game, rng=None):
    rng = rng or random.Random()
    moves = []

    while not game.done:
        observation = game.observe()
        action = rng.choice(game.legal_actions())
        game.step(action)
        moves.append((observation.player, action))

    return moves
