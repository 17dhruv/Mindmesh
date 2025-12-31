#!/usr/bin/env python3
"""Add mock data to Supabase database for testing"""

import asyncio
import uuid
from datetime import datetime, timedelta
from sqlalchemy import text
from app.database import engine, async_session, User, Plan, Task

async def add_mock_data():
    """Add mock data to the database"""
    async with async_session() as session:
        try:
            # First, let's create the tables if they don't exist
            # This should match the Supabase schema
            await session.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id VARCHAR PRIMARY KEY,
                    email VARCHAR UNIQUE NOT NULL,
                    full_name VARCHAR,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))

            await session.execute(text("""
                CREATE TABLE IF NOT EXISTS plans (
                    id VARCHAR PRIMARY KEY,
                    user_id VARCHAR NOT NULL REFERENCES users(id),
                    title VARCHAR NOT NULL,
                    description TEXT,
                    status VARCHAR DEFAULT 'draft',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))

            await session.execute(text("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id VARCHAR PRIMARY KEY,
                    plan_id VARCHAR NOT NULL REFERENCES plans(id),
                    title VARCHAR NOT NULL,
                    description TEXT,
                    priority INTEGER DEFAULT 3,
                    status VARCHAR DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))

            await session.commit()
            print("✅ Tables verified/created")

            # Create 3 mock users
            users = []
            for i in range(3):
                user = User(
                    id=str(uuid.uuid4()),
                    email=f"test.user{i+1}@example.com",
                    full_name=f"Test User {i+1}",
                    created_at=datetime.utcnow() - timedelta(days=i*5),
                    updated_at=datetime.utcnow()
                )
                users.append(user)
                session.add(user)

            await session.commit()
            print("✅ Created 3 mock users")

            # Create 5 mock plans
            plans = []
            plan_titles = [
                "Build Mobile App MVP",
                "Learn Machine Learning",
                "Home Renovation Project",
                "Start YouTube Channel",
                "Plan Summer Vacation"
            ]

            for i, title in enumerate(plan_titles):
                plan = Plan(
                    id=str(uuid.uuid4()),
                    user_id=users[i % 3].id,  # Rotate through users
                    title=title,
                    description=f"Detailed plan for {title.lower()}",
                    status="active",
                    created_at=datetime.utcnow() - timedelta(days=i*2),
                    updated_at=datetime.utcnow()
                )
                plans.append(plan)
                session.add(plan)

            await session.commit()
            print("✅ Created 5 mock plans")

            # Create 10 mock tasks
            task_data = [
                ("Research market requirements", "Research and analyze market needs", 5),
                ("Design UI/UX mockups", "Create wireframes and designs", 5),
                ("Set up development environment", "Install tools and frameworks", 3),
                ("Build core functionality", "Implement main features", 5),
                ("Write unit tests", "Create test cases", 3),
                ("Deploy to staging", "Deploy to staging server", 2),
                ("Gather user feedback", "Collect and analyze feedback", 3),
                ("Create documentation", "Write user and developer docs", 2),
                ("Plan marketing strategy", "Design marketing approach", 3),
                ("Launch beta version", "Release beta to users", 5)
            ]

            for i, (title, description, priority) in enumerate(task_data):
                task = Task(
                    id=str(uuid.uuid4()),
                    plan_id=plans[i % len(plans)].id,  # Distribute across plans
                    title=title,
                    description=description,
                    priority=priority,
                    status="pending",
                    created_at=datetime.utcnow() - timedelta(hours=i),
                    updated_at=datetime.utcnow()
                )
                session.add(task)

            await session.commit()
            print("✅ Created 10 mock tasks")

            # Print summary
            print("\n📊 Mock Data Summary:")
            print(f"   Users: 3")
            print(f"   Plans: 5")
            print(f"   Tasks: 10")
            print("\n✅ All mock data inserted successfully!")

        except Exception as e:
            print(f"❌ Error inserting mock data: {e}")
            await session.rollback()

if __name__ == "__main__":
    asyncio.run(add_mock_data())