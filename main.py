import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from handlers import router as private_router
import config
from messagetojson import groups

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(private_router)
    dp.include_router(groups)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())