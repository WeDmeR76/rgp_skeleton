from colorama import Fore, Back

class Body:
    def __init__(self, health):
        self.head = health
        self.body = health
        self.arms = int(health*0.25+1)
        self.legs = int(health * 0.25+1)

    def show_body(self):
        head_color = Fore.GREEN if self.head > 0 else Fore.RED
        arms_color = Fore.GREEN if self.arms > 0 else Fore.RED
        body_color = Fore.GREEN if self.body > 0 else Fore.RED
        legs_color = Fore.GREEN if self.legs > 0 else Fore.RED

        return (f'\n   {head_color}o   \n'
                f'  {arms_color}/{body_color}O{arms_color}\\   \n'
                f'  {legs_color}/{legs_color} \\  {Fore.RESET}\n')

    def death(self):
        self.head = 0
        self.body = 0
        self.arms = 0
        self.legs = 0

class Weapon:
    def __init__(self, name, price, damage, chance_of_crit):
        self.name = name
        self.price = price
        self.damage = damage
        self.chance_of_crit = chance_of_crit

    def show(self):
        return f'{self.name} {Fore.LIGHTYELLOW_EX}стоит: {self.price}  {Fore.RED}урон: {self.damage}, {Fore.LIGHTRED_EX}доп. нашс крита: {self.chance_of_crit}{Fore.RESET}'

class Poison:
    def __init__(self, name, price, heal):
        self.name = name
        self.price = price
        self.heal = heal

small_poison = Poison('Маленькая хилка', 100, 30)
mid_poison = Poison('Средняя хилка', 200, 50)
big_poison = Poison('Большая хилка', 300, 70)

class Hero:
    def __init__(self, name, straight, agillity, intelligence):
        self.weapon = Weapon('Палка', 50, 10, 1)
        self.straight = straight
        self.agillity = agillity
        self.intelligence = intelligence
        self.name = name
        self.max_health = 100 + straight * 4
        self.health = self.max_health
        self.max_exp = 100
        self.exp = 0
        self.lvl = 0
        self.damage = 10 * self.straight + self.weapon.damage
        self.avoid = (1 + self.agillity * 2)*0.01
        self.armor = self.agillity
        self.inventory = []
        self.money = 100



    def show_inventory(self):
        return [poison.name for poison in self.inventory]

    def info(self):
        print(f'\nВы: {Fore.LIGHTYELLOW_EX}{self.name}\n'
              f'{Fore.RESET}Статы: {Fore.RED}сила: {self.straight}, {Fore.GREEN}ловкость {self.agillity}, {Fore.BLUE}интеллект: {self.intelligence}\n'
              f'{Fore.RESET}Оружие {self.weapon.name} урон: {self.weapon.damage}, крит. шанс: {self.weapon.chance_of_crit}%\n'
              f'Здоровье: {self.health}\n'
              f'Броня: {self.armor}%\n'
              f'Шанс уворота {self.avoid}%\n'
              f'Опыт: {self.exp}\n'
              f'Уровень: {self.lvl}\n'
              f'Деньги: {self.money}\n'
              f'Инвентарь: {self.show_inventory()}\n'
              )

    def atack(self, enemy):
        mini_random_dmg = random.randint(0, 5)
        damage = self.damage
        plus_or_minus = random.randint(1, 2)
        if plus_or_minus == 1:
            damage += mini_random_dmg
        elif plus_or_minus == 2:
            damage -= mini_random_dmg
        crit = False
        if random.random() < self.weapon.chance_of_crit*0.01:
            damage = self.damage * 2
            crit = True

        while True:
            where = int(input('\n1) Ноги\n'
                              '2) Руки\n'
                              '3) Тело\n'
                              '4) Голова\n'
                              'Выберите куда бить: '))

            if where == 1:
                where = 'ногам'

                if enemy.body.legs <= 0:
                    print(f'\n{Back.RED}Ноги уже отрублены{Back.RESET}\n')

                elif random.random() < 0.9:
                    damage *= 0.8
                    enemy.body.legs -= damage
                    if enemy.body.legs <= 0:
                        time.sleep(1)
                        print(f"\n{Back.RED}Вы отрубаете ноги{Back.RESET}\n")
                        time.sleep(1)
                    break

                else:
                    print(f'{Back.RED}Вы промахнулсь!{Back.RESET}')
                    time.sleep(1)
                    return 'miss'


            elif where == 2:
                where = 'рукам'
                damage *= 0.8
                if enemy.body.arms <= 0:
                    print(f'\n{Back.RED}Руки уже отрублены{Back.RESET}\n')

                elif enemy.body.arms <= 0:
                    enemy.body.arms -= damage
                    break


                elif random.random() < 0.9:
                    enemy.body.arms -= damage
                    if enemy.body.arms <= 0:
                        print(f"\n{Back.RED}Вы отрубаете руки{Back.RESET}\n")
                        enemy.damage -= enemy.weapon_damage
                        enemy.weapon_damage = 0
                    break

                else:
                    print(f'{Back.RED}Вы промахнулсь!{Back.RESET}')
                    time.sleep(1)
                    return 'miss'


            elif where == 3:
                where = 'телу'
                if enemy.body.legs <= 0:
                    enemy.body.arms -= damage


                elif random.random() < 0.9:
                    enemy.body.arms -= damage

                else:
                    print(f'{Back.RED}Вы промахнулсь!{Back.RESET}')
                    time.sleep(1)
                    return 'miss'
                break

            elif where == 4:
                where = 'голове'
                if enemy.body.legs <= 0 and random.random() < 0.9:
                    enemy.body.head -= int(damage * 2.5)
                    damage *= 2.5

                elif random.random() < 0.3:
                    enemy.body.head -= int(damage * 2.5)
                    damage *= 2.5

                else:
                    print(f'{Back.RED}Вы промахнулсь!{Back.RESET}')
                    time.sleep(1)
                    return 'miss'
                break

        return [int(damage), crit, where]

    def lvl_up(self):
        self.lvl += 1
        self.max_exp, self.exp  = self.exp * 1.5, self.exp - self.max_exp
        print(f'\n{Back.GREEN}Вы повысили уровень!{Back.RESET}\n')
        time.sleep(1)
        choice = int(input(f'{Fore.GREEN}1) Ловкость{Fore.RESET}\n'
                       f'{Fore.RED}2) Сила\n{Fore.RESET
                       }'
                       f'{Fore.BLUE}3) Интелект\n{Fore.RESET}'
                       f'Выберите что хотите прокачать: '))
        if choice == 1:
            self.agillity += 1
            self.avoid = (1 + self.agillity * 2) * 0.01
            self.armor = self.agillity
        elif choice == 2:
            self.straight += 1
            self.damage = 10 * self.straight + self.weapon.damage
            self.max_health = 100 + self.straight * 4
        elif choice == 3:
            self.intelligence += 1


