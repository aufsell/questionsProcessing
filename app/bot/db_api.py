import sys
import os

import dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

sys.path.append(os.path.join(os.getcwd(), 'app'))
from models.models import User # noqa

dotenv.load_dotenv()
db_url = os.getenv('DB_URL')

async_engine = create_async_engine(db_url, echo=True)

async_session = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)


async def check_user_existence(user_id):
    async with async_session() as session:
        result = await session.execute(select(User).filter_by(user_id=user_id))
        return bool(result.scalar_one_or_none())
