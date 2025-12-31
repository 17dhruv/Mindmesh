#!/usr/bin/env python3
"""Insert mock data using direct SQL"""

import asyncio
import uuid
from datetime import datetime, timedelta
from sqlalchemy import text
from app.database import engine

async def insert_mock_data():
    """Insert mock data using direct SQL"""
    async with engine.connect() as conn:
        try:
            # Create 3 users
            users = []
            for i in range(3):
                user_id = str(uuid.uuid4())
                users.append(user_id)

                await conn.execute(text("""
                    INSERT INTO users (id, email, full_name, created_at, updated_at)
                    VALUES (:id, :email, :full_name, :created_at, :updated_at)
                """), {
                    'id': user_id,
                    'email': f'test.user{i+1}@example.com',
                    'full_name': f'Test User {i+1}',
                    'created_at': datetime.utcnow() - timedelta(days=i*5),
                    'updated_at': datetime.utcnow()
                })

            await conn.commit()
            print("✅ Created 3 mock users")

            # Create 5 plans
            plans = []
            plan_titles = [
                "Build Mobile App MVP",
                "Learn Machine Learning",
                "Home Renovation Project",
                "Start YouTube Channel",
                "Plan Summer Vacation"
            ]

            for i, title in enumerate(plan_titles):
                plan_id = str(uuid.uuid4())
                plans.append(plan_id)

                await conn.execute(text("""
                    INSERT INTO plans (id, user_id, title, description, status, created_at, updated_at)
                    VALUES (:id, :user_id, :title, :description, :status, :created_at, :updated_at)
                """), {
                    'id': plan_id,
                    'user_id': users[i % 3],
                    'title': title,
                    'description': f'Detailed plan for {title.lower()}',
                    'status': 'active',
                    'created_at': datetime.utcnow() - timedelta(days=i*2),
                    'updated_at': datetime.utcnow()
                })

            await conn.commit()
            print("✅ Created 5 mock plans")

            # Create 10 tasks
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
                await conn.execute(text("""
                    INSERT INTO tasks (id, plan_id, title, description, priority, status, created_at, updated_at)
                    VALUES (:id, :plan_id, :title, :description, :priority, :status, :created_at, :updated_at)
                """), {
                    'id': str(uuid.uuid4()),
                    'plan_id': plans[i % len(plans)],
                    'title': title,
                    'description': description,
                    'priority': priority,
                    'status': 'pending',
                    'created_at': datetime.utcnow() - timedelta(hours=i),
                    'updated_at': datetime.utcnow()
                })

            await conn.commit()
            print("✅ Created 10 mock tasks")

            # Verify data by counting
            users_count = await conn.execute(text("SELECT COUNT(*) FROM users"))
            plans_count = await conn.execute(text("SELECT COUNT(*) FROM plans"))
            tasks_count = await conn.execute(text("SELECT COUNT(*) FROM tasks"))

            print("\n📊 Mock Data Summary:")
            print(f"   Users: {users_count.scalar()}")
            print(f"   Plans: {plans_count.scalar()}")
            print(f"   Tasks: {tasks_count.scalar()}")
            print("\n✅ All mock data inserted successfully!")

        except Exception as e:
            print(f"❌ Error inserting data: {e}")
            await conn.rollback()

if __name__ == "__main__":
    asyncio.run(insert_mock_data())