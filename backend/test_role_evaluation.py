"""
Master Test Suite: TransformIQ Admin Role Evaluation & RBAC Integrity Verification
Tests all requirements from the Master Prompt:
1. Admin switches to all 7 roles and returns to Admin.
2. Admin -> Member -> Admin flow.
3. Database immutability (users.role remains ADMIN at all times).
4. Audit logging generates ROLE_EVALUATION_STARTED, ROLE_EVALUATION_SWITCHED, ROLE_EVALUATION_EXITED (never ROLE_CHANGED).
5. Privilege escalation tests: Non-admin users cannot call evaluation or admin endpoints (HTTP 403).
"""

import asyncio
import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "."))

from sqlalchemy.future import select
from app.config.database import AsyncSessionLocal, engine, Base
from app.models.user import User, UserRole
from app.models.collaboration import AuditLog
from app.auth.security import create_access_token, get_password_hash
import httpx
from app.main import app

BASE_URL = "http://testserver/api/v1"
ALL_7_ROLES = [
    "ADMIN",
    "PROJECT_OWNER",
    "BUSINESS_ANALYST",
    "SOLUTION_ARCHITECT",
    "MANAGER",
    "MEMBER",
    "VIEWER"
]

async def run_tests():
    print("=" * 70)
    print("TRANSFORMIQ MASTER EVALUATION MODE & RBAC VERIFICATION SUITE")
    print("=" * 70)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)

    async with AsyncSessionLocal() as db:
        # 1. Ensure test admin exists
        admin_res = await db.execute(select(User).filter(User.email == "admin@transformiq.local"))
        admin_user = admin_res.scalars().first()
        if not admin_user:
            admin_user = User(
                id="test-admin-uuid-001",
                email="admin@transformiq.local",
                hashed_password=get_password_hash("TransformIQ@2026"),
                full_name="Sarah Connor",
                role="ADMIN",
                is_active=True
            )
            db.add(admin_user)
            await db.commit()
            await db.refresh(admin_user)

        # 2. Ensure test member exists
        member_res = await db.execute(select(User).filter(User.email == "member@transformiq.local"))
        member_user = member_res.scalars().first()
        if not member_user:
            member_user = User(
                id="test-member-uuid-002",
                email="member@transformiq.local",
                hashed_password=get_password_hash("TransformIQ@2026"),
                full_name="Liam O'Connor",
                role="MEMBER",
                is_active=True
            )
            db.add(member_user)
            await db.commit()
            await db.refresh(member_user)

    admin_token = create_access_token(subject=admin_user.id)
    member_token = create_access_token(subject=member_user.id)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=BASE_URL) as client:
        # -------------------------------------------------------------
        # TEST 1: Admin Authentication & Initial Role
        # -------------------------------------------------------------
        print("\n[TEST 1] Admin Authentication & DB Role Check...")
        res = await client.get("/auth/me", headers={"Authorization": f"Bearer {admin_token}"})
        assert res.status_code == 200, f"Failed auth/me: {res.text}"
        data = res.json()["data"]
        assert data["role"] == "ADMIN", f"Expected ADMIN, got {data['role']}"
        print(f"  -> SUCCESS: Admin verified. email={data['email']}, role={data['role']}")

        # -------------------------------------------------------------
        # TEST 2: Admin -> Member -> Admin Evaluation Transition Flow
        # -------------------------------------------------------------
        print("\n[TEST 2] Executing Admin -> Member -> Admin Evaluation Flow...")
        
        # Step 2a: Admin -> Member
        res = await client.post(
            "/admin/evaluation/switch",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"evaluation_role": "MEMBER", "previous_evaluation_role": "ADMIN"}
        )
        assert res.status_code == 200, f"Failed Admin->Member: {res.text}"
        data = res.json()["data"]
        assert data["actual_role"] == "ADMIN", "Actual role must remain ADMIN"
        assert data["evaluation_role"] == "MEMBER", "Evaluation role should be MEMBER"
        assert data["action"] == "ROLE_EVALUATION_STARTED", f"Action should be ROLE_EVALUATION_STARTED, got {data['action']}"
        print("  -> Step 2a SUCCESS: Admin switched evaluation to MEMBER (action=ROLE_EVALUATION_STARTED)")

        # Step 2b: Member -> Admin
        res = await client.post(
            "/admin/evaluation/exit",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"previous_evaluation_role": "MEMBER"}
        )
        assert res.status_code == 200, f"Failed Member->Admin: {res.text}"
        data = res.json()["data"]
        assert data["actual_role"] == "ADMIN"
        assert data["evaluation_role"] == "ADMIN"
        assert data["action"] == "ROLE_EVALUATION_EXITED", f"Action should be ROLE_EVALUATION_EXITED, got {data['action']}"
        print("  -> Step 2b SUCCESS: Admin returned evaluation to ADMIN (action=ROLE_EVALUATION_EXITED)")

        # -------------------------------------------------------------
        # TEST 3: Full 7-Role Transition Cycle & Arbitrary Transitions
        # -------------------------------------------------------------
        print("\n[TEST 3] Full 7-Role Evaluation Cycle (Admin -> PO -> BA -> Arch -> Manager -> Member -> Viewer -> Admin)...")
        prev = "ADMIN"
        for target in ALL_7_ROLES[1:] + ["ADMIN"]:
            res = await client.post(
                "/admin/evaluation/switch",
                headers={"Authorization": f"Bearer {admin_token}"},
                json={"evaluation_role": target, "previous_evaluation_role": prev}
            )
            assert res.status_code == 200, f"Failed transition {prev} -> {target}: {res.text}"
            data = res.json()["data"]
            assert data["actual_role"] == "ADMIN"
            assert data["evaluation_role"] == target
            print(f"  -> Transition {prev:18} -> {target:18} : OK (action={data['action']})")
            prev = target

        # -------------------------------------------------------------
        # TEST 4: Database Role Immutability Verification
        # -------------------------------------------------------------
        print("\n[TEST 4] Validating Database Role Immutability...")
        async with AsyncSessionLocal() as db:
            user_check = await db.execute(select(User).filter(User.id == admin_user.id))
            db_admin = user_check.scalars().first()
            assert db_admin.role == "ADMIN", f"FATAL ERROR: Database role was changed! Found: {db_admin.role}"
            print(f"  -> SUCCESS: Database check confirmed users.role = '{db_admin.role}' (NEVER MUTATED)")

        # -------------------------------------------------------------
        # TEST 5: Audit Log Action Classification Check
        # -------------------------------------------------------------
        print("\n[TEST 5] Checking Audit Log Action Classifications...")
        async with AsyncSessionLocal() as db:
            logs_res = await db.execute(
                select(AuditLog).filter(AuditLog.user_id == admin_user.id).order_by(AuditLog.created_at.desc()).limit(15)
            )
            logs = logs_res.scalars().all()
            actions = [l.action for l in logs]
            print(f"  -> Recent audit actions: {actions}")
            assert "ROLE_EVALUATION_STARTED" in actions, "Missing ROLE_EVALUATION_STARTED in audit logs"
            assert "ROLE_EVALUATION_EXITED" in actions, "Missing ROLE_EVALUATION_EXITED in audit logs"
            assert "ROLE_CHANGED" not in actions, "CRITICAL ERROR: Found ROLE_CHANGED in evaluation logs! Must NOT log as ROLE_CHANGED."
            print("  -> SUCCESS: Audit logs correctly categorized as evaluation actions without false RBAC alerts.")

        # -------------------------------------------------------------
        # TEST 6: Privilege Escalation Prevention
        # -------------------------------------------------------------
        print("\n[TEST 6] Privilege Escalation Attack Vector Prevention (Non-Admin -> Admin)...")
        
        # Attack 1: Non-Admin attempting to call evaluation start/switch
        res_esc1 = await client.post(
            "/admin/evaluation/switch",
            headers={"Authorization": f"Bearer {member_token}"},
            json={"evaluation_role": "ADMIN", "previous_evaluation_role": "MEMBER"}
        )
        assert res_esc1.status_code == 403, f"Expected 403 Forbidden for non-admin, got {res_esc1.status_code}"
        print("  -> Attack 1 Blocked: Real Member attempting /admin/evaluation/switch -> HTTP 403 Forbidden")

        # Attack 2: Non-Admin attempting to access admin user management
        res_esc2 = await client.get(
            "/admin/users",
            headers={"Authorization": f"Bearer {member_token}"}
        )
        assert res_esc2.status_code == 403, f"Expected 403 Forbidden for non-admin, got {res_esc2.status_code}"
        print("  -> Attack 2 Blocked: Real Member attempting /admin/users -> HTTP 403 Forbidden")

    print("\n" + "=" * 70)
    print("ALL TEST SCENARIOS PASSED WITH 100% SUCCESS!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(run_tests())
