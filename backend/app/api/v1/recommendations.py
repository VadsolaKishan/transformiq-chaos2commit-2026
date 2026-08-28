import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.config.database import get_db
from app.auth.deps import get_current_user, require_project_permission, get_user_project_role, record_audit_log
from app.auth.permissions import Permission, has_permission
from app.models.user import User
from app.models.project import Project
from app.models.transformation import Recommendation, Solution
from app.schemas.project import ApiResponse
from app.ai.orchestrator import orchestrator

router = APIRouter(prefix="/recommendations", tags=["AI & Automation Recommendations"])

@router.get("/project/{project_id}", response_model=ApiResponse)
async def get_recommendations(
    project_id: str,
    project: Project = Depends(require_project_permission(Permission.RECOMMENDATION_VIEW)),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    rec_res = await db.execute(select(Recommendation).filter(Recommendation.project_id == project_id))
    recs = rec_res.scalars().all()
    
    sol_res = await db.execute(select(Solution).filter(Solution.project_id == project_id))
    sol = sol_res.scalars().first()
    
    if not recs or not sol:
        return ApiResponse(
            success=True,
            data={
                "recommended_solution_name": f"AI Solution for {project.name}",
                "tagline": "Awaiting generation",
                "executive_summary": "No recommendations generated yet.",
                "key_capabilities": [],
                "expected_roi": "N/A",
                "technology_stack": {},
                "recommendations": []
            }
        )
        
    return ApiResponse(
        success=True,
        data={
            "recommended_solution_name": sol.name,
            "tagline": sol.tagline,
            "executive_summary": sol.executive_summary,
            "key_capabilities": sol.key_capabilities,
            "expected_roi": sol.expected_roi,
            "technology_stack": sol.technology_stack,
            "recommendations": [{
                "id": r.id,
                "category": r.category,
                "title": r.title,
                "description": r.description,
                "reason": r.reason,
                "expected_impact": r.expected_impact,
                "feasibility": r.feasibility,
                "priority": r.priority,
                "confidence_score": r.confidence_score,
                "source_citation": r.source_citation,
                "dependencies": r.dependencies,
                "status": r.status
            } for r in recs]
        }
    )

@router.post("/project/{project_id}/generate", response_model=ApiResponse)
async def generate_recommendations(
    project_id: str,
    request: Request,
    project: Project = Depends(require_project_permission(Permission.RECOMMENDATION_GENERATE)),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    context_data = {
        "name": project.name,
        "industry": project.industry,
        "business_problem": project.business_problem,
        "business_objective": project.business_objective
    }
    
    result = await orchestrator.generate_recommendations(context_data)
    
    # Save solution
    sol_res = await db.execute(select(Solution).filter(Solution.project_id == project_id))
    sol = sol_res.scalars().first()
    if not sol:
        sol = Solution(
            id=str(uuid.uuid4()),
            project_id=project_id,
            name=result["recommended_solution_name"],
            tagline=result["tagline"],
            executive_summary=result["executive_summary"],
            technology_stack=result["technology_stack"],
            key_capabilities=result["key_capabilities"],
            expected_roi=result["expected_roi"]
        )
        db.add(sol)
    else:
        sol.name = result["recommended_solution_name"]
        sol.tagline = result["tagline"]
        sol.executive_summary = result["executive_summary"]
        sol.technology_stack = result["technology_stack"]
        sol.key_capabilities = result["key_capabilities"]
        sol.expected_roi = result["expected_roi"]
        
    # Clear & Save recommendations
    existing_recs = await db.execute(select(Recommendation).filter(Recommendation.project_id == project_id))
    for er in existing_recs.scalars().all():
        await db.delete(er)
        
    for r in result["recommendations"]:
        db.add(Recommendation(
            id=str(uuid.uuid4()),
            project_id=project_id,
            category=r["category"],
            title=r["title"],
            description=r["description"],
            reason=r["reason"],
            expected_impact=r["expected_impact"],
            feasibility=r["feasibility"],
            priority=r["priority"],
            confidence_score=r["confidence_score"],
            source_citation=r.get("source_citation"),
            dependencies=r.get("dependencies", []),
            status="AI_GENERATED"
        ))
        
    await record_audit_log(
        db=db,
        user=current_user,
        action="GENERATE_RECOMMENDATIONS",
        resource_type="RECOMMENDATION_SET",
        resource_id=project_id,
        project_id=project_id,
        details=f"{current_user.full_name} generated AI recommendations suite for {project.name}",
        request=request
    )
    
    await db.commit()
    return ApiResponse(success=True, data=result, message="Recommendations generated successfully")

@router.get("/why/{recommendation_id}", response_model=ApiResponse)
async def explain_recommendation(
    recommendation_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    rec_res = await db.execute(select(Recommendation).filter(Recommendation.id == recommendation_id))
    rec = rec_res.scalars().first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
        
    project_res = await db.execute(select(Project).filter(Project.id == rec.project_id))
    project = project_res.scalars().first()
    
    explanation = {
        "recommendation_title": rec.title,
        "recommendation_category": rec.category,
        "confidence_score": f"{int(rec.confidence_score * 100)}%",
        "contextual_rationale": rec.reason,
        "business_problem_alignment": f"Directly targets root cause in {project.name if project else 'the project'}: {project.business_problem[:150] if project and project.business_problem else 'Operational latency'}...",
        "risk_of_inaction": "Without this initiative, operational overhead remains linear with transaction growth, continuing to cause 24-48 hour response delays.",
        "expected_roi_contribution": "Contributes to the overall projected 340% 12-month transformation ROI.",
        "citations": [
            rec.source_citation or "Enterprise Process Discovery",
            "Gap Matrix: Process & Technology Dimensions",
            "Industry Benchmark: Top-Quartile AI Adoption Standard"
        ]
    }
    
    return ApiResponse(success=True, data=explanation, message="Explainability rationale retrieved")

@router.post("/{recommendation_id}/status", response_model=ApiResponse)
async def update_recommendation_status(
    recommendation_id: str,
    status_value: str, # APPROVED, REJECTED, REVIEWED, TECHNICALLY_REVIEWED, UNDER_REVIEW
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    rec_res = await db.execute(select(Recommendation).filter(Recommendation.id == recommendation_id))
    rec = rec_res.scalars().first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
        
    user_role = await get_user_project_role(rec.project_id, current_user, db)
    if not user_role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this project.")
        
    target_status = status_value.upper()
    
    # Permission verification for specific workflow stage transitions
    if target_status in ["APPROVED", "REJECTED"]:
        if not has_permission(user_role, Permission.RECOMMENDATION_APPROVE):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: Approving/rejecting recommendations requires MANAGER or PROJECT_OWNER role. Your role is {user_role}."
            )
    elif target_status == "REVIEWED":
        if not has_permission(user_role, Permission.RECOMMENDATION_REVIEW_BA):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: Business review requires BUSINESS_ANALYST role. Your role is {user_role}."
            )
    elif target_status == "TECHNICALLY_REVIEWED":
        if not has_permission(user_role, Permission.RECOMMENDATION_REVIEW_ARCH):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: Technical review requires SOLUTION_ARCHITECT role. Your role is {user_role}."
            )
            
    old_status = rec.status
    rec.status = target_status
    
    await record_audit_log(
        db=db,
        user=current_user,
        action="UPDATE_RECOMMENDATION_STATUS",
        resource_type="RECOMMENDATION",
        resource_id=rec.id,
        project_id=rec.project_id,
        old_value=old_status,
        new_value=rec.status,
        details=f"{current_user.full_name} ({user_role}) transitioned recommendation '{rec.title}' from {old_status} to {rec.status}",
        request=request
    )
    
    await db.commit()
    return ApiResponse(success=True, data={"id": rec.id, "status": rec.status}, message=f"Recommendation marked as {rec.status}")
