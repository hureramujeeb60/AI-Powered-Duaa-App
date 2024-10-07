from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

DATABASE_URL = "postgresql+asyncpg://postgres:hurera12@localhost/Dua_App"  # Update with your database info

# Create the async engine and session
engine = create_async_engine(DATABASE_URL, echo=True)
metadata = MetaData()
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        # Ensure that all tables are created
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

