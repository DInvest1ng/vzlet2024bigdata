from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
import keyboards as kb
import airesponce
import aiofiles
import os
from aiogram.fsm.state import State, StatesGroup

router = Router()

@router.message(F.chat.type == 'private', CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет! Сначала пройдем обучение или сразу приступим к работе? В случае если что-то не понятно, всегда можно получить краткую выжимку из обучения по команде:\n\n/help', reply_markup=kb.ob_or_next)

@router.message(F.chat.type == 'private', F.text == 'Продолжить ⏩')
async def nnn(message: Message):
    await message.answer("Чем займемся?", reply_markup=kb.Next)

@router.message(F.chat.type == 'private', F.text == 'Обучение 📚')
async def nnn(message: Message):
    await message.answer('Обучение:\n\
\nПервым делом давай выберем, что именно ты хочешь узнать:', reply_markup=kb.education)

@router.message(F.chat.type == 'private', F.text == '⏪ Назад')
async def nnn(message: Message):
    await message.answer(f'Повторим обучение или продолжим', reply_markup=kb.ob_or_next)

@router.message(F.chat.type == 'private', F.text == 'Как мне пользоваться им? ❓')
async def nnn(message: Message):
    await message.answer(f'Что бы получить пересказ переписки отправь комманду /summary в группу где есть этот бот', reply_markup=kb.backinstruct)

@router.message(F.chat.type == 'private', F.text == 'Как добавить бота в чат 🤖')
async def nnn(message: Message):
    await message.answer(f'Найти бота по нику @SlashInatorBot перейти в описание и добавить в нужную группу', reply_markup=kb.backinstruct)

@router.message(F.chat.type == 'private', F.text == 'Безопастно ли это 🔒')
async def nnn(message: Message):
    await message.answer(f'Да, все данные скачиваются и переправляются на анализ, там они обрабатываются и возвращаются вам как ответ, после чего они удаляются - данные у нас не хранятся', reply_markup=kb.backinstruct)

@router.message(F.chat.type == 'private', F.text == 'Пересказ 🗣️')
async def nnn(message: Message):
    await message.answer(f'Эта функция в разработке, пока что воспользуйтесь коммандой /summary в чате', reply_markup=kb.backsummary)

@router.message(F.chat.type == 'private', F.text == 'ГС в текст 📝')
async def nnn(message: Message):
    await message.answer(f'Пришлите голосовое сообщение', reply_markup=kb.backsummary)

@router.message(F.chat.type == 'private', F.text == 'Назад к функционалу 📱')
async def nnn(message: Message):
    await message.answer("Чем займемся?", reply_markup=kb.Next)

@router.message(F.chat.type == 'private', F.text == 'Назад к обучению 📚')
async def nnn(message: Message):
    await message.answer('Обучение:\n\
\nПервым делом давай выберем, что именно ты хочешь узнать:', reply_markup=kb.education)

@router.message(F.chat.type == 'private', F.voice)
async def voice_processing(message: types.Message, bot):
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
    await message.answer(text, reply_markup=kb.backvoice)