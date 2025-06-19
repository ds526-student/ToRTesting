import combat

class playerStats:
    maxHealth = 100
    health = 100
    maxDmg = 10
    minDmg = 5

    def __init__(self, health=100, maxHealth=100, maxDmg=10, minDmg=5):
        self.health = health
        self.maxHealth = maxHealth
        self.maxDmg = maxDmg
        self.minDmg = minDmg

    def takeDamage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def attack(self):
        damage = combat.attack(self.minDmg, self.maxDmg)
        return damage
    
    def heal(self, amount):
        self.health += amount
        if self.health > self.maxHealth:
            self.health = self.maxHealth

        print(f"Player heals for {amount}, health is now {self.health}/{self.maxHealth}")

    def printStats(self):
        print(f"Player Stats:\nHealth: {self.health}/{self.maxHealth}\nDamage: {self.minDmg}-{self.maxDmg}") 