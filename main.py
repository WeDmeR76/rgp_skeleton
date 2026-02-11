import random
from colorama import Fore, Back
import time



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






#=============БОЙ==================
def fight(hero):
    number_of_round = 0
    enemy = Enemy(hero.max_health, hero.damage)
    win = False
    enemy.info()
    print(enemy.body.show_body())
    while True:
        number_of_round += 1

        if win:
            print(f'\n{Back.GREEN}Награда:{Back.RESET}')
            print(f'{Fore.LIGHTYELLOW_EX}{enemy.reward_money} монет{Fore.RESET}')
            print(f'{Fore.CYAN}{enemy.reward_exp} опыта{Fore.RESET}')
            hero.exp += enemy.reward_exp
            hero.money += enemy.reward_money
            if hero.exp > hero.max_exp:
                hero.lvl_up()
            break


        #=====ХОД ИГРОКА=======
        if number_of_round % 2 != 0:
            while True:
                choice = int(input(f'1) Атака\n'
                      f'2) Инвентрарь\n'
                      f'3) Посмотреть информацию о себе\n'
                      f'4) Посмотреть информацию о враге\n'
                      f'Выберите действие: '))



                #===АТАКА===
                if choice == 1:
                    atack = hero.atack(enemy)

                    if atack == 'miss':
                        break

                    damage = int(atack[0])
                    crit = atack[1]
                    where = atack[2]
                    enemy.health -= damage

                    if crit:
                        print(f'Критический удар! Вы нанесли {Fore.RED}{damage} урона{Fore.RESET} по {where}\n')
                    else:
                        print(f'Вы атакуете и наносите {Fore.RED}{damage} урона{Fore.RESET} по {where}\n')

                    if enemy.health <= 0:
                        enemy.body.death()
                        win = True
                        print(f'{Fore.LIGHTGREEN_EX}Вы победили!{Fore.RESET}\n')
                        print(f'\n{enemy.body.show_body()}\n')
                        time.sleep(3)
                        break
                    print(f'\n{enemy.body.show_body()}\n')
                    enemy.info()
                    time.sleep(2)
                    break


                #=======ИНВЕНТАРЬ=========
                elif choice == 2:

                    print(f'\n{hero.show_inventory()}')
                    choice = int(input('\nВыберите зелье или вернитесь назад введя 0: '))
                    if choice == 0:
                        pass
                    else:
                        heal = hero.inventory.pop(choice - 1).heal + hero.intelligence * 5
                        hero.health += heal
                        if hero.health > hero.max_health:
                            hero.health = hero.max_health
                        print(f'\nВы пополнили здоровье на {Fore.RED}{heal} ед.{Fore.RESET}\n')

                elif choice == 3:
                    hero.info()

                elif choice == 4:
                    print('')
                    enemy.info()
                    print(enemy.body.show_body())




        #=======ХОД ПРОТИВНИКА========
        elif number_of_round % 2 == 0:
            atack = enemy.atack(hero)
            if atack == 'miss':
                print(f'\n{Back.RED}Противник промахнулся!{Back.RESET}\n')

            else:
                damage = int(atack[0])
                crit = atack[1]
                hero.health -= damage
                hero.health = int(hero.health)
                if crit:
                    print(f'\nВраг нанес критический урон! Вы получили {Fore.RED}{damage} урона{Fore.RESET}\n')
                else:
                    print(f'\nВраг атакует и вы получаете {Fore.RED}{damage} урона{Fore.RESET}\n')

                if hero.health <= 0:
                    print(f'\n{Fore.LIGHTRED_EX}Вы мертвы.{Fore.RESET}\n')
                    time.sleep(2)
                    exit()


