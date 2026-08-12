import argparse
import json
import random

from hanoi_crossing.engine import Game
from hanoi_crossing.model import Lift, Place, Player, Pole, Skip
from hanoi_crossing.player import play_random


def parse_action(data):
    name = data["action"].lower()
    if name == "skip":
        return Skip()

    pole = Pole(str(data["pole"]))
    if name == "lift":
        return Lift(pole)
    if name == "place":
        return Place(pole)
    raise ValueError(f"Unknown action: {name}")


def action_data(action):
    if isinstance(action, Skip):
        return {"action": "skip"}
    return {
        "action": "lift" if isinstance(action, Lift) else "place",
        "pole": action.pole.value,
    }


def result_data(game, moves):
    return {
        "winner": game.winner.value if game.winner else None,
        "moves": moves,
        "state": game.snapshot(),
    }


def replay(path):
    with open(path, encoding="utf-8") as replay_file:
        data = json.load(replay_file)

    turn_order = [Player(player) for player in data["turn_order"]]
    game = Game(data["n"], turn_order)
    moves = []

    for move in data["moves"]:
        if game.done:
            break
        player = game.current_player
        action = parse_action(move)
        applied = game.step(action)
        moves.append(
            {
                "player": player.value,
                **action_data(action),
                "applied": applied,
            }
        )

    return result_data(game, moves)


def random_game(n, turns, seed=None):
    rng = random.Random(seed)
    turn_order = [rng.choice([Player.A, Player.B]) for _ in range(turns)]
    game = Game(n, turn_order)
    history = play_random(game, rng)
    moves = [
        {"player": player.value, **action_data(action)}
        for player, action in history
    ]
    return result_data(game, moves)


def main():
    parser = argparse.ArgumentParser(prog="hanoi-crossing")
    commands = parser.add_subparsers(dest="command", required=True)

    replay_parser = commands.add_parser("replay")
    replay_parser.add_argument("file")

    random_parser = commands.add_parser("random")
    random_parser.add_argument("--n", type=int, default=3)
    random_parser.add_argument("--turns", type=int, default=100)
    random_parser.add_argument("--seed", type=int)

    args = parser.parse_args()

    try:
        if args.command == "replay":
            result = replay(args.file)
        else:
            result = random_game(args.n, args.turns, args.seed)
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
