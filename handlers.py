from create import dp
from aiogram import Bot, Dispatcher, types
import model

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

    model.start(message)
    await message.answer('Привет!\nБудем играть в конфеты.\nНаберите /help для вывода списка команд ')


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
    answer = model.settings(message.from_user.id)
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
    answer = model.fate(message.from_user.id)
    await message.answer(answer)


@dp.message_handler(commands=['play'])
async def mes_play(message: types.Message):
    global waiting
    waiting = 'human_move'
    answer = model.play(message.from_user.id)
    await message.answer(answer)
    if 'Бот' in answer:
        answer = model.bot_move(message.from_user.id)
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
        answer = model.set(message.from_user.id,int(user_message))
        await message.answer(answer)
        waiting = 'menu'
    elif waiting == 'take':
        answer = model.take(message.from_user.id,int(user_message))
        await message.answer(answer)
        waiting = 'menu'

    elif waiting == 'human_move':
        answer = model.human_move(message.from_user.id,int(user_message))
        await message.answer(answer)

        if 'выиграл' in answer:
            waiting = 'menu'
        elif 'нельзя' not in answer:
            answer = model.bot_move(message.from_user.id)
            await message.answer(answer)

            if 'выиграл' in answer:
                waiting = 'menu'
