# from aiogram import Update
# from aiogram import ApplicationBuilder, CommandHandler, ContextTypes

def log(data):
    file = open('db.csv', 'a')
    file.write(f'{" | ".join(data)}\n')
    file.close()

