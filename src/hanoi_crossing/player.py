import random


def play_random(game):
    moves = []

    while not game.done:
        observation = game.observe()
        action = random.choice(game.legal_actions())
        game.step(action)
        moves.append((observation.player, action))

    return moves
