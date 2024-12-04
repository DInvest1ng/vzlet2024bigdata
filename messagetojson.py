import json
import os
import asyncio
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER, LEFT, KICKED, IS_MEMBER
from dbconf import add_user, add_chat, add_user_to_chat, remove_user_from_chat
from aiogram.types import ChatMemberUpdated
import config
import airesponce
import aiofiles

groups = Router()

# MESSAGES

# summary
@groups.message(
    F.chat.type.in_({"group", "supergroup"}),
    Command(commands=['summary'])
)
async def summary(message: Message):
    response = airesponce.answer(f"messages/chathistory{message.chat.id}.json")
    await message.reply(response)

# speech2text
@groups.message(
    F.chat.type.in_({"group", "supergroup"}),
    F.voice
)
async def voice_processing(message: Message, bot):
    # saving
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    destination = f"voice_messages/voice{message.chat.id}.ogg"
    file_content = await bot.download_file(file_path)
    async with aiofiles.open(destination, 'wb') as f:
        await f.write(file_content.getvalue())

    # speech2text
    text = airesponce.speach2text(f"voice_messages/voice{message.chat.id}.ogg")
    os.remove(f"voice_messages/voice{message.chat.id}.ogg")

    # save2json
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

    # answer
    await message.reply(text)

# messages2json
@groups.message(F.chat.type.in_({"group", "supergroup"}))
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

# GROUP MONITORING

@groups.chat_member(
    F.chat.type.in_({"group", "supergroup"}),
    ChatMemberUpdatedFilter(
        member_status_changed=IS_NOT_MEMBER >> MEMBER
    )
)
async def new_member_joined(event: ChatMemberUpdated):
    for member in event.new_chat_member.user:
        add_user(member.id, member.username, None)
        add_chat(event.chat.id, event.chat.title)
        add_user_to_chat(member.id, event.chat.id)

@groups.chat_member(
    F.chat.type.in_({"group", "supergroup"}),
    ChatMemberUpdatedFilter(
        member_status_changed=MEMBER >> (LEFT | KICKED)
    )
)
async def member_left(event: ChatMemberUpdated):
    remove_user_from_chat(event.old_chat_member.user, event.chat.id)

@groups.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER))
async def on_bot_added(event: ChatMemberUpdated):
    chat_id = event.chat.id
    chat_title = event.chat.title
    chat_members = await event.bot.get_chat_members(chat_id)

    for member in chat_members:
        user = member.user
        add_user(user.id, user.username, None)
        add_chat(chat_id, chat_title)
        add_user_to_chat(user.id, chat_id)