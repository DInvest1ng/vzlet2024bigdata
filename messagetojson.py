import json
import logging
import telebot
from telebot import types
from datetime import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

MESSAGES_FILE = 'messages.json'
TOKEN = '7000026321:AAGefkqhq_wUvj2WVTAsxgH8sM7YAo8dKY0'

try:
    with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
        messages = json.load(f)
except FileNotFoundError:
    messages = []

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет! Я буду сохранять все сообщения в этом чате.')

@bot.message_handler(commands=['save'])
def save_last_500_messages(message):
    updates = bot.get_updates(offset=-1, limit=500)
    saved_messages = []

    for update in updates:
        if 'message' in update:
            msg = update.message
            message_data = {
                'message_id': msg.message_id,
                'date': datetime.fromtimestamp(msg.date).isoformat(),
                'chat_id': msg.chat.id,
                'text': msg.text,
                'user': {
                    'id': msg.from_user.id,
                    'username': msg.from_user.username,
                    'first_name': msg.from_user.first_name,
                    'last_name': msg.from_user.last_name
                }
            }
            saved_messages.append(message_data)

    with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(saved_messages, f, indent=4, ensure_ascii=False)

    bot.reply_to(message, 'Последние 500 сообщений сохранены в файл messages.json.')

@bot.message_handler(func=lambda message: True)
def save_message(message):
    message_data = {
        'message_id': message.message_id,
        'date': datetime.fromtimestamp(message.date).isoformat(),
        'chat_id': message.chat.id,
        'text': message.text,
        'user': {
            'id': message.from_user.id,
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name
        }
    }
    messages.append(message_data)
    with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    bot.polling(none_stop=True)
