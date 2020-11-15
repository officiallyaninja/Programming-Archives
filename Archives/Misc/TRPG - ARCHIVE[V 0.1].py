from termcolor import colored
import random

opponents = []


def show_opponents(opponent_list):
    for i in range(0, len(opponent_list)):
        print(colored(i, 'green'), ': ', end='', sep='')
        opponent_list[i].show_healthbar()


class Move():
    def __init__(self, name, base_dmg, AoE, status_effect, accuracy):
        self.name = name
        self.base_dmg = base_dmg
        self.AoE = AoE
        self.status_effect = status_effect
        self.accuracy = accuracy

    def use_move(self, user):
        # base damage of an attack for that character
        dmg = (((user.ATK) / 2) * (self.base_dmg))
        if user.isPlayer:  # checks if the user is the player or an enemy
            if self.AoE:  # checks if the move hits all enemies or just one Enemy
                for enemy in opponents:
                    hit_chance = max(50, self.accuracy - enemy.evasion)
                    hit_roll = random.randint(0, 99)
                    if hit_roll > hit_chance:  # if this triggers its a miss
                        print(f'{user.name} missed {enemy.name}')
                        continue
                    dmg = dmg * random.uniform(0.9, 1.1)
                    user.attack(enemy, dmg)

            # TODO: add status effect check here
            else:
                show_opponents(opponents)
                target = int(input('which enemy do you want to attack?: '))
                hit_chance = max(50, self.accuracy - target.evasion)
                hit_roll = random.randint(0, 99)
                if hit_roll > hit_chance:  # if this triggers its a miss
                    print(f'{user.name} missed {target.name}')
                    return None
                dmg = dmg * random.uniform(0.9, 1.1)
                user.attack(opponents[target], dmg)
                # TODO: add status effect check here
        # TODO: make enemies attack too u idiot


strike = Move('strike', 10, True, None, 60)
Flame_strike = Move('flame strike', 20, False, 'burning', 90)


class Character():
    def __init__(self):
        self.dead = False  # checks whether player or enemy is dead
        # TODO: add a way for characters to die
        self.base_color = 'white'
        self.color = 'white'
        self.isPlayer = False
        self.evasion = 0

    def get_health_percent(self):  # gives percent of health remaining as a float b/w 0 and 1
        return self.hp / self.maxhp

    def show_healthbar(self):  # prints a healthbar
        health_bar = "["
        len_filled_in_bit = self.hp // 10  # every 10 hit points corresponds to 1 'block' of health

        for i in range(len_filled_in_bit):
            health_bar += '■'

        # calculates how much health has been lost and hence the empty space in the bar
        len_empty_bit = (self.maxhp - self.hp) // 10

        for i in range(len_empty_bit):
            health_bar += ' '

        # also gives a precise numeric display, in case the player needs it
        health_bar += f'] {self.hp}/{self.maxhp}'
        # health is set to be red in colour for the player, and white for enemies
        # this is to make it easy to distinguish a see
        print(self.name)
        print(colored(health_bar, self.color))

    def attack(self, other, dmg):  # code to make moves easily deal damage enemies and check if dead
        damage = int(dmg)
        other.hp -= damage
        print(f'{self.name} dealt {damage} damage to {other.name}')
        if other.hp < 0:
            other.dead = True

    # def die(self): should remove enemies from opponents, and end game for player


class Player(Character):
    def __init__(self):
        super().__init__()
        self.maxhp = 100
        self.hp = self.maxhp  # initially hp will be max hp
        self.ATK = 3
        self.color = 'red'  # player color is red to easily differentiate from enemies
        self.name = 'Player'  # maybe i will later make this a variable that the player enters
        self.isPlayer = True


class Enemy(Character):
    def __init__(self):
        super().__init__()


class Gremlin(Enemy):
    def __init__(self):
        super().__init__()
        self.name = 'Gremlin'
        self.base_maxhp = 80
        self.maxhp = int(self.base_maxhp * (random.uniform(0.75, 1.2))
                         )  # some variance in max health
        self.hp = self.maxhp  # initially hp will be max hp
        self.ATK = 2 + random.randint(-1, 1)  # slightly varies the attack power


class Bat(Enemy):
    def __init__(self):
        super().__init__()
        self.name = 'Bat'
        self.base_maxhp = 35
        self.maxhp = int(self.base_maxhp * (random.uniform(0.8, 1.2))
                         )  # some variance in max health
        self.hp = self.maxhp  # initially hp will be max hp
        self.ATK = 4 + random.randint(-1, 1)  # slightly varies the attack power
        self.evasion = 5


p = Player()
p.show_healthbar()

opponents.append(Gremlin())
opponents.append(Bat())
opponents.append(Bat())
for i in range(0, 10):
    strike.use_move(p)
    show_opponents(opponents)
