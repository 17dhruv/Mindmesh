"""Add AI-related columns to plans and tasks tables."""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from app.config import settings

async def add_ai_columns():
    """Add AI columns to the database."""

    engine = create_async_engine(settings.database_url, echo=True)
    async_session = async_sessionmaker(engine)

    async with async_session() as session:
        async with session.begin():
            # Add columns to plans table
            print("Adding AI columns to plans table...")

            # Check if columns exist, add if they don't
            try:
                await session.execute(text("""
                    ALTER TABLE plans
                    ADD COLUMN IF NOT EXISTS ai_generated_data TEXT;
                """))
                print("✓ Added ai_generated_data column")
            except Exception as e:
                print(f"ai_generated_data: {e}")

            try:
                await session.execute(text("""
                    ALTER TABLE plans
                    ADD COLUMN IF NOT EXISTS original_thought TEXT;
                """))
                print("✓ Added original_thought column")
            except Exception as e:
                print(f"original_thought: {e}")

            try:
                await session.execute(text("""
                    ALTER TABLE plans
                    ADD COLUMN IF NOT EXISTS ai_metadata TEXT;
                """))
                print("✓ Added ai_metadata column")
            except Exception as e:
                print(f"ai_metadata: {e}")

            # Add columns to tasks table
            print("\nAdding AI columns to tasks table...")

            try:
                await session.execute(text("""
                    ALTER TABLE tasks
                    ADD COLUMN IF NOT EXISTS ai_category VARCHAR;
                """))
                print("✓ Added ai_category column")

                # Create index if it doesn't exist
                await session.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_tasks_ai_category ON tasks(ai_category);
                """))
                print("✓ Created index on ai_category")
            except Exception as e:
                print(f"ai_category: {e}")

            try:
                await session.execute(text("""
                    ALTER TABLE tasks
                    ADD COLUMN IF NOT EXISTS ai_priority_score INTEGER;
                """))
                print("✓ Added ai_priority_score column")

                # Add check constraint
                await session.execute(text("""
                    ALTER TABLE tasks
                    DROP CONSTRAINT IF EXISTS check_ai_priority_score;
                    ALTER TABLE tasks
                    ADD CONSTRAINT check_ai_priority_score
                    CHECK (ai_priority_score BETWEEN 1 AND 10);
                """))
                print("✓ Added check constraint for ai_priority_score")
            except Exception as e:
                print(f"ai_priority_score: {e}")

            try:
                await session.execute(text("""
                    ALTER TABLE tasks
                    ADD COLUMN IF NOT EXISTS ai_reasoning TEXT;
                """))
                print("✓ Added ai_reasoning column")
            except Exception as e:
                print(f"ai_reasoning: {e}")

            print("\n✅ Migration completed successfully!")

if __name__ == "__main__":
    asyncio.run(add_ai_columns())
