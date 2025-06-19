import combat

class enemyStats:
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
        print(f"Enemy attacks for {damage} damage")
        return damage   
    
    def printStats(self):
        print(f"Enemy Stats: Health: {self.health}/{self.maxHealth}, Damage: {self.minDmg}-{self.maxDmg}")    

    def getEnemyStats(self):
        return f"Enemy Stats {self.health}/{self.maxHealth} Damage {self.minDmg}-{self.maxDmg}\n"