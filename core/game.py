from core.characters import Guerrier, Mage, Archer

class Game:
    def __init__(self):
        """Initialise l'état du jeu"""
        self.joueur1 = None
        self.joueur2 = None
        self.moteur_combat = None
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
            self.moteur_combat = CombatEngine(self.joueur1, self.joueur2)
            self.moteur_combat.start_combat()
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
        if not self.moteur_combat or self.moteur_combat.is_combat_over:
            return False, False

        # Récupère le joueur actuel et son adversaire
        joueur_actuel = self.moteur_combat.get_current_player()
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
            self.moteur_combat.is_combat_over = True
            return True, True

        # CORRECTION CRITIQUE : Passer au tour suivant
        self.moteur_combat.next_turn()
        
        # Ajoute un message pour le nouveau tour
        nouveau_joueur = self.moteur_combat.get_current_player()
        self.historique.append(f"Au tour de {nouveau_joueur.nom} !")
        
        return True, False

    def get_joueur_actuel(self):
        """Retourne le numéro du joueur dont c'est le tour (1 ou 2)"""
        if not self.moteur_combat:
            return None
        return 1 if self.moteur_combat.get_current_player() == self.joueur1 else 2

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

class CombatEngine:
    """Gestion des tours de combat"""
    def __init__(self, joueur1, joueur2):
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.tour_joueur1 = True  # True = tour du joueur1, False = tour du joueur2
        self.is_combat_over = False

    def start_combat(self):
        """Réinitialise l'état pour un nouveau combat"""
        self.tour_joueur1 = True
        self.is_combat_over = False
        # Réinitialise l'état des joueurs
        self.joueur1.pv = self.joueur1.pv_max
        self.joueur1.energie = self.joueur1.energie_max
        self.joueur2.pv = self.joueur2.pv_max
        self.joueur2.energie = self.joueur2.energie_max
        self.joueur1.is_defending = False
        self.joueur2.is_defending = False

    def get_current_player(self):
        """Retourne le joueur dont c'est le tour"""
        return self.joueur1 if self.tour_joueur1 else self.joueur2

    def next_turn(self):
        """Passe au tour suivant et réinitialise la défense"""
        # Change de tour
        self.tour_joueur1 = not self.tour_joueur1
        
        # Réinitialise l'état de défense pour le nouveau joueur
        current_player = self.get_current_player()
        current_player.is_defending = False
