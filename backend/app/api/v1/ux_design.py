import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.config.database import get_db
from app.auth.deps import get_current_user, require_project_permission, record_audit_log
from app.auth.permissions import Permission
from app.models.user import User
from app.models.project import Project
from app.models.design import Wireframe
from app.schemas.project import ApiResponse
from app.ai.orchestrator import orchestrator

router = APIRouter(prefix="/ux", tags=["UX Design & Wireframes"])

@router.get("/project/{project_id}", response_model=ApiResponse)
async def get_ux_design(
    project_id: str,
    project: Project = Depends(require_project_permission(Permission.UX_VIEW)),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    wf_res = await db.execute(select(Wireframe).filter(Wireframe.project_id == project.id))
    wfs = wf_res.scalars().all()
    
    if not wfs:
        context_data = {
            "name": project.name,
            "industry": project.industry,
            "business_problem": project.business_problem,
            "business_objective": project.business_objective
        }
        gen_data = await orchestrator.generate_ux_design(context_data)
        for w in gen_data.get("wireframes", []):
            wf_obj = Wireframe(
                id=str(uuid.uuid4()),
                project_id=project.id,
                screen_name=w.get("screen_name", "Screen"),
                purpose=w.get("purpose", "User interface screen"),
                target_users=w.get("target_users", []),
                layout_type=w.get("layout_type", "DASHBOARD"),
                components_json=w.get("components", []),
                user_actions=w.get("user_actions", []),
                preview_mockup=w.get("preview_mockup", {})
            )
            db.add(wf_obj)
        await db.commit()
        wf_res = await db.execute(select(Wireframe).filter(Wireframe.project_id == project.id))
        wfs = wf_res.scalars().all()
        
    return ApiResponse(
        success=True,
        data={
            "ux_strategy": "High-density enterprise design system emphasizing zero-cognitive-friction, dark/light theme harmony, responsive layout, and instant explainability.",
            "personas": [
                {
                    "name": "Elena Rostova",
                    "role": "Chief Operating Officer / Executive Sponsor",
                    "goals": ["Monitor transformation ROI", "Track SLA compliance across departments", "Identify operational bottlenecks early"],
                    "pain_points": ["Static monthly reports", "Lack of real-time drill-down visibility"]
                },
                {
                    "name": "Devin Clark",
                    "role": "Frontline Operations Lead",
                    "goals": ["Process flagged cases with minimal clicks", "Review AI suggestions quickly", "Manage agent shift queues"],
                    "pain_points": ["Context switching between multiple legacy tools", "Repetitive manual categorization"]
                }
            ],
            "user_journey_stages": [
                {"stage": "1. Discovery & Ingestion", "description": "User enters business problem or uploads enterprise SOP/BRD document."},
                {"stage": "2. Intelligence Generation", "description": "AI generates gap analysis, recommendations, and transformation score."},
                {"stage": "3. Interactive Design", "description": "Architect refines React Flow HLD/LLD diagrams, ER schema, and API catalog."},
                {"stage": "4. What-If Simulation", "description": "User tunes budget/team sliders to recalculate timeline and ROI."},
                {"stage": "5. Blueprint Approval & Export", "description": "Executive reviews and exports one-click PDF, Word, Excel, or PPT reports."}
            ],
            "wireframes": [{
                "id": w.id,
                "screen_name": w.screen_name,
                "purpose": w.purpose,
                "target_users": w.target_users or ["Operations Specialist"],
                "layout_type": w.layout_type or "DASHBOARD",
                "components": w.components_json or [],
                "user_actions": w.user_actions or ["Inspect", "Approve", "Export"],
                "preview_mockup": w.preview_mockup or {}
            } for w in wfs]
        }
    )

@router.post("/project/{project_id}/generate", response_model=ApiResponse)
async def generate_ux_design(
    project_id: str,
    request: Request,
    project: Project = Depends(require_project_permission(Permission.UX_GENERATE)),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    context_data = {
        "name": project.name,
        "industry": project.industry,
        "business_problem": project.business_problem,
        "business_objective": project.business_objective
    }
    
    result = await orchestrator.generate_ux_design(context_data)
    
    # Clear existing
    old_wfs = await db.execute(select(Wireframe).filter(Wireframe.project_id == project.id))
    for ow in old_wfs.scalars().all():
        await db.delete(ow)
        
    for w in result.get("wireframes", []):
        db.add(Wireframe(
            id=str(uuid.uuid4()),
            project_id=project.id,
            screen_name=w.get("screen_name", "Screen"),
            purpose=w.get("purpose", "User interface screen"),
            target_users=w.get("target_users", []),
            layout_type=w.get("layout_type", "DASHBOARD"),
            components_json=w.get("components", []),
            user_actions=w.get("user_actions", []),
            preview_mockup=w.get("preview_mockup", {})
        ))
        
    await record_audit_log(
        db=db,
        user=current_user,
        action="GENERATE_UX_DESIGN",
        resource_type="UX_WIREFRAMES",
        resource_id=project.id,
        project_id=project.id,
        details=f"{current_user.full_name} generated {len(result['wireframes'])} interactive UI wireframes",
        request=request
    )
        
    await db.commit()
    return ApiResponse(success=True, data=result, message="UX wireframes generated successfully")
