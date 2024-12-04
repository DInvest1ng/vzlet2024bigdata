from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Message
from dbconf import add_user, add_chat, add_user_to_chat, remove_user_from_chat
import asyncio
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER, LEFT, KICKED, IS_MEMBER
from aiogram.types import ChatMemberUpdated
import logging

checker = Router()

@checker.chat_member(
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

@checker.chat_member(
    F.chat.type.in_({"group", "supergroup"}),
    ChatMemberUpdatedFilter(
        member_status_changed=MEMBER >> (LEFT | KICKED)
    )
)
async def member_left(event: ChatMemberUpdated):
    remove_user_from_chat(event.old_chat_member.user, event.chat.id)

@checker.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER))
async def on_bot_added(event: ChatMemberUpdated):
    chat_id = event.chat.id
    chat_title = event.chat.title
    chat_members = await event.bot.get_chat_members(chat_id)

    for member in chat_members:
        user = member.user
        add_user(user.id, user.username, None)
        add_chat(chat_id, chat_title)
        add_user_to_chat(user.id, chat_id)