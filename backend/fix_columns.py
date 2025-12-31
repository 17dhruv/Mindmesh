"""Fix missing AI columns in database."""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from app.config import settings

async def fix_columns():
    """Add missing AI columns."""

    engine = create_async_engine(settings.database_url, echo=False)
    async_session = async_sessionmaker(engine)

    async with async_session() as session:
        async with session.begin():
            print("Adding missing columns to PLANS table...")

            # Check and add ai_generated_data
            try:
                await session.execute(text("""
                    ALTER TABLE plans ADD COLUMN ai_generated_data TEXT;
                """))
                print("  ✓ Added ai_generated_data")
            except Exception as e:
                if "already exists" not in str(e):
                    print(f"  ✗ ai_generated_data: {e}")

            # Check and add original_thought
            try:
                await session.execute(text("""
                    ALTER TABLE plans ADD COLUMN original_thought TEXT;
                """))
                print("  ✓ Added original_thought")
            except Exception as e:
                if "already exists" not in str(e):
                    print(f"  ✗ original_thought: {e}")

            # Check and add ai_metadata
            try:
                await session.execute(text("""
                    ALTER TABLE plans ADD COLUMN ai_metadata TEXT;
                """))
                print("  ✓ Added ai_metadata")
            except Exception as e:
                if "already exists" not in str(e):
                    print(f"  ✗ ai_metadata: {e}")

            print("\nAdding missing columns to TASKS table...")

            # Check and add ai_category
            try:
                await session.execute(text("""
                    ALTER TABLE tasks ADD COLUMN ai_category VARCHAR;
                """))
                print("  ✓ Added ai_category")
            except Exception as e:
                if "already exists" not in str(e):
                    print(f"  ✗ ai_category: {e}")

            # Check and add ai_priority_score
            try:
                await session.execute(text("""
                    ALTER TABLE tasks ADD COLUMN ai_priority_score INTEGER;
                """))
                print("  ✓ Added ai_priority_score")
            except Exception as e:
                if "already exists" not in str(e):
                    print(f"  ✗ ai_priority_score: {e}")

            print("\n✅ All columns added successfully!")

if __name__ == "__main__":
    asyncio.run(fix_columns())
