import json
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import config

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_message(message: Message):
    if not os.path.exists(f"messages/chathistory{message.chat.id}.json"):
        with open(f"messages/chathistory{message.chat.id}.json", 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=4)

    with open(f"messages/chathistory{message.chat.id}.json", 'r', encoding='utf-8') as f:
        messages = json.load(f)

    new_message = {
        'text': message.text,
        'sender_username': message.from_user.username,
        'sender_id': message.from_user.id,
        'reply_to_username': message.reply_to_message.from_user.username if message.reply_to_message else None,
        'reply_to_id': message.reply_to_message.from_user.id if message.reply_to_message else None,
        'reply_to_text': message.reply_to_message.text if message.reply_to_message else None,
        'date': message.date.isoformat()
    }
    messages.append(new_message)

    with open(f"messages/chathistory{message.chat.id}.json", 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())