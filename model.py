from random import randint as RI

start_candy = 100
current_candy = start_candy
start_limit_to_take = 28
limit_to_take = start_limit_to_take
gamer1_name = 'Человек'
gamer2_name = 'Бот'
current_gamer = gamer1_name
winner = ''
rules = '''На столе лежат конфеты. 
Игроки по очереди берут конфеты, не более оговоренного количества за ход.
Игрок, забравший последнюю конфету проигрывает.'''

def play() -> str:
    global current_candy
    global start_candy
    global limit_to_take
    limit_to_take = start_limit_to_take
    current_candy = start_candy
    message = f'Начали!\nНа столе {current_candy} конфет\nПервым ходит {current_gamer}'
    if current_gamer == gamer1_name:
        message += '\nСколько конфет возьмёте?'
    return message


def settings() -> str:
    global start_candy
    global current_gamer
    global start_limit_to_take
    message = ''
    message += f'На старте будет {start_candy} конфет\n'
    message += f'За раз можно брать не более {start_limit_to_take} конфет\n'
    message += f'Первым ходит {current_gamer}\n'

    return message


def fate() -> str:
    global current_gamer
    if RI(1, 2) == 1:
        current_gamer = gamer2_name
    else:
        current_gamer = gamer1_name
    message = f'Первым ходит {current_gamer}'
    return message


def set(custom_start_candy: int) -> str:
    global current_candy
    global start_candy
    start_candy = custom_start_candy
    message = f'На старте будет {start_candy} конфет'
    return message


def take(custom_take_candy: int) -> str:
    global start_limit_to_take
    start_limit_to_take = custom_take_candy
    message = f'Максимум за ход {start_limit_to_take} конфет'
    return message


def human_move(human_takes: int) -> str:
    global current_gamer
    global current_candy
    global limit_to_take
    if human_takes > limit_to_take or human_takes < 1:
        message = f'Столько конфет брать нельзя\nНа столе осталось {current_candy} конфет\nЗа раз можно брать не более {limit_to_take} конфет'
    else:
        current_candy -= human_takes      

        if current_candy <= limit_to_take:
            limit_to_take = current_candy
        message = f'Вы взяли {human_takes} конфет\nНа столе осталось {current_candy} конфет\nЗа раз можно брать не более {limit_to_take} конфет'
        if current_candy == 0:
            winner = current_gamer
            message = f'{winner} выиграл!'
        if current_gamer == gamer2_name:
            current_gamer = gamer1_name
        elif current_gamer == gamer1_name:
            current_gamer = gamer2_name

    return message


def bot_move() -> str:
    global current_gamer
    global current_candy
    global limit_to_take
    if current_candy <= limit_to_take:
        bot_takes = current_candy
    elif current_candy % limit_to_take > 1:
        bot_takes = current_candy % limit_to_take-1
    else:
        bot_takes = 1
    current_candy -= bot_takes
    
    if current_candy <= limit_to_take:
        limit_to_take = current_candy
    message = f'Бот взял {bot_takes} конфет\nНа столе осталось {current_candy} конфет\nЗа раз можно брать не более {limit_to_take} конфет\nСколько конфет возьмёте?'
    if current_candy == 0: 
        winner = current_gamer
        message = f'Бот взял {bot_takes} конфет\nНа столе осталось {current_candy} конфет'
        message += f'\n{winner} выиграл!'
    if current_gamer == gamer2_name:
        current_gamer = gamer1_name
    elif current_gamer == gamer1_name:
        current_gamer = gamer2_name

    return message


def is_win() -> str:
    global current_candy
    global current_gamer
    global winner
    message = 'Продолжаем!'
    if current_candy == 0:

        winner = current_gamer
        message = f'{winner} выиграл!'
        if current_gamer == gamer2_name:
            current_gamer = gamer1_name
        elif current_gamer == gamer1_name:
            current_gamer = gamer2_name
    return message
