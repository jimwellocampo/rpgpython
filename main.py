from classes.game import Person, bcolors
from classes.magic import Spells
from classes.inventory import Item
import random
# DARK SPELLS
fire = Spells("Fire ball", 25, 400, "black")
thunder = Spells("Thunder bolt", 50, 220, "black")
water = Spells("Splash", 45, 510, "black")
rock = Spells("Rock Smash", 70, 530, "black")
wind = Spells("Gust", 25, 299, "black")

# LIGHT SPELLS
cure = Spells("Cure", 35, 100, "light")
greatHeal = Spells("Mega Heal", 75, 200, "light")

# Instance of Items
potion = Item('Potion', 'potion', 'Heals 50 HP', 55, 3)
greatPotion = Item('Great Potion', 'potion', 'Heals 100 HP', 105, 2)
maxPotion = Item('Max Potion', 'potion', 'Heals 500 HP', 505, 1)
elixir = Item('Elixir', 'elixir', 'Fully Restore HP/MP of one party member', 9999, 1)
greatElixir = Item('MegaElixir', 'elixir', 'Fully Restore HP/MP of whole party', 9999, 1)
rocket = Item('Rocket', 'attack', 'Deals 500 Damage', 500, 2)

# Enemy magic
fireBreath = Spells("Fire Breath", 25, 600, "black")
enemySkills = [fireBreath, wind, cure]

playerSkills = [fire, thunder, water, rock, wind, cure, greatHeal]
playerItems = [potion, greatPotion, maxPotion, elixir, greatElixir, rocket]
# create instance
player1 = Person("Samurai", 3040, 300, 80, 40, playerSkills, playerItems)
player2 = Person("Knight+", 4260, 304, 80, 60, playerSkills, playerItems)
player3 = Person("Lu 'Bao", 3660, 320, 80, 50, playerSkills, playerItems)
enemy2 = Person("Minion", 1205, 125, 400, 55, enemySkills, [])
enemy1 = Person("Dragon", 11200, 165, 400, 55, enemySkills, [])
enemy3 = Person("Undead", 1300, 105, 400, 55, enemySkills, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]
running = True
print(bcolors.FAIL + bcolors.BOLD + "AN EMEMY APPEARS!" + bcolors.ENDC)

while running:
    print("===========================")
    print(f"{bcolors.BOLD}NAME                 HP                                   MP")
    for enemy in enemies:
        enemy.getEnemyStats()
    for stats in players:
        stats.getStats()
    print('\n')

    for player in players:
        player.chooseAction()
        # print(f"{bcolors.FAIL} ALLEN TEMPLATE {bcolors.ENDC}")
        try:
            choice = input("Choose Action: ")
            index = int(choice) - 1
        except:
            print("Enter valid input")
            continue

        if index == 0:
            dmg = player.generateDamage()
            target = player.chooseTarget(enemies)
            enemies[target].takeDamage(dmg)
            print(f"{bcolors.OKBLUE}You attacked {enemies[target].name} for  {dmg} damage!{bcolors.ENDC} ")
            if enemies[target].getHp() == 0:
                print(f"{enemies[target].name} has died.")
                del enemies[target]
        elif index == 1:
            player.chooseMagic()
            magicChoice = input("\tChoose magic: ")
            if magicChoice == -1:
                continue
            spell = player.magic[int(magicChoice) - 1]
            magicDmg = spell.generateSpellDamage()

            if player.getMp() >= spell.cost:
                if spell.type == 'light':
                    player.heal(magicDmg)
                    print(f"{bcolors.OKGREEN}Player healed for {magicDmg}. {bcolors.ENDC}")
                else:
                    target = player.chooseTarget(enemies)
                    enemies[target].takeDamage(magicDmg)

                    player.reduceMp(spell.cost)
                    print(f"{bcolors.OKBLUE}{enemies[target].name} has taken {magicDmg} damage {bcolors.ENDC}\n"
                          f"You used {spell.name}! "
                          f" \nCost: {spell.cost} "
                          f"Remaining MP: {player.getMp()}")
                    if enemies[target].getHp() == 0:
                        print(f"{enemies[target].name} has died.")
                        del enemies[target]
            else:
                print(f"MP insufficient")
                continue
        elif index == 2:
            player.chooseItem()
            itemChoice = int(input("\tChoose Item: "))-1
            item = player.items[itemChoice]
            if itemChoice == -1:
                continue

            if item.qty == 0:
                print("You doesn't have this item anymore")
                continue
            else:
                if item.type == 'potion':
                    player.heal(item.prop)
                    item.qty -= 1
                    print(f"{bcolors.OKGREEN}Player healed for {item.prop}. {bcolors.ENDC}")
                elif item.type == 'elixir':
                    if item.name == 'MegaElixir':
                        for i in players:
                            i.hp = i.getMaxHp()
                            i.mp = i.getMaxMp()
                    else:
                        player.hp = player.getMaxHp()
                        player.mp = player.getMaxMp()
                    item.qty -= 1
                    print(f"{bcolors.OKGREEN}HP and MP of party was restored. {bcolors.ENDC}")
                elif item.type == 'attack':
                    target = player.chooseTarget(enemies)
                    enemies[target].takeDamage(item.prop)

                    item.qty -= 1
                    print(f"{bcolors.OKBLUE} {enemies[target].name} has taken {item.prop} damage. {bcolors.ENDC}")
                    if enemies[target].getHp() == 0:
                        print(f"{enemies[target].name} has died.")
                        del enemies[target]
        else:
            print("Please enter a number between the choices.")

    defeatedEnemies = 0
    defeatedPlayers = 0
    for enemy in enemies:
        if enemy.getHp() == 0:
            defeatedEnemies += 1
    i = -1
    for player in players:
        i += 1
        if player.getHp() == 0:
            defeatedPlayers += 1
            del players[i]
    if defeatedEnemies == 3:
        print(bcolors.OKGREEN + "You win! " + bcolors.ENDC)
        running = False
    if defeatedPlayers == 3:
        print(bcolors.FAIL + "Your enemies has defeated you!" + bcolors.ENDC)
        running = False

    for enemy in enemies:
        enemyChoice = random.randrange(0, 2)
        if enemyChoice == 0:
            enemyDmg = enemies[0].generateDamage()
            target = random.randrange(0, 3)
            players[target].takeDamage(enemyDmg)
            print(f"{bcolors.FAIL}{enemy.name} attacks {players[target].name} for {enemyDmg} {bcolors.ENDC}")
        elif enemyChoice == 1:
            spell, magicDmg = enemy.chooseEnemySpell()
            target = random.randrange(0, len(players))

            if enemy.getMp() >= spell.cost:
                if spell.type == 'light':
                    enemy.heal(magicDmg)
                    print(f"{bcolors.OKGREEN}{enemy.name } healed for {magicDmg}. {bcolors.ENDC}")
                else:
                    target = random.randrange(0, 3)
                    players[target].takeDamage(magicDmg)
                    print(f"{enemy.name} used {spell.name}!"
                          f"{bcolors.FAIL}{players[target].name} has taken {magicDmg} damage from {enemy.name} {bcolors.ENDC}\n")
                    if players[target].getHp() == 0:
                        print(f"{players[target].name} has died.")
                        del players[target]
                enemy.reduceMp(spell.cost)
            else:
                print(f"{enemy.name} has not enough MP to use his skill.")
                continue
        elif enemyChoice == 2:
            print('wala pa')