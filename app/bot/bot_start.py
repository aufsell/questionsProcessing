import os,sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
sys.path.append(os.path.join(os.getcwd(), 'app'))
from utils.create_db import init_db

from bot.handlers import user


async def bot_start(db_file, logger):
    await init_db(db_file, logger)
    bot = Bot(os.getenv('TOKEN'),
              default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
              )

    dp = Dispatcher()
    dp.include_router(user.router)

    logger.info('Bot started successfully')
    await bot.delete_webhook(True)
    await dp.start_polling(bot)