def game(hero):
    global small_poison, mid_poison, big_poison
    while True:

        #======МАГАЗИН=======
        hero.health = hero.max_health #лечение в френдли зоне после боя
        print(f'{Back.RED}Магазин зелий:{Back.RESET}\n')
        shop = [small_poison, mid_poison, big_poison]
        while True:
            for i, poison in enumerate(shop, start=1):
                print(f'{i}: {poison.name}\n'
                      f'{Fore.LIGHTRED_EX}Лечение: {poison.heal}{Fore.RESET}\n'
                      f'{Fore.LIGHTYELLOW_EX}Цена: {poison.price}{Fore.RESET}\n')

            print(f'{Fore.CYAN}Ваш инвентарь: {hero.show_inventory()}')
            print(f'{Fore.LIGHTYELLOW_EX}Ваше деньги {hero.money}{Fore.RESET}\n')
            buy = int(input('1, 2, 3) Выбрать какое зелье хотите купить\n'
                            '0) Уйти\n'
                            '4) Персонаж\n'
                            'Выберите действие: '))
            if buy == 0:
                break

            elif buy == 4:
                time.sleep(1)
                hero.info()
                input(f'{Fore.GREEN}Нажмите "Enter" чтобы продолжить{Fore.RESET}\n')

            elif len(hero.inventory) >= 3:
                print(f'\n{Fore.RED}Ваш инвентарь переполнен\n')
                break
            elif hero.money < shop[buy-1].price:
                print(f'{Fore.RED}Недостаточно средств')



            else:
                hero.money -= shop[buy-1].price
                hero.inventory.append(shop.pop(buy-1))
                print(f"\n{Fore.GREEN}Вы купили зелье!{Fore.RESET}\n")



            if shop == []:
                print('\nВы скупили весь магазин\n')
                break

        #=======МАГАЗИН ОРУЖИЯ========
        time.sleep(2)
        print(f'\n{Back.RED}Магазин оружия:{Back.RESET}\n')
        while True:
            shop = []
            for i in range(3):
                weapon_name = random.choice(['Копье', 'Меч', 'Клинки', 'Булава'])
                weapon_price = hero.weapon.price + random.randint(1, 50) * hero.weapon.price
                weapon_damage = int(weapon_price*0.2 + random.randint(1, 50)/100 * hero.weapon.price)
                weapon_crit = int(random.randint(1, 50))
                shop.append(Weapon(weapon_name, weapon_price, weapon_damage, weapon_crit))
            for idx, weapon in enumerate(shop, start=1):
                print(f'{idx}) {weapon.show()}\n')


            print(f'Ваше оружие: {hero.weapon.show()}')
            print(f'{Fore.LIGHTYELLOW_EX}Ваши деньги: {hero.money}{Fore.RESET}\n')
            buy = int(input('1, 2, 3) Выбрать какое оружие хотите купить\n'
                            '0) Уйти\n'
                            '4) Персонаж\n'
                            '5) Реролл (5 монет)\n'
                            'Выберите действие: '))
            if buy == 0:
                break

            elif buy == 4:
                time.sleep(1)
                hero.info()
                input(f'{Fore.GREEN}Нажмите "Enter" чтобы продолжить{Fore.RESET}\n')

            elif buy == 5 and hero.money - 5 >= 0:
                hero.money -= 5
                time.sleep(1)
                print('')
                pass
            elif buy == 5 and hero.money - 5 < 0:
                print(f'{Fore.RED}Недостаточно средств{Fore.RESET}\n')

            elif hero.money < shop[buy-1].price:
                print(f'{Fore.RED}Недостаточно средств{Fore.RESET}')


            else:
                hero.money -= shop[buy - 1].price
                hero.weapon = shop.pop(buy-1)
                hero.damage = 10 * hero.straight + hero.weapon.damage
                print(f"\n{Fore.GREEN}Вы купили новое оружие!{Fore.RESET}\n")
                break






        #==========ПЕРЕХОД В БОЙ=================
        time.sleep(2)
        print(f"\n{Back.LIGHTRED_EX}Вы отправляетесь в бой{Back.RESET}\n")
        fight(hero)


#======НАЧАЛО ИГРЫ============= #fast or slow
def start(how):

    if how == 'slow':
        while True:
            name = input('Выберите имя персонажа: ')
            stats = list(map(int, input('Выберите атрибуты персонажа сила/ловкость/интеллект (всего очков 10): ').split()))
            if sum(stats) != 10:
                print('\nСумма расспределенных очков атрибутов должна быть равна 10\n')
            else:
                hero = Hero(name, stats[0], stats[1], stats[2])
                print("\nВаш персонаж:")
                hero.info()
                choice = input('\nНажмите enter чтобы продолжить или введите 0 чтобы создать персонажа заново: ')
                if choice == '0':
                    pass
                else:
                    print('\n'*100)
                    print(f'{Back.BLACK}Вы долго скитались по миру в поисках знаний{Back.RESET}')
                    time.sleep(2.5)
                    print(f'{Back.BLACK}Вы видели много того, что хотели бы забыть{Back.RESET}')
                    time.sleep(2.5)
                    print(f'{Back.BLACK}Вы потеряли счет времени{Back.RESET}')
                    time.sleep(2.5)
                    print(f'{Back.BLACK}И вот вы очутились в мрачной деревне{Back.RESET}')
                    time.sleep(2.5)
                    print(f'{Back.BLACK}Улицы почти пусты{Back.RESET}')
                    time.sleep(2.5)
                    print(f'{Back.BLACK}Вокруг мертвая тишина, а из окон с недоверием на вас смотрят загадочные силуэты{Back.RESET}')
                    time.sleep(2.5)
                    print(f'{Back.BLACK}Вы набредаете на базар, где стоит один единственный торговец{Back.RESET}')
                    time.sleep(2.5)
                    print(f'{Back.BLACK}Он не вызывает у вас доверия, но вы решаетесь подойти{Back.RESET}')
                    time.sleep(2.5)
                    print(f'{Back.BLACK}Вы спрашиваете у него что здесь происходит{Back.RESET}')
                    time.sleep(2.5)
                    print(f'{Back.BLACK}{Fore.RED}Он молчит.{Back.RESET}')
                    time.sleep(5)
                    print(f'{Back.BLACK}{Fore.RESET}Вы опускаете глаза вниз на прилавок:{Back.RESET} \n')
                    time.sleep(2.5)
                    game(hero)
    elif how == 'fast':
        hero = Hero('fdsfds', 2, 2, 6)
        hero.info()
        game(hero)


start('fast')

