from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from typing import AsyncGenerator

from config import APP_CONFIG

sync_engine = create_engine(f"sqlite:///{APP_CONFIG.db_file_path}")


async_engine = create_async_engine(
  f"sqlite+aiosqlite:///{APP_CONFIG.db_file_path}", pool_pre_ping=True
)

async_session_maker = async_sessionmaker(
  async_engine,
  class_=AsyncSession,
  expire_on_commit=False,
  autocommit=False,
  autoflush=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
  async with async_session_maker() as session:
    yield session
    await session.close()
