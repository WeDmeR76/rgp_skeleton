import random
from colorama import Fore, Back
import time
from classes import *


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


