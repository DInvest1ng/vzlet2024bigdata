from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

ob_or_next = ReplyKeyboardMarkup(keyboard=
[
    [KeyboardButton (text='Продолжить')],
    [KeyboardButton (text='Обучение')], 
], 
        one_time_keyboard=True,
        resize_keyboard=True, 
        input_field_placeholder='Выберете пункт меню.'
)

Next = InlineKeyboardMarkup(inline_keyboard=
    [
[InlineKeyboardButton(text = 'полный пересказ', callback_data='PP')],
[InlineKeyboardButton(text = 'краткий пересказ', callback_data='KP')],
[InlineKeyboardButton(text = 'личный пересказ', callback_data='LP')],
    ]

)

education = InlineKeyboardMarkup(inline_keyboard=
    [
[InlineKeyboardButton(text = 'Как добавить бота в канал?', callback_data='KDBK')],
[InlineKeyboardButton(text = 'Как мне пользоваться им?', callback_data='KMPI')],
[InlineKeyboardButton(text = 'Безопастно ли это?', callback_data='BLU')],
    ]

)

'''

'''