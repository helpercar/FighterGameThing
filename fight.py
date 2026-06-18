import random

class fight:
    def __init__(self, fighter1, fighter2):
        self.fighter1 = fighter1    # Should be Player in most instances
        self.fighter2 = fighter2
        self.turnRolls = 0

    # Turn order of Combat using a system where the fighters rolls between 75% and 110% of their speed
    def turn_order(self):
        while True:
            if self.turnRolls > 10:
                if self.fighter1.speed > self.fighter2.speed:
                    return 1
                elif self.fighter2.speed > self.fighter1.speed:
                    return 2
                else:
                    return random.randint(1, 2)

            roll1 = random.randint(int(self.fighter1.speed * 0.75), int(self.fighter1.speed * 1.1))
            roll2 = random.randint(int(self.fighter2.speed * 0.75), int(self.fighter2.speed * 1.1))

            if roll1 > roll2:
                return 1
            elif roll2 > roll1:
                return 2
            else:
                self.turnRolls += 1
                continue
        
    def attack(self, defender, damage):
        if isinstance(damage, tuple):
            for hit in damage:
                defender.take_damage(hit)
        else:
            defender.take_damage(damage)
