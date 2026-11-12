# Duel of Heroes

A turn-based duel simulator with a Tkinter interface. You play one hero against a simple AI opponent.

## Requirements

- Python 3
- Tkinter (bundled with most Python installs)

## Run

```bash
git clone https://github.com/NanteRhak/duel_heroes
cd duel_heroes
python main.py
```

## How to play

Type a name for each hero, pick Warrior, Mage or Archer, then start the duel. On your turn, choose one action:

- **Attack** — basic damage.
- **Special** — costs energy; each class has its own.
- **Defend** — halves the next incoming hit.
- **Recharge** — restores 10 energy.

Reduce the opponent to 0 HP to win. This is single-player: player 2 is controlled by a simple AI.
