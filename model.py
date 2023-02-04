from random import randint as RI
import spy
from datetime import datetime

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

users = {}


def start(message) -> str:

    global current_candy
    global start_candy
    global limit_to_take
    global gamer1_name
    global gamer2_name
    global winner
    start_candy = 100
    current_candy = start_candy
    start_limit_to_take = 28
    limit_to_take = start_limit_to_take
    gamer1_name = 'Человек'
    gamer2_name = 'Бот'
    current_gamer = gamer1_name
    winner = ''
    user_name = message.from_user.username
    user_firstname = message.from_user.first_name
    user_id = message.from_user.id
    user_start_time = datetime.now().strftime('%d.%m.%Y, %H:%M:%S')

    user_data = []
    user_data.append(user_start_time)
    user_data.append(user_name)
    user_data.append(user_firstname)
    user_data.append(user_id)
    user_data = list(map(str, user_data))
    spy.log(user_data)

    if user_id not in users.keys():
        users[user_id] = {}
        users[user_id]['user_start_time'] = user_start_time
        users[user_id]['user_name'] = user_name
        users[user_id]['user_first_name'] = user_firstname
        users[user_id]['settings'] = {}
        users[user_id]['settings']['start_candy'] = start_candy
        users[user_id]['settings']['current_candy'] = start_candy
        users[user_id]['settings']['start_limit_to_take'] = start_limit_to_take
        users[user_id]['settings']['current_gamer'] = gamer1_name
        users[user_id]['settings']['winner'] = ''

        print(f'{users[user_id]["user_start_time"]} подключился {users[user_id]["user_name"]}, всего игроков онлайн: {len(users.values())}')

    message = f'Начали!\nНа столе {current_candy} конфет\nПервым ходит {current_gamer}'
    if current_gamer == gamer1_name:
        message += '\nСколько конфет возьмёте?'
    return message


def play(userID) -> str:

    # global users

    users[userID]['settings']['limit_to_take'] = users[userID]['settings']['start_limit_to_take']
    users[userID]['settings']['current_candy'] = users[userID]['settings']['start_candy']
    message = f'Начали!\nНа столе {users[userID]["settings"]["current_candy"]} конфет\nПервым ходит {users[userID]["settings"]["current_gamer"]}'
    if users[userID]["settings"]["current_gamer"] == gamer1_name:
        message += '\nСколько конфет возьмёте?'
    return message


def settings(userID) -> str:

    global users
    message = ''
    message += f'На старте будет {users[userID]["settings"]["start_candy"]} конфет\n'
    message += f'За раз можно брать не более {users[userID]["settings"]["start_limit_to_take"]} конфет\n'
    message += f'Первым ходит {users[userID]["settings"]["current_gamer"]}\n'

    return message


def fate(userID) -> str:

    if RI(1, 2) == 1:
        users[userID]["settings"]["current_gamer"] = gamer2_name
    else:
        users[userID]["settings"]["current_gamer"] = gamer1_name
    message = f'Первым ходит {users[userID]["settings"]["current_gamer"]}'
    return message


def set(userID, custom_start_candy: int) -> str:

    users[userID]["settings"]["start_candy"] = custom_start_candy
    message = f'На старте будет {users[userID]["settings"]["start_candy"]} конфет'
    if users[userID]["settings"]["start_limit_to_take"] >= users[userID]["settings"]["start_candy"]:
        users[userID]["settings"]["start_candy"] = users[userID]["settings"]["start_limit_to_take"]*3
        message = f'Максимум за ход {users[userID]["settings"]["start_limit_to_take"]} конфет\nНа старте будет {users[userID]["settings"]["start_candy"]} конфет'
    return message


def take(userID, custom_take_candy: int) -> str:

    users[userID]["settings"]["start_limit_to_take"] = custom_take_candy
    message = f'Максимум за ход {users[userID]["settings"]["start_limit_to_take"]} конфет'
    if users[userID]["settings"]["start_limit_to_take"] >= users[userID]["settings"]["start_candy"]:
        users[userID]["settings"]["start_candy"] = users[userID]["settings"]["start_limit_to_take"]*3
        message = f'Максимум за ход {users[userID]["settings"]["start_limit_to_take"]} конфет\nНа старте будет {users[userID]["settings"]["start_candy"]} конфет'

    return message


def human_move(userID, human_takes: int) -> str:

    if human_takes > users[userID]["settings"]["limit_to_take"] or human_takes < 1:
        message = f'Столько конфет брать нельзя\nНа столе осталось {users[userID]["settings"]["current_candy"]} конфет\nЗа раз можно брать не более {users[userID]["settings"]["limit_to_take"]} конфет'
    else:
        users[userID]["settings"]["current_candy"] -= human_takes

        if users[userID]["settings"]["current_candy"] <= users[userID]["settings"]["limit_to_take"]:
            users[userID]["settings"]["limit_to_take"] = current_candy
        message = f'Вы взяли {human_takes} конфет\nНа столе осталось {users[userID]["settings"]["current_candy"]} конфет\nЗа раз можно брать не более {users[userID]["settings"]["limit_to_take"]} конфет'
        if users[userID]["settings"]["current_candy"] == 0:
            users[userID]["settings"]["winner"] = users[userID]["settings"]["current_gamer"]
            message = f'{users[userID]["settings"]["winner"]} выиграл!'
        if users[userID]["settings"]["current_gamer"] == gamer2_name:
            users[userID]["settings"]["current_gamer"] = gamer1_name
        elif users[userID]["settings"]["current_gamer"] == gamer1_name:
            users[userID]["settings"]["current_gamer"] = gamer2_name

    return message


def bot_move(userID) -> str:

    if users[userID]["settings"]["current_candy"] <= users[userID]["settings"]["limit_to_take"]:
        bot_takes = users[userID]["settings"]["current_candy"]
    elif users[userID]["settings"]["current_candy"] % users[userID]["settings"]["limit_to_take"] > 1:
        bot_takes = users[userID]["settings"]["current_candy"] % users[userID]["settings"]["limit_to_take"]-1
    else:
        bot_takes = 1
    users[userID]["settings"]["current_candy"] -= bot_takes

    if users[userID]["settings"]["current_candy"] <= users[userID]["settings"]["limit_to_take"]:
        users[userID]["settings"]["limit_to_take"] = users[userID]["settings"]["current_candy"]
    message = f'Бот взял {bot_takes} конфет\nНа столе осталось {users[userID]["settings"]["current_candy"]} конфет\nЗа раз можно брать не более {users[userID]["settings"]["limit_to_take"]} конфет\nСколько конфет возьмёте?'
    if users[userID]["settings"]["current_candy"] == 0:
        users[userID]["settings"]["winner"] = users[userID]["settings"]["current_gamer"]
        message = f'Бот взял {bot_takes} конфет\nНа столе осталось {users[userID]["settings"]["current_candy"]} конфет'
        message += f'\n{users[userID]["settings"]["winner"]} выиграл!'
    if users[userID]["settings"]["current_gamer"] == gamer2_name:
        users[userID]["settings"]["current_gamer"] = gamer1_name
    elif users[userID]["settings"]["current_gamer"] == gamer1_name:
        users[userID]["settings"]["current_gamer"] = gamer2_name

    return message
