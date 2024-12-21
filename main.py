import asyncio
import random
from telebot.async_telebot import AsyncTeleBot
from config import TOKEN

bot = AsyncTeleBot(TOKEN)


@bot.message_handler(commands=['start'])
async def send_welcome(message):
    text = 'Добро пожаловать! С вами Бот-ассистент Магистрант.'
    await bot.reply_to(message, text)


@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    text = 'Я не знаю, что на это ответить!'
    await bot.reply_to(message, text)

asyncio.run(bot.polling())
