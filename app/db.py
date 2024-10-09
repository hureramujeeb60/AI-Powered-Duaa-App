from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
import logging

logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql+asyncpg://postgres:hurera12@localhost/Dua_App"  # Update with your database info

# Create the async engine and session
engine = create_async_engine(DATABASE_URL, echo=True)
print('engineeeeee', engine)
metadata = MetaData()
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def init_db():
    print("Initializing database and creating tables...")
    async with engine.begin() as conn:
        logger.info("Initializing database and creating tables...")
        # Ensure that all tables are created
        await conn.run_sync(metadata.create_all)  # Corrected here
        logger.info("Database initialized successfully.")


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# Function to run init_db (optional for testing)
async def main():
    await init_db()

# To run the main function if needed
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
