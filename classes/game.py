import random


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mana, atk, df, magic, items):
        self.name = name
        self.hp = hp
        self.maxHp = hp
        self.mana = mana
        self.maxMana = mana
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.action = ["Attack", "Magic", "Items"]

    def generateDamage(self):
        return random.randrange(self.atkl, self.atkh)

    def chooseTarget(self, enemies):
        i = 1
        print(f"{bcolors.FAIL}{bcolors.BOLD}\t\tTARGET {bcolors.ENDC}")
        for enemy in enemies:
            if enemy.hp > 0:
                print(f"\t\t {i}. {enemy.name}")
                i += 1
        choice = int(input('\tChoose target: ')) - 1
        return choice

    def takeDamage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def getHp(self):
        return self.hp

    def getMaxHp(self):
        return self.maxHp

    def getMp(self):
        return self.mana

    def getMaxMp(self):
        return self.maxMana

    def reduceMp(self, cost):
        self.mana -= cost

    def chooseAction(self):
        print(f"{bcolors.BOLD} {self.name}'s turn! {bcolors.ENDC}")
        print(f"\t{bcolors.OKBLUE}{bcolors.BOLD} Actions {bcolors.ENDC}")
        i = 1
        for item in self.action:
            print(f"\t\t{str(i)}: {item}")
            i += 1

    def chooseMagic(self):
        print(f"\t{bcolors.OKBLUE}{bcolors.BOLD} Magics {bcolors.ENDC}")
        i = 1
        for spell in self.magic:
            print(f"\t\t{str(i)}: {spell.name} cost: {spell.cost}")
            i += 1

    def chooseItem(self):
        print(f"\t{bcolors.OKGREEN}{bcolors.BOLD} Items {bcolors.ENDC}")
        i = 1
        for item in self.items:
            print(f"\t\t{str(i)}: {item.name} cost: {item.description} (x{item.qty})")
            i += 1

    def heal(self, points):
        self.hp += points
        if self.hp > self.maxHp:
            self.hp = self.maxHp

    def getName(self):
        return self.name

    def getEnemyStats(self):
        hpBar = ""
        barTicks = (self.hp / self.maxHp) * 100 / 2

        while barTicks > 0:
            hpBar += '█'
            barTicks -= 1

        while len(hpBar) < 50:
            hpBar += ' ' \
                     ''
        hpString = str(self.hp) + '/' + str(self.maxHp)
        tmp = ''
        if len(hpString) < 11:
            decreased = 11 - len(hpString)
            while decreased > 0:
                tmp += ' '
                decreased -= 1
            currentHp = tmp + hpString
        else:
            currentHp = hpString

        manabarsTicks = ((self.mana / self.maxMana) * 100 / 10)
        manaBar = ""
        while manabarsTicks > 0:
            manaBar += '█'
            manabarsTicks -= 1
        while len(manaBar) < 10:
            manaBar += ' '
        mpString = str(self.mana) + '/' + str(self.maxMana)
        tmp1 = ''
        if len(mpString) < 7:
            minus = 7 - len(mpString)
            while minus > 0:
                tmp1 += ' '
                minus -= 1
            currentMP = tmp1 + mpString
        else:
            currentMP = mpString
        print(f"                      __________________________________________________               __________\n"
              f"{self.name}  {currentHp}  |{bcolors.FAIL}{hpBar}{bcolors.ENDC}|     {currentMP} |{bcolors.OKBLUE}{manaBar}{bcolors.ENDC}|")

    def getStats(self):
        barsTicks = ((self.hp / self.maxHp) * 100 / 4)
        manabarsTicks = ((self.mana / self.maxMana) * 100 / 10)
        healthBar = ""

        while barsTicks > 0:
            healthBar += '█'
            barsTicks -= 1
        while len(healthBar) < 25:
            healthBar += ' '

        manaBar = ""
        while manabarsTicks > 0:
            manaBar += '█'
            manabarsTicks -= 1
        while len(manaBar) < 10:
            manaBar += ' '

        theme = bcolors.OKGREEN
        theme2 = bcolors.OKBLUE
        if len(str(self.hp)) <= 3:
            theme = bcolors.FAIL
        if len(str(self.mana)) < 2:
            theme2 = bcolors.FAIL

        hpString = str(self.hp) + '/' + str(self.maxHp)
        tmp = ''
        if len(hpString) < 9:
            decreased = 9 - len(hpString)
            while decreased > 0:
                tmp += ' '
                decreased -= 1
            currentHp = tmp + hpString
        else:
            currentHp = hpString

        mpString = str(self.mana) + '/' + str(self.maxMana)
        tmp1 = ''
        if len(mpString) < 7:
            minus = 7 - len(mpString)
            while minus > 0:
                tmp1 += ' '
                minus -= 1
            currentMP = tmp1 + mpString
        else:
            currentMP = mpString
        print(f"                     _________________________              __________\n"
              f"{self.name}  {currentHp}  |{theme}{healthBar}{bcolors.ENDC}|"
              f"  {currentMP}   |{theme2}{manaBar}{bcolors.ENDC}|")

    def chooseEnemySpell(self):
        magicChoice = random.randrange(0, len(self.magic))
        spell = self.magic[magicChoice]
        magicDmg = spell.generateSpellDamage()
        pct = self.hp / self.maxHp
        try:
            if self.mana < spell.cost or (spell.type == "light" and pct > 0.5):
                # this will fail incase of black_magic_cost > self.mp and pct > 0.5
                spell, magicDmg = self.chooseEnemySpell()
                return spell, magicDmg
            if spell.type == 'black' and spell.cost > self.mana and pct > 0.5:
                print(f"{self.name} doesn't have enough mana to use his skill. Free turn ")
            else:
                return spell, magicDmg
        except:
            print('Something went wrong')
