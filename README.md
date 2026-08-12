# Hanoi Crossing

Hanoi Crossing is a two-player, partial-information variation of Tower of
Hanoi. Each player owns two private poles, while the middle pole is shared.
Player A starts with odd disks and player B with even disks.

This repository contains a reusable game engine and two small frontends:

- `replay` reads a recorded game from JSON and prints its final state;
- `random` generates a turn order and lets both players choose random valid
  actions.

The engine uses only the Python standard library and stays below the
500-line limit.

## Setup

Python 3.10 or newer is required. No runtime dependency is needed.

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
python -m pip install -e .
```

On Linux or macOS, activate the environment with:

```bash
source env/bin/activate
```

The editable installation provides the `hanoi-crossing` command.

## Usage

Replay the example from the assignment:

```powershell
hanoi-crossing replay examples/official_n1.json
```

Other examples demonstrate an illegal action, an illegal Hanoi placement and
interaction through the shared pole:

```powershell
hanoi-crossing replay examples/illegal_action.json
hanoi-crossing replay examples/illegal_hanoi_place.json
hanoi-crossing replay examples/shared_pole.json
```

Run a random game:

```powershell
hanoi-crossing random --n 3 --turns 200 --seed 42
```

Both the turn order and the actions are random. A local random generator is
used, so a seed makes the complete simulation reproducible. The turn limit
prevents a random game from running forever.

The CLI prints JSON containing the moves, the winner (if any), and a snapshot
of the final board.

## Replay format

```json
{
  "n": 1,
  "turn_order": ["A", "B", "A"],
  "moves": [
    {"action": "lift", "pole": "1"},
    {"action": "lift", "pole": "1"},
    {"action": "place", "pole": "3"}
  ]
}
```

`n` is the number of disks initially owned by each player. Pole names are
relative to the acting player: `1` is that player's starting pole, `2` is the
shared pole, and `3` is that player's target pole.

The turn order is independent from the moves and may contain any sequence of
players, including repeated turns. A move rejected by the engine is reported
with `"applied": false`.

## Tests

The tests exercise the engine directly and use the standard library
`unittest` module:

```powershell
python -m unittest discover -s tests -v
```

They cover initialization, observations, legal and illegal actions, Hanoi
placement, arbitrary turn orders, both victory paths, and interaction through
the shared pole.

## Design decisions

### Engine boundary

`Game` owns the complete state. External players use three methods:

```python
observation = game.observe()
actions = game.legal_actions()
applied = game.step(action)
```

`step()` is the transition boundary used by both frontends. The random player
does not inspect the private state. `snapshot()` is an administrative view
used by the replay and random frontends to serialize a final result; it is not
part of the information available to a player choosing an action.

Each observation contains copies of the current player's private poles, the
shared pole and that player's hand. It contains no opponent hand or private
pole, and changing an observation cannot change the game state.

### State and rules

Pole lists are stored from bottom to top, making the last item the disk that
can be lifted. Actions are represented by the small `Lift`, `Place`, and
`Skip` classes.

The victory rule is implemented literally: the acting player's hand and visible poles 1 and 2 must be empty, while visible pole 3 must contain disks. I interpret the alternative case where pole 3 is also empty as not being a win, since that could allow a player to win simply because their disks were moved out of their visible area. Consequently, a disk left by the opponent on the shared pole prevents a win.

An illegal action leaves the state unchanged but still consumes the turn, as
specified by the assignment. `Skip` is always legal and also consumes a turn.

The engine never assumes alternating players. `Game` receives the complete
turn order from its caller. A game is done when a player wins or when this
sequence is exhausted. The random frontend generates an arbitrary order as a
convenience; this policy is not part of the engine.

## Reinforcement learning perspective

The public interface maps naturally to an environment loop:

```python
while not game.done:
    observation = game.observe()
    action = agent.act(observation, game.legal_actions())
    game.step(action)
```

A simple terminal reward could be +1 for winning and 0 otherwise. Once a reliable terminal 
objective is established, efficiency could be incorporated through a secondary penalty on game length. However, reward shaping should remain secondary to the actual game objective to avoid introducing unintended shortcuts.

The full game can also be described as a graph: a node contains the poles,
hands and current turn, and an edge is a state transition caused by an action.
For small configurations, graph search can provide a shortest-path baseline.
An RL policy can then be compared with that baseline through win rate, path
length or regret. This comparison needs care: Hanoi Crossing is partially
observable, has another acting player, and accepts arbitrary turn orders, so
it is closer to a game graph than to a deterministic single-agent shortest
path problem. A full-state search oracle is therefore useful for evaluation,
but its private information should not leak into the agent's observation.

### Reasoning evaluation and verifiable rewards

This assignment reminded me directly of Apple's
[The Illusion of Thinking](https://machinelearning.apple.com/research/illusion-of-thinking),
which I discussed in an article in 2025. The paper uses controllable puzzles,
including Tower of Hanoi, to study how reasoning and non-reasoning models
behave as problem complexity increases. The paper identifies three qualitative regimes: reasoning and non-reasoning models perform similarly on low-complexity instances, reasoning models gain an advantage as complexity increases, and performance eventually collapses for both at sufficiently high complexity.
A particularly interesting result is that providing the solution algorithm does not remove the collapse.
This raises a useful distinction between knowing a procedure and reliably
executing it over a long horizon.

I would not interpret these experiments as proving that reasoning itself is
an illusion. They provide a controlled way to expose limitations that public
benchmarks may hide, while leaving open questions about output constraints,
tool use, and how algorithm-guided non-reasoning models would compare. Hanoi
Crossing could support similar experiments: complexity can be increased with
`n`, every action can be verified, and failures can be localized to a precise
transition rather than only a final answer.

[Absolute Zero](https://arxiv.org/abs/2505.03335) offers the complementary
training perspective. Instead of using a controlled environment only to
evaluate reasoning, it uses self-generated tasks and automatically verifiable
outcomes as an RL signal. This engine could play the role of such a verifier
for self-play. Verifiable rewards are especially effective in code,
mathematics, games, formal reasoning and simulation, but verification against
a specification is not the same as alignment with human intent. In this
project, shortest-path efficiency is measurable, yet it should not replace
legality, victory and partial-information constraints in the reward.

## AI usage

I used Cursor as pair-programming and review tools. IT helped
with initial scaffolding, discussing ambiguous rules, identifying edge cases,
and editing documentation. I selected the architecture and interpretations,
reviewed the generated suggestions, kept the implementation deliberately
small, and ran every test and frontend locally.

## Next steps

With more time, I would:

- add type hints and clearer action representations;
- separate terminal status from turn-order exhaustion in the result;
- add property-based tests for state invariants;
- benchmark search algorithms on small full-state game graphs;
- Add deterministic reproducibility and explicit game statistics (win rate, invalid-action rate, 
average episode length).
- build a self-play environment wrapper and compare learned policies against
  search baselines;
- add persistence and batch execution for concurrent simulations.
