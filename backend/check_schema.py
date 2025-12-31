"""Check database schema for plans and tasks tables."""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from app.config import settings

async def check_schema():
    """Check what columns exist in plans and tasks tables."""

    engine = create_async_engine(settings.database_url, echo=True)
    async_session = async_sessionmaker(engine)

    async with async_session() as session:
        # Check plans table columns
        print("\n=== PLANS TABLE COLUMNS ===")
        result = await session.execute(text("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'plans'
            ORDER BY ordinal_position;
        """))
        for row in result:
            print(f"  {row.column_name}: {row.data_type}")

        # Check tasks table columns
        print("\n=== TASKS TABLE COLUMNS ===")
        result = await session.execute(text("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'tasks'
            ORDER BY ordinal_position;
        """))
        for row in result:
            print(f"  {row.column_name}: {row.data_type}")

if __name__ == "__main__":
    asyncio.run(check_schema())
