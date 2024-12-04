import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from handlers import router as private_router
import config
import messagetojson

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher()

class ChatTypeMiddleware:
    async def __call__(self, handler, event, data):
        message: Message = data['event_update'].message
        if message.chat.type in ['group', 'supergroup']:
            data['router'] = messagetojson.groups
        else:
            data['router'] = private_router
        return await handler(event, data)

async def main():
    dp.message.middleware(ChatTypeMiddleware())

    dp.include_router(private_router)
    dp.include_router(messagetojson.groups)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())