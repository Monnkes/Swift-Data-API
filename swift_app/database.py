from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from .settings import config
from .utils.data_loader import load_initial_data


engine = create_async_engine(config.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, autoflush=False, autocommit=False
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with SessionLocal() as db:
        await load_initial_data(db)


async def get_db():
    async with SessionLocal() as db:
        yield db
