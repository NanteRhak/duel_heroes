from core.characters import Warrior, Mage, Archer


class Game:
    def __init__(self):
        """Hold the duel state."""
        self.player1 = None
        self.player2 = None
        self.turn = None
        self.is_combat_over = False
        self.history = []
        self.winner = None

    def create_character(self, character_class, name, player_number):
        """Create a hero for player 1 or 2."""
        if character_class.lower() == 'warrior':
            character = Warrior(name)
        elif character_class.lower() == 'mage':
            character = Mage(name)
        elif character_class.lower() == 'archer':
            character = Archer(name)
        else:
            return False

        if player_number == 1:
            self.player1 = character
        else:
            self.player2 = character
        return True

    def start_combat(self):
        """Reset both heroes and start a new duel."""
        if self.player1 and self.player2:
            self.turn = 1
            self.is_combat_over = False
            for player in (self.player1, self.player2):
                player.hp = player.max_hp
                player.energy = player.max_energy
                player.is_defending = False
            self.history = [
                f"The duel begins! {self.player1.name} vs {self.player2.name}",
                f"{self.player1.name}'s turn!"
            ]
            self.winner = None
            return True
        return False

    def perform_action(self, action):
        """Run one action for the current player and return (ok, finished)."""
        if self.turn is None or self.is_combat_over:
            return False, False

        current = self.get_current_player()
        opponent = self.player2 if current is self.player1 else self.player1

        if action == 'attack':
            result = current.attack(opponent)
        elif action == 'special':
            result = current.special_attack(opponent)
            if not result:
                return False, False
        elif action == 'defend':
            current.defend()
            result = f"{current.name} takes a defensive stance"
        elif action == 'recharge':
            current.recharge_energy()
            result = f"{current.name} recharges energy"
        else:
            return False, False

        self.history.append(result)

        if opponent.is_ko():
            self.winner = current
            self.history.append(f"{current.name} wins the duel!")
            self.is_combat_over = True
            return True, True

        self.next_turn()
        self.history.append(f"{self.get_current_player().name}'s turn!")

        return True, False

    def perform_ai_action(self):
        """Special attack if affordable, otherwise recharge."""
        if self.turn is None or self.is_combat_over:
            return False, False
        player = self.get_current_player()
        action = 'special' if player.energy >= player.special_cost else 'recharge'
        return self.perform_action(action)

    def get_current_player(self):
        """Return the hero whose turn it is."""
        return self.player1 if self.turn == 1 else self.player2

    def next_turn(self):
        """Switch turns and clear the new player's defence."""
        self.turn = 2 if self.turn == 1 else 1
        self.get_current_player().is_defending = False

    def current_player_number(self):
        """Return 1 or 2 for the current player."""
        return self.turn

    def get_state(self):
        """Return both heroes' stats, the history and the current player."""
        player1_data = {
            'name': self.player1.name,
            'hp': self.player1.hp,
            'energy': self.player1.energy
        } if self.player1 else {'name': 'Player 1', 'hp': 0, 'energy': 0}

        player2_data = {
            'name': self.player2.name,
            'hp': self.player2.hp,
            'energy': self.player2.energy
        } if self.player2 else {'name': 'Player 2', 'hp': 0, 'energy': 0}

        return {
            'player1': player1_data,
            'player2': player2_data,
            'history': self.history,
            'turn': self.current_player_number()
        }
