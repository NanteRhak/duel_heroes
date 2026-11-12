from abc import ABC, abstractmethod


class Character(ABC):
    def __init__(self, name):
        """Base hero shared by every class."""
        self.name = name
        self.max_hp = 100
        self.hp = self.max_hp
        self.max_energy = 50
        self.energy = self.max_energy
        self.is_defending = False
        self.special_cost = 25

    @abstractmethod
    def attack(self, target):
        """Basic attack."""

    @abstractmethod
    def special_attack(self, target):
        """Special attack."""

    def defend(self):
        """Halve the next incoming hit."""
        self.is_defending = True

    def recharge_energy(self, amount=10):
        """Restore energy, capped at the maximum."""
        self.energy = min(self.energy + amount, self.max_energy)

    def take_damage(self, damage):
        """Apply damage after defence and return the HP actually lost."""
        if self.is_defending:
            damage = max(1, damage // 2)
            self.is_defending = False

        before = self.hp
        self.hp = max(0, self.hp - damage)
        return before - self.hp

    def is_ko(self):
        """Whether the hero is knocked out."""
        return self.hp <= 0


class Warrior(Character):
    def __init__(self, name):
        super().__init__(name)
        self.special_cost = 20

    def attack(self, target):
        """Sword strike."""
        damage = 15
        damage_dealt = target.take_damage(damage)
        return f"{self.name} strikes with a sword (-{damage_dealt} HP)"

    def special_attack(self, target):
        """Powerful blow."""
        if self.energy >= self.special_cost:
            self.energy -= self.special_cost
            damage = 25
            damage_dealt = target.take_damage(damage)
            return f"{self.name} unleashes a powerful blow! (-{damage_dealt} HP)"
        return None


class Mage(Character):
    def __init__(self, name):
        super().__init__(name)
        self.special_cost = 30

    def attack(self, target):
        """Fireball."""
        damage = 20
        damage_dealt = target.take_damage(damage)
        return f"{self.name} casts a fireball (-{damage_dealt} HP)"

    def special_attack(self, target):
        """Elemental storm that ignores defence."""
        if self.energy >= self.special_cost:
            self.energy -= self.special_cost
            damage = 35
            was_defending = target.is_defending
            target.is_defending = False
            damage_dealt = target.take_damage(damage)
            target.is_defending = was_defending
            return f"{self.name} summons an elemental storm! (-{damage_dealt} HP)"
        return None


class Archer(Character):
    def __init__(self, name):
        super().__init__(name)
        self.special_cost = 15

    def attack(self, target):
        """Two quick arrows."""
        first = target.take_damage(12)
        second = target.take_damage(12)
        return f"{self.name} fires two quick arrows: first (-{first} HP), second (-{second} HP)"

    def special_attack(self, target):
        """Precise shot."""
        if self.energy >= self.special_cost:
            self.energy -= self.special_cost
            damage_dealt = target.take_damage(40)
            return f"{self.name} looses a precise shot! (-{damage_dealt} HP)"
        return None
