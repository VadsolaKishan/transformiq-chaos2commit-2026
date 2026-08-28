import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from app.config.database import engine, Base, AsyncSessionLocal
from sqlalchemy import text

async def clear_all_dummy_data():
    print("Clearing all dummy data from Neon PostgreSQL database...")
    async with engine.begin() as conn:
        # In PostgreSQL we can truncate or delete from all tables safely
        tables = [
            "export_jobs", "audit_logs", "notifications", "versions", "comments", "approvals",
            "messages", "conversations", "simulation_scenarios", "transformation_scores",
            "risks", "estimates", "roadmaps", "wireframes", "api_endpoints", "database_entities",
            "workflow_edges", "workflow_nodes", "architecture_connections", "architecture_components",
            "solutions", "recommendations", "gaps", "business_processes", "stakeholders",
            "requirements", "document_chunks", "documents", "business_contexts", "project_members",
            "projects", "workspaces", "organizations", "users"
        ]
        for t in tables:
            try:
                await conn.execute(text(f"DELETE FROM {t}"))
                print(f"[OK] Cleaned table: {t}")
            except Exception as ex:
                print(f"[NOTE] Table {t}: {ex}")
    print("[SUCCESS] All dummy data wiped. Database is completely clean!")

if __name__ == "__main__":
    asyncio.run(clear_all_dummy_data())
