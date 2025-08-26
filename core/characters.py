from abc import ABC, abstractmethod

class Personnage(ABC):
    def __init__(self, nom):
        """
        Classe abstraite représentant un personnage de base
        Args:
            nom (str): Nom du personnage
        """
        self.nom = nom
        self.pv_max = 100
        self.pv = self.pv_max
        self.energie_max = 50
        self.energie = self.energie_max
        self.is_defending = False
        self.special_cost = 25  # Coût de base pour l'attaque spéciale

    @abstractmethod
    def attaque_normale(self, cible):
        """Attaque de base du personnage"""
        pass

    @abstractmethod
    def attaque_speciale(self, cible):
        """Attaque spéciale du personnage"""
        pass

    def defendre(self):
        """Active le mode défense pour le tour"""
        self.is_defending = True

    def recharger_energie(self, amount=10):
        """Recharge l'énergie du personnage"""
        self.energie = min(self.energie + amount, self.energie_max)

    def recevoir_degats(self, degats):
        """
        Applique les dégâts au personnage en tenant compte de la défense
        Retourne les dégâts réellement subis
        """
        if self.is_defending:
            degats = max(1, degats // 2)  # Réduction de 50% (min 1 dégât)
            self.is_defending = False
        
        self.pv = max(0, self.pv - degats)
        return degats

    def est_ko(self):
        """Vérifie si le personnage est K.O."""
        return self.pv <= 0


class Guerrier(Personnage):
    def __init__(self, nom):
        super().__init__(nom)
        self.special_cost = 20

    def attaque_normale(self, cible):
        """Coup d'épée standard"""
        degats = 15
        degats_infliges = cible.recevoir_degats(degats)
        return f"{self.nom} frappe avec son épée (-{degats_infliges} PV)"

    def attaque_speciale(self, cible):
        """Frappe puissante avec chance d'étourdissement"""
        if self.energie >= self.special_cost:
            self.energie -= self.special_cost
            degats = 25
            degats_infliges = cible.recevoir_degats(degats)
            return f"{self.nom} lance une frappe puissante ! (-{degats_infliges} PV)"
        return None


class Mage(Personnage):
    def __init__(self, nom):
        super().__init__(nom)
        self.special_cost = 30

    def attaque_normale(self, cible):
        """Boule de feu élémentaire"""
        degats = 20
        degats_infliges = cible.recevoir_degats(degats)
        return f"{self.nom} lance une boule de feu (-{degats_infliges} PV)"

    def attaque_speciale(self, cible):
        """Tempête élémentaire (ignore la défense)"""
        if self.energie >= self.special_cost:
            self.energie -= self.special_cost
            degats = 35
            was_defending = cible.is_defending
            cible.is_defending = False  # Ignore la défense
            degats_infliges = cible.recevoir_degats(degats)
            cible.is_defending = was_defending
            return f"{self.nom} invoque une tempête élémentaire ! (-{degats_infliges} PV)"
        return None


class Archer(Personnage):
    def __init__(self, nom):
        super().__init__(nom)
        self.special_cost = 15

    def attaque_normale(self, cible):
        """Tir rapide (double attaque)"""
        degats1 = 12
        degats2 = 12
        total = 0
        
        msg = f"{self.nom} tire deux flèches rapides : "
        degats_infliges = cible.recevoir_degats(degats1)
        total += degats_infliges
        msg += f"première (-{degats_infliges} PV), "
        
        degats_infliges = cible.recevoir_degats(degats2)
        total += degats_infliges
        msg += f"seconde (-{degats_infliges} PV)"
        
        return msg

    def attaque_speciale(self, cible):
        """Tir précis (dégâts critiques)"""
        if self.energie >= self.special_cost:
            self.energie -= self.special_cost
            degats = 40
            degats_infliges = cible.recevoir_degats(degats)
            return f"{self.nom} décoche un tir précis ! (-{degats_infliges} PV)"
        return None
