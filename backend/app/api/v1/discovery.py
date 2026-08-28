import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Body, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.config.database import get_db
from app.auth.deps import get_current_user, require_project_permission, record_audit_log
from app.auth.permissions import Permission
from app.models.user import User
from app.models.project import Project, BusinessContext
from app.models.transformation import Question
from app.schemas.project import ApiResponse
from app.ai.orchestrator import orchestrator

router = APIRouter(prefix="/discovery", tags=["Discovery & AI Companion"])

@router.get("/project/{project_id}/questions", response_model=ApiResponse)
async def get_discovery_questions(
    project_id: str,
    project: Project = Depends(require_project_permission(Permission.DISCOVERY_CHAT)),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    q_res = await db.execute(select(Question).filter(Question.project_id == project_id).order_by(Question.created_at.asc()))
    questions = q_res.scalars().all()
    
    if not questions:
        default_qs = [
            {"id": "q1", "question_text": "What is the primary customer friction point in this process?", "category": "Problem Statement", "suggested_answers": ["48h turnaround time", "High manual error rate", "Lack of real-time visibility"]},
            {"id": "q2", "question_text": "What legacy software systems are currently handling these requests?", "category": "Technology Landscape", "suggested_answers": ["Custom On-Prem SQL", "Salesforce Service Cloud", "SAP ERP", "Zendesk & Shared Mailboxes"]},
            {"id": "q3", "question_text": "What is the target straight-through processing (STP) rate for phase 1?", "category": "Target Outcomes", "suggested_answers": [">75% STP", ">50% STP", ">90% STP"]}
        ]
        return ApiResponse(success=True, data=default_qs, message="Default discovery questions")
        
    return ApiResponse(
        success=True,
        data=[{
            "id": q.id,
            "question_text": q.question_text,
            "category": q.category,
            "answer_text": q.answer_text,
            "suggested_answers": q.suggested_answers,
            "is_answered": q.is_answered
        } for q in questions]
    )

@router.post("/project/{project_id}/chat", response_model=ApiResponse)
async def chat_with_ai_companion(
    project_id: str,
    message: str = Body(..., embed=True),
    project: Project = Depends(require_project_permission(Permission.DISCOVERY_CHAT)),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    ctx_res = await db.execute(select(BusinessContext).filter(BusinessContext.project_id == project_id))
    ctx = ctx_res.scalars().first()
    context_text = ctx.summary if ctx else (project.business_problem or "")
    
    ai_reply = await orchestrator.chat_companion(
        message=message,
        project_context=f"Project: {project.name}\nIndustry: {project.industry}\nProblem: {project.business_problem}\nContext: {context_text[:1000]}"
    )
    
    return ApiResponse(
        success=True,
        data={"reply": ai_reply, "project_id": project_id},
        message="AI Companion response generated"
    )
