import asyncio
import os
import sys
import logging

import dotenv

sys.path.append(os.path.join(os.getcwd(), '..'))

from bot.bot_start import bot_start # noqa

dotenv.load_dotenv()
db_file = os.getenv('DB_URL')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    asyncio.run(bot_start(db_file=db_file, logger=logger))
