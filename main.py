import asyncio
import logging
import config

from database import create_tables
from aiogram import Bot, Dispatcher
from handlers import router


async def main():
    create_tables()
    bot = Bot(config.token)
    dp = Dispatcher()
    dp.include_router(router)
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot is offline')
