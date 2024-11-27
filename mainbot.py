import asyncio
import os
from telebot.async_telebot import AsyncTeleBot
import airesponce

bot = AsyncTeleBot('7638095622:AAHvhGP3vwIRc7mvLcBgagCYGPK47X6c2vA')

@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    text = 'Hi, I am LLM'
    await bot.reply_to(message, text)

@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    response = airesponce.answer(message.text)
    await bot.reply_to(message, response)

asyncio.run(bot.polling())