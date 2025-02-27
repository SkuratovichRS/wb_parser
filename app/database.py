from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.settings import Settings
from app.models import Base

engine = create_async_engine(
    f"postgresql+asyncpg://{Settings.POSTGRES_USER}:{Settings.POSTGRES_PASSWORD}@{Settings.POSTGRES_HOST}:"
    f"{Settings.POSTGRES_PORT}/{Settings.POSTGRES_DB}",
)
DbSession = async_sessionmaker(engine, expire_on_commit=False)


async def init_orm() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm() -> None:
    await engine.dispose()
