from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

ob_or_next = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Продолжить ⏩'),
            KeyboardButton(text='Обучение 📚')
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True,
    input_field_placeholder='Выберете пункт меню.'
)

Next = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Пересказ 🗣️'),
            KeyboardButton(text='ГС в текст 📝')
        ],
        [
            KeyboardButton(text='⏪ Назад')
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True,
    input_field_placeholder='Выберете пункт меню.'
)
education = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Как добавить бота в чат 🤖'),
            KeyboardButton(text='Как мне пользоваться им ❓'),
            KeyboardButton(text='Безопастно ли это 🔒')
        ],
        [
            KeyboardButton(text='⏪ Назад')
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True,
    input_field_placeholder='Выберете пункт меню.'
)

backsummary = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='⏪ Назад'),
            KeyboardButton(text="Назад к функционалу 📱")
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True,
    input_field_placeholder='Выберете пункт меню.'
)

backinstruct = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='⏪ Назад'),
            KeyboardButton(text="Назад к обучению 📚")
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True,
    input_field_placeholder='Выберете пункт меню.'
)

backvoice = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Распознать еще 🎤")
        ],
        [
            KeyboardButton(text='⏪ Назад'),
            KeyboardButton(text="Назад к функционалу 📱")
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True,
    input_field_placeholder='Выберете пункт меню.'
)