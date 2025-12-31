"""Add ai_reasoning column to tasks table."""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from app.config import settings

async def add_ai_reasoning():
    """Add ai_reasoning column to tasks table."""

    engine = create_async_engine(settings.database_url, echo=True)
    async_session = async_sessionmaker(engine)

    async with async_session() as session:
        async with session.begin():
            print("Adding ai_reasoning column to tasks table...")

            try:
                await session.execute(text("""
                    ALTER TABLE tasks
                    ADD COLUMN IF NOT EXISTS ai_reasoning TEXT;
                """))
                print("✓ Added ai_reasoning column")
            except Exception as e:
                print(f"ai_reasoning: {e}")

            print("\n✅ Migration completed!")

if __name__ == "__main__":
    asyncio.run(add_ai_reasoning())
