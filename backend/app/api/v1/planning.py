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
from app.models.planning import Roadmap, Estimate
from app.schemas.project import ApiResponse
from app.ai.orchestrator import orchestrator

router = APIRouter(prefix="/planning", tags=["Implementation Planning & Estimation"])

@router.get("/project/{project_id}", response_model=ApiResponse)
async def get_planning(
    project_id: str,
    project: Project = Depends(require_project_permission(Permission.PLANNING_VIEW)),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    rm_res = await db.execute(select(Roadmap).filter(Roadmap.project_id == project_id))
    roadmap = rm_res.scalars().first()
    
    est_res = await db.execute(select(Estimate).filter(Estimate.project_id == project_id))
    estimate = est_res.scalars().first()
    
    if not roadmap or not estimate:
        return ApiResponse(
            success=True,
            data={
                "roadmap_phases": [],
                "estimate": {"total_estimated_hours": 0, "total_estimated_cost": 0, "duration_months": 0},
                "wbs_tasks": []
            }
        )
        
    wbs = []
    if roadmap and roadmap.phases:
        for p in roadmap.phases:
            for t in p.get("tasks", []):
                wbs.append({
                    "id": str(uuid.uuid4()),
                    "phase_name": p.get("phase_name", "Phase"),
                    "title": t if isinstance(t, str) else t.get("title", "Task"),
                    "description": f"Implementation deliverable for {p.get('phase_name', '')}",
                    "assigned_role": "Engineering & Architecture",
                    "estimated_hours": 40,
                    "status": "PLANNED"
                })
                
    return ApiResponse(
        success=True,
        data={
            "roadmap_phases": roadmap.phases,
            "total_duration_weeks": roadmap.total_duration_weeks,
            "estimate": {
                "total_estimated_hours": estimate.total_estimated_hours,
                "total_estimated_cost": estimate.total_estimated_cost,
                "duration_months": estimate.duration_months,
                "role_breakdown": estimate.roles_breakdown,
                "infra_cost_monthly": estimate.infrastructure_cost
            },
            "wbs_tasks": wbs
        }
    )

@router.post("/project/{project_id}/generate", response_model=ApiResponse)
async def generate_planning(
    project_id: str,
    request: Request,
    project: Project = Depends(require_project_permission(Permission.PLANNING_GENERATE)),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    context_data = {
        "name": project.name,
        "industry": project.industry,
        "business_problem": project.business_problem,
        "business_objective": project.business_objective
    }
    
    result = await orchestrator.generate_planning(context_data)
    
    phases = result.get("phases", result.get("roadmap_phases", []))
    total_weeks = result.get("total_duration_weeks", 16)
    estimate_info = result.get("estimate", result.get("estimates", {}))
    
    # Save Roadmap
    rm_res = await db.execute(select(Roadmap).filter(Roadmap.project_id == project_id))
    roadmap = rm_res.scalars().first()
    if not roadmap:
        roadmap = Roadmap(
            id=str(uuid.uuid4()),
            project_id=project_id,
            name=f"Roadmap for {project.name}",
            phases=phases,
            total_duration_weeks=total_weeks
        )
        db.add(roadmap)
    else:
        roadmap.phases = phases
        roadmap.total_duration_weeks = total_weeks
        
    # Save Estimate
    est_res = await db.execute(select(Estimate).filter(Estimate.project_id == project_id))
    estimate = est_res.scalars().first()
    if not estimate:
        estimate = Estimate(
            id=str(uuid.uuid4()),
            project_id=project_id,
            total_estimated_hours=estimate_info.get("total_estimated_hours", 1200),
            total_estimated_cost=estimate_info.get("total_estimated_cost", 145000.0),
            duration_months=estimate_info.get("duration_months", 4),
            roles_breakdown=estimate_info.get("role_breakdown", estimate_info.get("roles_breakdown", [])),
            infrastructure_cost=estimate_info.get("infra_cost_monthly", estimate_info.get("infrastructure_cost", 450.0))
        )
        db.add(estimate)
    else:
        estimate.total_estimated_hours = estimate_info.get("total_estimated_hours", 1200)
        estimate.total_estimated_cost = estimate_info.get("total_estimated_cost", 145000.0)
        estimate.duration_months = estimate_info.get("duration_months", 4)
        estimate.roles_breakdown = estimate_info.get("role_breakdown", estimate_info.get("roles_breakdown", []))
        
    await record_audit_log(
        db=db,
        user=current_user,
        action="GENERATE_PLANNING",
        resource_type="PLANNING_ROADMAP",
        resource_id=project_id,
        project_id=project_id,
        details=f"{current_user.full_name} generated implementation plan and roadmap",
        request=request
    )
        
    await db.commit()
    return ApiResponse(success=True, data=result, message="Implementation roadmap and estimation generated successfully")
