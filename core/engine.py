class CombatEngine:
    def __init__(self, player1, player2):
        """
        Initialise le moteur de combat avec deux joueurs
        Args:
            player1: Instance de Personnage (joueur 1)
            player2: Instance de Personnage (joueur 2)
        """
        self.players = [player1, player2]
        self.current_turn = 0  # 0 pour joueur1, 1 pour joueur2
        self.combat_log = []
        self.is_combat_over = False

    def start_combat(self):
        """Initialise les variables pour un nouveau combat"""
        self.combat_log.append("Le combat commence!")
        self._reset_players_state()

    def execute_turn(self, action, target=None):
        """
        Exécute une action pour le joueur courant
        Args:
            action: str ('attack', 'special', 'defend', 'recharge')
            target: Personnage cible (None pour défense/recharge)
        Returns:
            bool: True si l'action a été exécutée avec succès
        """
        if self.is_combat_over:
            return False

        current_player = self.players[self.current_turn]
        opponent = self.players[1 - self.current_turn]

        if action == 'attack':
            result = current_player.attack(opponent)
            self.combat_log.append(result)
        elif action == 'special':
            if current_player.energy >= current_player.special_cost:
                result = current_player.special_attack(opponent)
                self.combat_log.append(result)
            else:
                self.combat_log.append(f"{current_player.name} n'a pas assez d'énergie!")
                return False
        elif action == 'defend':
            current_player.is_defending = True
            self.combat_log.append(f"{current_player.name} se met en défense!")
        elif action == 'recharge':
            current_player.recharge_energy()
            self.combat_log.append(f"{current_player.name} recharge son énergie!")

        self._check_combat_end()
        if not self.is_combat_over:
            self._next_turn()
        
        return True

    def _next_turn(self):
        """Passe au tour suivant"""
        self.current_turn = 1 - self.current_turn
        current_player = self.players[self.current_turn]
        current_player.is_defending = False  # Réinitialise la défense
        self.combat_log.append(f"C'est au tour de {current_player.name}!")

    def _check_combat_end(self):
        """Vérifie si le combat est terminé"""
        for player in self.players:
            if player.hp <= 0:
                self.is_combat_over = True
                winner = self.players[1 - self.players.index(player)]
                self.combat_log.append(f"{winner.name} remporte le combat!")
                break

    def _reset_players_state(self):
        """Réinitialise l'état des joueurs pour un nouveau combat"""
        for player in self.players:
            player.hp = player.max_hp
            player.energy = player.max_energy
            player.is_defending = False

    def get_combat_log(self):
        """Retourne l'historique du combat"""
        return "\n".join(self.combat_log)

    def get_current_player(self):
        """Retourne le joueur dont c'est le tour"""
        return self.players[self.current_turn]
