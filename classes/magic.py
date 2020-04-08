import random

class Spells:
    def __init__(self,name,cost,damage,type):
       self.name = name
       self.cost = cost
       self.damage = damage
       self.type = type

    def generateSpellDamage(self):
        mgdmgl = self.damage - 15
        mgdmgh = self.damage + 15
        return random.randrange(mgdmgl, mgdmgh)