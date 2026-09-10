import asyncio
from app.config.database import AsyncSessionLocal
from app.models.user import User
from app.models.project import Project
from sqlalchemy.future import select

async def main():
    async with AsyncSessionLocal() as db:
        users = (await db.execute(select(User))).scalars().all()
        projects = (await db.execute(select(Project))).scalars().all()
        print("Users count:", len(users))
        for u in users:
            print(f"  User: {u.email} | {u.role} | {u.full_name}")
        print("Projects count:", len(projects))
        for p in projects:
            print(f"  Project: {p.id} | {p.name} | {p.status}")

if __name__ == "__main__":
    asyncio.run(main())
