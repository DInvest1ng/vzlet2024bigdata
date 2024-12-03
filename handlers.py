from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery   

import keyboards as kb

router = Router()

###

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Добрый {"время_суток"}!\
\n{message.from_user.first_name}, хотите ли вы приступить к работе со мной, или же пройти обучения?', reply_markup=kb.ob_or_next)


@router.message(F.text == 'Продолжить')
async def nnn(message: Message):
    await message.answer("Выберете вид пересказа:\n\
\n  ●Полный пересказ - пересказ событий за N сообщений.\
\n  ●Краткий пересказ - только что-то важное, без излишек.\
\n  ●Личный пересказ - только то, что связанно не преименно с вами.\
\n\n выберете из списка ниже.   \
", reply_markup = kb.Next)
    

@router.message(F.text == 'Обучение')
async def nnn(message: Message):
    await message.answer('Обучение:\n\
\nПервым делом давай выберем, что именно ты хочешь узнать:', reply_markup = kb.education)





### продолжить      Тут за тобой Дань

@router.callback_query(F.data == 'PP')
async def PP(callback: CallbackQuery):
    await callback.message.edit_text('VAR1')

@router.callback_query(F.data == 'KP')
async def KP(callback: CallbackQuery):
    await callback.message.edit_text('VAR2')

@router.callback_query(F.data == 'LP')
async def LP(callback: CallbackQuery):
    await callback.message.edit_text('VAR3')

###



### Обучение

@router.callback_query(F.data == 'KDBK')
async def KDBK(callback: CallbackQuery):
    await callback.message.edit_text('')

@router.callback_query(F.data == 'KMPI')
async def KMPI(callback: CallbackQuery):
    await callback.message.edit_text('')

@router.callback_query(F.data == 'BLU')
async def BLU(callback: CallbackQuery):
    await callback.message.edit_text('')
###