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
        
        avant = self.pv
        self.pv = max(0, self.pv - degats)
        return avant - self.pv

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
        return f"{self.nom} strikes with a sword (-{degats_infliges} HP)"

    def attaque_speciale(self, cible):
        """Frappe puissante avec chance d'étourdissement"""
        if self.energie >= self.special_cost:
            self.energie -= self.special_cost
            degats = 25
            degats_infliges = cible.recevoir_degats(degats)
            return f"{self.nom} unleashes a powerful blow! (-{degats_infliges} HP)"
        return None


class Mage(Personnage):
    def __init__(self, nom):
        super().__init__(nom)
        self.special_cost = 30

    def attaque_normale(self, cible):
        """Boule de feu élémentaire"""
        degats = 20
        degats_infliges = cible.recevoir_degats(degats)
        return f"{self.nom} casts a fireball (-{degats_infliges} HP)"

    def attaque_speciale(self, cible):
        """Tempête élémentaire (ignore la défense)"""
        if self.energie >= self.special_cost:
            self.energie -= self.special_cost
            degats = 35
            was_defending = cible.is_defending
            cible.is_defending = False  # Ignore la défense
            degats_infliges = cible.recevoir_degats(degats)
            cible.is_defending = was_defending
            return f"{self.nom} summons an elemental storm! (-{degats_infliges} HP)"
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
        
        msg = f"{self.nom} fires two quick arrows: "
        degats_infliges = cible.recevoir_degats(degats1)
        total += degats_infliges
        msg += f"first (-{degats_infliges} HP), "
        
        degats_infliges = cible.recevoir_degats(degats2)
        total += degats_infliges
        msg += f"second (-{degats_infliges} HP)"
        
        return msg

    def attaque_speciale(self, cible):
        """Tir précis (dégâts critiques)"""
        if self.energie >= self.special_cost:
            self.energie -= self.special_cost
            degats = 40
            degats_infliges = cible.recevoir_degats(degats)
            return f"{self.nom} looses a precise shot! (-{degats_infliges} HP)"
        return None
