from create import dp
from aiogram import Bot, Dispatcher, types
import spy
import model
from create import kb_main_menu
from datetime import datetime
commands = [
    '\n/start - запустить бота',
    '\n/help - вывести список команд',
    '\n/rules - вывести правила',
    '\n/settings - вывести настройки игры',
    '\n/set - задать количество конфет на старте',
    '\n/take - задать максимум конфет для хода',
    '\n/fate - бросить жребий - кто ходит первым'
    '\n/play - начать игру'
]
waiting = 'menu'



@dp.message_handler(commands=['start'])
async def mes_start(message: types.Message):
    user_name = message.from_user.username
    user_firstname = message.from_user.first_name
    user_id = message.from_user.id
    user_start_time = datetime.now().strftime('%d.%m.%Y, %H:%M:%S')
    
    user_data = []
    user_data.append(user_start_time)
    user_data.append(user_name)
    user_data.append(user_firstname)
    user_data.append(user_id)
    user_data = list(map(str,user_data))
    spy.log(user_data)
    model.start()
    await message.answer('Привет!\nБудем играть в конфеты.\nНаберите /help для вывода списка команд ', reply_markup=kb_main_menu)


@dp.message_handler(commands=['help'])
async def mes_help(message: types.Message):
    global commands
    await message.answer(f'Доступные команды:{"".join(commands)}')

@dp.message_handler(commands=['rules'])
async def mes_rules(message: types.Message):
    answer = model.rules
    await message.answer(answer)



@dp.message_handler(commands=['settings'])
async def mes_help(message: types.Message):
    answer = model.settings()
    await message.answer(answer)


@dp.message_handler(commands=['set'])
async def mes_set(message: types.Message):
    global waiting
    waiting = 'set'
    await message.answer('Сколько конфет возьмём на старт?')

@dp.message_handler(commands=['take'])
async def mes_set(message: types.Message):
    global waiting
    waiting = 'take'
    await message.answer('Какой максимум конфет на ход?')

@dp.message_handler(commands=['fate'])
async def mes_fate(message: types.Message):
    msg = model.fate()
    await message.answer(msg)


@dp.message_handler(commands=['play'])
async def mes_play(message: types.Message):
    global waiting
    waiting = 'human_move'
    answer = model.play()
    await message.answer(answer)
    if 'Бот' in answer:
        answer = model.bot_move()
        await message.answer(answer)

        if 'выиграл' in answer:
            waiting = 'menu'



@dp.message_handler()
async def mes_waiting(message: types.Message):
    global waiting
    user_message = message.text
    if waiting == 'menu' or not user_message.isdigit():
        await message.answer('Это неуместно')
    elif waiting == 'set':
        answer = model.set(int(user_message))
        await message.answer(answer)
        waiting = 'menu'
    elif waiting == 'take':
        answer = model.take(int(user_message))
        await message.answer(answer)
        waiting = 'menu'
    
    elif waiting == 'human_move':
        answer = model.human_move(int(user_message))
        await message.answer(answer)

        if 'выиграл' in answer:
            waiting = 'menu'
        elif 'нельзя' not in answer:
            answer = model.bot_move()
            await message.answer(answer)       

            if 'выиграл' in answer:
                waiting = 'menu'


