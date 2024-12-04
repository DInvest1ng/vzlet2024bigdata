import json
import os
import asyncio
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Message
import config
import airesponce
import aiofiles

groups = Router()

#summary
@groups.message(Command(commands=['summary']))
async def summary(message: Message):
    response = airesponce.answer(f"messages/chathistory{message.chat.id}.json")
    await message.reply(response)

#speech2text
@groups.message(F.voice)
async def voice_processing(message: Message, bot):
    #saving
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    destination = f"voice_messages/voice{message.chat.id}.ogg"
    file_content = await bot.download_file(file_path)
    async with aiofiles.open(destination, 'wb') as f:
        await f.write(file_content.getvalue())

    #speech2text
    text = airesponce.speach2text(f"voice_messages/voice{message.chat.id}.ogg")
    os.remove(f"voice_messages/voice{message.chat.id}.ogg")

    #save2json
    file_path = f"messages/chathistory{message.chat.id}.json"
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=4)
    with open(file_path, 'r', encoding='utf-8') as f:
        messages = json.load(f)
    new_message = {
        'text': text,
        'sender_username': message.from_user.username,
        'sender_id': message.from_user.id,
        'reply_to_username': message.reply_to_message.from_user.username if message.reply_to_message else None,
        'reply_to_id': message.reply_to_message.from_user.id if message.reply_to_message else None,
        'reply_to_text': message.reply_to_message.text if message.reply_to_message else None,
        'date': message.date.isoformat()
    }
    messages.append(new_message)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

    #answer
    await message.reply(text)

#messages2json
@groups.message()
async def handle_message(message: Message):
    file_path = f"messages/chathistory{message.chat.id}.json"
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=4)

    with open(file_path, 'r', encoding='utf-8') as f:
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

    if len(messages) > 75:
        messages = messages[-75:]

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)