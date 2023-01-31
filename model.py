from random import randint as RI

start_candy = 100
current_candy = start_candy
limit_to_take = 28
gamer1_name = 'Человек'
gamer2_name = 'Бот'
current_gamer = gamer1_name
winner = ''


def play() -> str:
    global current_candy
    global start_candy
    global limit_to_take
    limit_to_take = 28
    if current_candy == 0:
        current_candy = start_candy
    message = f'Начали!\nНа столе {current_candy} конфет\nПервым ходит {current_gamer}'
    if current_gamer == gamer1_name:
        message += 'Сколько конфет возьмёте?' 
    return message

def settings() -> str:
    global current_candy
    global current_candy
    global limit_to_take
    message = ''
    message += f'На старте будет {current_candy} конфет\n'
    message += f'За раз можно брать не более {limit_to_take} конфет\n'
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
    current_candy = custom_start_candy
    message = f'На старте будет {current_candy} конфет'
    return message


def human_move(human_takes: int) -> str:
    global current_gamer
    global current_candy
    global limit_to_take
    if human_takes > limit_to_take or human_takes < 1:
        message = f'Столько конфет брать нельзя\nНа столе осталось {current_candy} конфет\nЗа раз можно брать не более {limit_to_take} конфет'
    else:
        current_gamer = gamer2_name
        current_candy -= human_takes
        if current_candy <= limit_to_take:
            limit_to_take = current_candy
        message = f'Вы взяли {human_takes} конфет\nНа столе осталось {current_candy} конфет\nЗа раз можно брать не более {limit_to_take} конфет'
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
    current_gamer = gamer1_name
    message = f'Бот взял {bot_takes} конфет\nНа столе осталось {current_candy} конфет\nЗа раз можно брать не более {limit_to_take} конфет\nСколько конфет возьмёте?'
    return message


def is_win() -> str:
    global current_candy
    global current_gamer
    global winner
    message = ''
    if current_gamer == gamer2_name:

        if current_candy == 0:
            winner =  current_gamer
            message = f'{winner} выиграл!'
        current_gamer = gamer1_name
    elif current_gamer == gamer1_name:
        
        if current_candy == 0:
            winner =  current_gamer
            message = f'{winner} выиграл!'
        current_gamer = gamer2_name
    return message
