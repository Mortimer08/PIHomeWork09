from create import dp
from aiogram import Bot, Dispatcher, types

import model

commands = [
    '\n/start - запустить бота',
    '\n/help - вывести список команд',
    '\n/settings - вывести настройки игры',
    '\n/set - задать количество конфет на старте',
    '\n/fate - бросить жребий - кто ходит первым'
    '\n/play - начать игру'
]
waiting = 'menu'


@dp.message_handler(commands=['start'])
async def mes_start(message: types.Message):
    await message.answer('Привет!\nБудем играть в конфеты.')


@dp.message_handler(commands=['help'])
async def mes_help(message: types.Message):
    global commands
    await message.answer(f'Доступные команды:{"".join(commands)}')

@dp.message_handler(commands=['settings'])
async def mes_help(message: types.Message):
    answer = model.settings()
    await message.answer(answer)


@dp.message_handler(commands=['set'])
async def mes_set(message: types.Message):
    global waiting
    waiting = 'set'
    await message.answer('Сколько конфет возьмём на старт?')


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
        answer = model.is_win()
        await message.answer(answer)
        if 'выиграл' in answer:
            waiting = 'menu'



@dp.message_handler()
async def mes_waiting(message: types.Message):
    global waiting
    user_message = message.text
    if waiting == 'menu' or not user_message.isdigit():
        pass
    elif waiting == 'set':
        answer = model.set(int(user_message))
        await message.answer(answer)
        waiting = 'human_move'
    elif waiting == 'human_move':
        answer = model.human_move(int(user_message))
        await message.answer(answer)
        answer = model.is_win()
        await message.answer(answer)
        if 'выиграл' in answer:
            waiting = 'menu'
        else:
            answer = model.bot_move()
            await message.answer(answer)       
            answer = model.is_win()
            await message.answer(answer)
            if 'выиграл' in answer:
                waiting = 'menu'


