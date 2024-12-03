import json
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

API_TOKEN = '7000026321:AAGefkqhq_wUvj2WVTAsxgH8sM7YAo8dKY0'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

MESSAGES_FILE = 'messages.json'

if not os.path.exists(MESSAGES_FILE):
    with open(MESSAGES_FILE, 'w') as f:
        json.dump([], f)

@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: Message):
    await message.reply("Привет! Отправь мне сообщение, и я сохраню его в JSON файл.")

@dp.message()
async def handle_message(message: Message):
    with open(MESSAGES_FILE, 'r') as f:
        messages = json.load(f)

    new_message = {
        'text': message.text,
        'sender_username': message.from_user.username,
        'sender_id': message.from_user.id,
        'reply_to_username': message.reply_to_message.from_user.username if message.reply_to_message else None,
        'reply_to_id': message.reply_to_message.from_user.id if message.reply_to_message else None,
        'date': message.date.isoformat()
    }
    messages.append(new_message)

    with open(MESSAGES_FILE, 'w') as f:
        json.dump(messages, f, indent=4)

    await message.reply("Сообщение сохранено!")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())