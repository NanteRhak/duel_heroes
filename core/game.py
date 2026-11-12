from core.characters import Guerrier, Mage, Archer

class Game:
    def __init__(self):
        """Initialise l'état du jeu"""
        self.joueur1 = None
        self.joueur2 = None
        self.tour = None
        self.historique = []
        self.gagnant = None

    def creer_personnage(self, classe, nom, joueur_num):
        """
        Crée un personnage pour un joueur
        Args:
            classe (str): 'guerrier', 'mage' ou 'archer'
            nom (str): Nom du personnage
            joueur_num (int): 1 ou 2
        Returns:
            bool: True si création réussie
        """
        if classe.lower() == 'guerrier':
            perso = Guerrier(nom)
        elif classe.lower() == 'mage':
            perso = Mage(nom)
        elif classe.lower() == 'archer':
            perso = Archer(nom)
        else:
            return False

        if joueur_num == 1:
            self.joueur1 = perso
        else:
            self.joueur2 = perso
        return True

    def demarrer_combat(self):
        """
        Prépare et lance un nouveau combat
        Returns:
            bool: True si les deux joueurs sont prêts
        """
        if self.joueur1 and self.joueur2:
            self.tour = 1
            self.is_combat_over = False
            for joueur in (self.joueur1, self.joueur2):
                joueur.pv = joueur.pv_max
                joueur.energie = joueur.energie_max
                joueur.is_defending = False
            self.historique = [
                f"Le combat commence ! {self.joueur1.nom} vs {self.joueur2.nom}",
                f"C'est au tour de {self.joueur1.nom} !"
            ]
            self.gagnant = None
            return True
        return False

    def executer_action(self, action):
        """
        Exécute une action pour le joueur courant
        Args:
            action (str): 'attaquer', 'special', 'defendre', 'recharger'
        Returns:
            tuple: (succès(bool), est_fini(bool))
        """
        # Vérifie si le combat est prêt
        if self.tour is None or self.is_combat_over:
            return False, False

        # Récupère le joueur actuel et son adversaire
        joueur_actuel = self.get_current_player()
        adversaire = self.joueur2 if joueur_actuel == self.joueur1 else self.joueur1

        # Exécute l'action demandée
        if action == 'attaquer':
            resultat = joueur_actuel.attaque_normale(adversaire)
        elif action == 'special':
            resultat = joueur_actuel.attaque_speciale(adversaire)
            if not resultat:  # Énergie insuffisante
                return False, False
        elif action == 'defendre':
            joueur_actuel.defendre()
            resultat = f"{joueur_actuel.nom} se met en position défensive"
        elif action == 'recharger':
            joueur_actuel.recharger_energie()
            resultat = f"{joueur_actuel.nom} recharge son énergie"
        else:
            return False, False

        # Ajoute le résultat à l'historique
        self.historique.append(resultat)
        
        # Vérifie si le combat est terminé
        if adversaire.est_ko():
            self.gagnant = joueur_actuel
            message_victoire = f"{joueur_actuel.nom} remporte le combat !"
            self.historique.append(message_victoire)
            self.is_combat_over = True
            return True, True

        self.next_turn()
        self.historique.append(f"Au tour de {self.get_current_player().nom} !")

        return True, False

    def executer_action_ia(self):
        """Joue le tour de l'IA : attaque spéciale si elle peut la payer, sinon recharge."""
        if self.tour is None or self.is_combat_over:
            return False, False
        joueur = self.get_current_player()
        action = 'special' if joueur.energie >= joueur.special_cost else 'recharger'
        return self.executer_action(action)

    def get_current_player(self):
        """Retourne le personnage dont c'est le tour."""
        return self.joueur1 if self.tour == 1 else self.joueur2

    def next_turn(self):
        """Passe au tour suivant et réinitialise la défense du joueur qui commence."""
        self.tour = 2 if self.tour == 1 else 1
        self.get_current_player().is_defending = False

    def get_joueur_actuel(self):
        """Retourne le numéro du joueur dont c'est le tour (1 ou 2)"""
        return self.tour

    def get_etat_combat(self):
        """
        Retourne l'état actuel du combat
        Returns:
            dict: {
                'joueur1': { 'nom': str, 'pv': int, 'energie': int },
                'joueur2': { 'nom': str, 'pv': int, 'energie': int },
                'historique': list[str],
                'tour': int (1 ou 2)
            }
        """
        # CORRECTION : Gestion des cas où les joueurs ne sont pas initialisés
        joueur1_data = {
            'nom': self.joueur1.nom,
            'pv': self.joueur1.pv,
            'energie': self.joueur1.energie
        } if self.joueur1 else {'nom': 'Joueur 1', 'pv': 0, 'energie': 0}
        
        joueur2_data = {
            'nom': self.joueur2.nom,
            'pv': self.joueur2.pv,
            'energie': self.joueur2.energie
        } if self.joueur2 else {'nom': 'Joueur 2', 'pv': 0, 'energie': 0}
        
        return {
            'joueur1': joueur1_data,
            'joueur2': joueur2_data,
            'historique': self.historique,
            'tour': self.get_joueur_actuel()
        }

