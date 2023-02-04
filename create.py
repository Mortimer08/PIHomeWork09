from aiogram import Bot, Dispatcher


key_file = open('key', 'r')
key = key_file.read()
key_file.close()

bot = Bot(key)

dp = Dispatcher(bot)