class Enemy(Hero):
    def __init__(self, health, damage):
        self.name = random.choice(['Гоблин', 'Зомби', 'Разбойник', 'Киборг'])
        if self.name == 'Гоблин':
            self.health = damage * random.randint(4, 5)
            self.reward_money = int(self.health * 0.5)
            self.reward_exp = int(self.health * 0.3)
            self.body = Body(health*0.8)
            self.weapon_damage = health * 0.25
            self.base_damage = health * 0.1
            self.damage = self.weapon_damage + self.base_damage

        elif self.name == 'Зомби':
            self.health = damage * random.randint(2, 3)
            self.reward_money = int(self.health * 0.5)
            self.reward_exp = int(self.health * 0.3)
            self.body = Body(health * 0.8)
            self.weapon_damage = 0
            self.base_damage = health * 0.3
            self.damage = self.weapon_damage + self.base_damage

        elif self.name == 'Разбойник':
            self.health = damage * random.randint(3, 4)
            self.reward_money = int(self.health * 0.5)
            self.reward_exp = int(self.health * 0.3)
            self.body = Body(self.health)
            self.weapon_damage = health * 0.4
            self.base_damage = health * 0.1
            self.damage = self.weapon_damage + self.base_damage

        elif self.name == 'Киборг':
            self.health = damage * random.randint(5, 6)
            self.reward_money = int(self.health * 0.5)
            self.reward_exp = int(self.health * 0.3)
            self.body = Body(health * 0.8)
            self.weapon_damage = health * 0.25
            self.base_damage = health * 0.1
            self.damage = self.weapon_damage + self.base_damage




    def info(self):
        print(f'Враг: {self.name}\n'
              f'{Fore.RED}Здоровье: {self.health}{Fore.RESET}\n'
              f'{Fore.LIGHTRED_EX}Базовый урон: {int(self.base_damage)}{Fore.RESET}\n'
              f'{Fore.LIGHTRED_EX}Урон оружия: {int(self.weapon_damage)}{Fore.RESET}\n'
              f'{Fore.LIGHTRED_EX}Общиц урон: {int(self.damage)}{Fore.RESET}\n'
              )

    def atack(self, hero):
        mini_random_dmg = random.randint(0, 5)
        damage = self.damage
        plus_or_minus = random.randint(1, 2)
        if plus_or_minus == 1:
            damage += mini_random_dmg
        elif plus_or_minus == 2:
            damage -= mini_random_dmg

        crit = False
        if random.randint(1, 10) == 10:
            damage = self.damage * 2
            crit = True

        if random.random() < hero.avoid:
            return 'miss'
        return [int(damage-hero.armor*0.01*damage), crit]


