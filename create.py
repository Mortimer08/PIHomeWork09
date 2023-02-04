from aiogram import Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_main_menu = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)

btn_settings = KeyboardButton('/settings')
btn_help = KeyboardButton('/help')
btn_rules = KeyboardButton('/rules')
btn_location = KeyboardButton('/lication',request_location=True)

kb_main_menu.add(btn_settings,btn_help)
kb_main_menu.add(btn_rules,btn_location)


key_file = open('key.txt','r')
key = key_file.read()
key_file.close()
bot = Bot(key)

dp = Dispatcher(bot)