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
    wf_res = await db.execute(select(Wireframe).filter(Wireframe.project_id == project_id))
    wfs = wf_res.scalars().all()
    
    if not wfs:
        return ApiResponse(
            success=True,
            data={
                "design_principles": ["Zero-Friction Ingestion", "Transparent AI Rationale", "One-Click Escalation"],
                "target_personas": [],
                "wireframes": []
            }
        )
        
    return ApiResponse(
        success=True,
        data={
            "design_principles": [
                "Zero-Friction Ingestion: Drag-and-drop any enterprise artifact with real-time feedback.",
                "Transparent AI Rationale: Every AI decision exposes confidence score and citation links.",
                "One-Click Escalation: Frontline specialists can override or approve with minimal clicks."
            ],
            "target_personas": [
                {"name": "Operations Lead", "role": "Triages complex exceptions and oversees straight-through queue."},
                {"name": "Business Executive", "role": "Tracks real-time transformation ROI and SLA compliance."}
            ],
            "wireframes": [{
                "id": w.id,
                "screen_name": w.screen_name,
                "route_path": w.route_path,
                "persona": w.persona,
                "description": w.description,
                "layout_json": w.layout_json
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
    old_wfs = await db.execute(select(Wireframe).filter(Wireframe.project_id == project_id))
    for ow in old_wfs.scalars().all():
        await db.delete(ow)
        
    for w in result.get("wireframes", []):
        db.add(Wireframe(
            id=str(uuid.uuid4()),
            project_id=project_id,
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
        resource_id=project_id,
        project_id=project_id,
        details=f"{current_user.full_name} generated {len(result['wireframes'])} interactive UI wireframes",
        request=request
    )
        
    await db.commit()
    return ApiResponse(success=True, data=result, message="UX wireframes generated successfully")
