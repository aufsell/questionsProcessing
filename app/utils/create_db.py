import os

from sqlalchemy.ext.asyncio import create_async_engine

from models.models import Base


async def init_db(db_file, logger):
    if not os.path.exists(db_file.split('///')[-1]):
        engine = create_async_engine(db_file, echo=True)

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        logger.info('Database and tables created successfully.')
    else:
        logger.info('Database already exists. No action taken.')
