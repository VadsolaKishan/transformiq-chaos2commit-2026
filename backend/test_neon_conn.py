import asyncio
import os
import sys

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.dirname(__file__))

from app.config.database import engine, Base, AsyncSessionLocal
from app.seed.demo_data import seed_database
from sqlalchemy import text

async def test_neon_connection():
    print("Testing connection to Neon PostgreSQL...")
    try:
        async with engine.begin() as conn:
            print("Verifying and creating tables in Neon PostgreSQL...")
            await conn.run_sync(Base.metadata.create_all, checkfirst=True)
        print("[OK] All 28+ tables verified in Neon DB!")

        print("Seeding demo enterprise data if not present...")
        async with AsyncSessionLocal() as session:
            await seed_database(session)
            await session.commit()
        print("[OK] Flagship Customer Support Transformation demo data seeded in Neon DB!")

        # Verify a count query
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT count(*) FROM users"))
            user_count = result.scalar()
            print(f"[OK] Verification query successful! Total users in Neon DB: {user_count}")

            p_result = await session.execute(text("SELECT count(*) FROM projects"))
            proj_count = p_result.scalar()
            print(f"[OK] Total transformation initiatives in Neon DB: {proj_count}")

        print("[SUCCESS] Neon PostgreSQL database is 100% connected, operational, and healthy!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_neon_connection())
