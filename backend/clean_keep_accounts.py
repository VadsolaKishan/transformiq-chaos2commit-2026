"""
TransformIQ Database Sanitizer:
Removes ALL dummy data (projects, documents, workflows, requirements, architecture, tickets, simulations, blueprints, exports)
while strictly preserving user accounts and organizations.
"""

import asyncio
import os
import sys
import shutil

sys.path.insert(0, os.path.dirname(__file__))

from app.config.database import engine, Base, AsyncSessionLocal
from sqlalchemy import text
from sqlalchemy.future import select
from app.models.user import User
from app.auth.security import get_password_hash

ACCOUNT_PRESETS = [
    {
        "id": "usr-admin-001",
        "email": "admin@transformiq.local",
        "full_name": "Sarah Connor",
        "role": "ADMIN",
        "password": "TransformIQ@2026"
    },
    {
        "id": "usr-owner-002",
        "email": "owner@transformiq.local",
        "full_name": "Elena Rostova",
        "role": "PROJECT_OWNER",
        "password": "TransformIQ@2026"
    },
    {
        "id": "usr-analyst-003",
        "email": "analyst@transformiq.local",
        "full_name": "Priya Sharma",
        "role": "BUSINESS_ANALYST",
        "password": "TransformIQ@2026"
    },
    {
        "id": "usr-architect-004",
        "email": "architect@transformiq.local",
        "full_name": "David Vance",
        "role": "SOLUTION_ARCHITECT",
        "password": "TransformIQ@2026"
    },
    {
        "id": "usr-manager-005",
        "email": "manager@transformiq.local",
        "full_name": "Marcus Chen",
        "role": "MANAGER",
        "password": "TransformIQ@2026"
    },
    {
        "id": "usr-member-006",
        "email": "member@transformiq.local",
        "full_name": "Liam O'Connor",
        "role": "MEMBER",
        "password": "TransformIQ@2026"
    },
    {
        "id": "usr-viewer-007",
        "email": "viewer@transformiq.local",
        "full_name": "Victoria Sterling",
        "role": "VIEWER",
        "password": "TransformIQ@2026"
    }
]

async def clean_database_keep_accounts():
    print("=" * 70)
    print("TRANSFORMIQ DATABASE CLEANUP: REMOVING ALL DUMMY DATA (KEEP ACCOUNTS ONLY)")
    print("=" * 70)

    # Tables to wipe completely (everything EXCEPT users and organizations)
    tables_to_wipe = [
        "export_jobs",
        "audit_logs",
        "notifications",
        "versions",
        "comments",
        "approvals",
        "messages",
        "conversations",
        "simulation_scenarios",
        "transformation_scores",
        "risks",
        "estimates",
        "roadmaps",
        "wireframes",
        "api_endpoints",
        "database_entities",
        "workflow_edges",
        "workflow_nodes",
        "architecture_connections",
        "architecture_components",
        "solutions",
        "recommendations",
        "gaps",
        "business_processes",
        "stakeholders",
        "requirements",
        "document_chunks",
        "documents",
        "business_contexts",
        "project_members",
        "projects",
        "workspaces"
    ]

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)

        for table in tables_to_wipe:
            try:
                await conn.execute(text(f"DELETE FROM {table}"))
                print(f"  [OK] Cleaned dummy table: {table}")
            except Exception as e:
                print(f"  [NOTE] Table {table}: {e}")

    # Ensure clean accounts exist
    async with AsyncSessionLocal() as db:
        for acc in ACCOUNT_PRESETS:
            res = await db.execute(select(User).filter(User.email == acc["email"]))
            existing = res.scalars().first()
            if not existing:
                new_user = User(
                    id=acc["id"],
                    email=acc["email"],
                    hashed_password=get_password_hash(acc["password"]),
                    full_name=acc["full_name"],
                    role=acc["role"],
                    is_active=True
                )
                db.add(new_user)
                print(f"  [OK] Seeded clean account: {acc['email']} ({acc['role']})")
            else:
                existing.role = acc["role"]
                existing.full_name = acc["full_name"]
                existing.is_active = True
                print(f"  [OK] Preserved existing account: {acc['email']} ({acc['role']})")
        await db.commit()

    # Clear uploads and exports folder dummy files
    base_dir = os.path.dirname(__file__)
    for folder in ["uploads", "exports_generated"]:
        folder_path = os.path.join(base_dir, folder)
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"  [NOTE] File cleanup note for {file_path}: {e}")
            print(f"  [OK] Purged temporary files in: {folder}/")

    print("=" * 70)
    print("SUCCESS: ALL DUMMY DATA HAS BEEN REMOVED! ONLY ACCOUNTS REMAIN IN DATABASE.")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(clean_database_keep_accounts())
