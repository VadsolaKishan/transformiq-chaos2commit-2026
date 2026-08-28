import pytest
import httpx
from app.main import app
from app.config.database import engine, Base, AsyncSessionLocal
from app.seed.demo_data import seed_database

@pytest.fixture(autouse=True, scope="module")
def setup_db():
    pass

@pytest.mark.asyncio
async def test_root_and_health():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        await seed_database(session)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert "TransformIQ" in data["product"]
        assert data["status"] == "HEALTHY"

@pytest.mark.asyncio
async def test_login_and_projects():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        login_resp = await client.post("/api/v1/auth/login", json={
            "email": "demo@transformiq.ai",
            "password": "Demo@12345"
        })
        assert login_resp.status_code == 200
        token = login_resp.json()["data"]["token"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # List projects
        proj_resp = await client.get("/api/v1/projects", headers=headers)
        assert proj_resp.status_code == 200
        assert len(proj_resp.json()["data"]) > 0

@pytest.mark.asyncio
async def test_what_if_simulation():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        proj_resp = await client.get("/api/v1/projects")
        assert proj_resp.status_code == 200
        projects = proj_resp.json()["data"]
        assert len(projects) > 0
        project_id = projects[0]["id"]
        
        sim_resp = await client.post(f"/api/v1/simulations/project/{project_id}/run", json={
            "automation_level": 80,
            "team_size": 7,
            "budget": 160000.0,
            "timeline_months": 4,
            "ai_adoption_level": "HIGH"
        })
        assert sim_resp.status_code == 200
        sim_data = sim_resp.json()["data"]
        assert "expected_roi_percentage" in sim_data
        assert sim_data["automation_level"] == 80
