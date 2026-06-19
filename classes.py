import random

class Fightable:
    def __init__(self, health, attack, defense, speed, name, level):
        self.health = health
        self.maxHP = self.health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.name = name
        self.level = level
        self.attacks = []
        self.buffs = []
        self.regen = False


    def roll_attack(self):
        # Can Crit and Fail
        crit = random.randint(0, 1) == 1
        damage = random.randint(0, 6) * self.attack

        if (crit):
            print("Crit!")
            damage = damage * 2

        return damage
    
    def take_damage(self, damage):
        self.health -= max(0, damage - self.defense)

    def get_attacks(self):
        return self.attacks
    
    def turn(self):
        return
    
    def reduce_buff(self):
        for index, buff in enumerate(self.buffs):
            buff[0] -= 1
            if buff[0] <= 0:
                self.toggle_buffs(index)

    def toggle_buffs(self, index):
        return

class Slime(Fightable):
    def __init__(self, health, attack, defense, speed, name, level):
        super().__init__(health, attack, defense, speed, name, level)
        self.attacks = ["Hop", "Splash", "Slime Scales", "Sharp Slime", "Slime Slurp", "Slime Dance"]
        self.buffs = [[0, "def"], [0, "att"], [0, "reg"], [0, "spe"]] # Order goes [slime_scale, slime_stab, slime_regen, slime_dance]

    def choice_attack(self, attack):
        match attack:
            case 0:
                return self.hop()
            case 1:
                return self.splash()
            case 2:
                self.slime_scale()
            case 3:
                self.slime_stab()
            case 4:
                self.slime_slurp()
            case 5:
                self.slime_dance()
        
        # For the attacks that buff/do no damage
        return 0

    def hop(self):
        return int(self.roll_attack())
    
    # Want the splash to hit 3 times
    def splash(self):
        damage1 = int(self.roll_attack() / 2)
        damage2 = int(self.roll_attack() / 3)
        damage3 = int(self.roll_attack() / 4)
        return (damage1, damage2, damage3)
    
    def slime_scale(self):
        # Make sure that the buff does not stack with itself
        if (self.buffs[0][0] == 0):
            self.defense *= 1.5

        # 3 Turn Buff
        self.buffs[0][0] += 3

    def slime_stab(self):
        if (self.buffs[1][0] == 0):
            self.attack *= 1.5
        
        # 3 turn buff
        self.buffs[1][0] += 3

    def slime_slurp(self):
        self.regen = True
        self.buffs[2][0] += 3
    
    def slime_dance(self):
        self.speed *= 1.25
        self.buffs[3][0]

    def toggle_buffs(self, index):
        match index:
            case 0:
                self.defense /= 1.5
            case 1:
                self.attack /= 1.5
            case 2:
                self.regen = False
            case 3:
                self.speed /= 1.25
            case _:
                return
        return
    
    def turn(self):
        if self.regen:
            # Regenerate 10% Health
            self.health += (0.1 * self.maxHP)
            self.reduce_buff()


    



