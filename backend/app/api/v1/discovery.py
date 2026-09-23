import uuid
from typing import List, Optional
from pydantic import BaseModel
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
    q_res = await db.execute(select(Question).filter(Question.project_id == project.id).order_by(Question.created_at.asc()))
    questions = q_res.scalars().all()
    
    if not questions:
        from app.ai.smart_engine import detect_domain
        ctx_data = {
            "name": project.name,
            "industry": project.industry,
            "business_problem": project.business_problem,
            "business_objective": project.business_objective
        }
        domain = detect_domain(ctx_data)
        if domain == "HR_RECRUITING":
            default_qs = [
                {"id": "q1", "question_text": "What is the average monthly resume volume received across all recruiters?", "category": "Candidate Ingestion", "suggested_answers": ["100 - 500 resumes/mo", "500 - 2,000 resumes/mo", "2,000+ resumes/mo"]},
                {"id": "q2", "question_text": "How many recruiters require daily attendance and activity tracking?", "category": "Team Operations", "suggested_answers": ["1 - 5 Recruiters", "6 - 15 Recruiters (e.g. 12 Recruiters)", "15+ Recruiters"]},
                {"id": "q3", "question_text": "What is your target client digital onboarding turnaround time?", "category": "Client SLAs", "suggested_answers": ["Under 3 Days (Target)", "3 - 5 Days", "Under 24 Hours"]}
            ]
        elif domain == "RETAIL_SUPPLY_CHAIN":
            default_qs = [
                {"id": "q1", "question_text": "How many store POS terminals and central warehouses need real-time synchronization?", "category": "Store Architecture", "suggested_answers": ["5 - 20 Stores", "20 - 50 Stores", "50+ Retail Locations"]},
                {"id": "q2", "question_text": "What is the current estimated revenue impact from stockouts and phantom inventory?", "category": "Supply Chain Friction", "suggested_answers": ["5% - 10% lost sales", "10% - 20% lost revenue", "Critical multi-day stockouts"]},
                {"id": "q3", "question_text": "Is offline-first checkout capability required during store internet disruptions?", "category": "Reliability", "suggested_answers": ["Yes, zero store sales downtime required", "Preferred with local cache", "Not required"]}
            ]
        else:
            default_qs = [
                {"id": "q1", "question_text": "What is the primary operational friction point in this workflow?", "category": "Problem Statement", "suggested_answers": ["48h turnaround time", "High manual error rate", "Lack of real-time visibility"]},
                {"id": "q2", "question_text": "What legacy software systems are currently handling these requests?", "category": "Technology Landscape", "suggested_answers": ["Custom On-Prem SQL", "Salesforce / SAP ERP", "Shared Spreadsheets & Mailboxes"]},
                {"id": "q3", "question_text": "What is the target straight-through processing (STP) rate for phase 1?", "category": "Target Outcomes", "suggested_answers": [">75% STP", ">50% STP", ">90% STP"]}
            ]
        return ApiResponse(success=True, data=default_qs, message="Contextual discovery questions")
        
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

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    language: Optional[str] = "en"

@router.post("/project/{project_id}/chat", response_model=ApiResponse)
async def chat_with_ai_companion(
    project_id: str,
    req: ChatRequest,
    project: Project = Depends(require_project_permission(Permission.DISCOVERY_CHAT)),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    ctx_res = await db.execute(select(BusinessContext).filter(BusinessContext.project_id == project.id))
    ctx = ctx_res.scalars().first()
    context_text = ctx.summary if ctx else (project.business_problem or "")
    
    project_context = (
        f"Project Name: {project.name}\n"
        f"Industry Vertical: {project.industry}\n"
        f"Business Problem Statement: {project.business_problem or 'Operational bottlenecks and legacy manual workflows'}\n"
        f"Business Objectives: {project.business_objective or 'Streamline processes and achieve autonomous straight-through processing'}\n"
        f"Business Context Summary: {context_text[:1200]}"
    )
    
    ai_reply = await orchestrator.chat_companion(
        message=req.message,
        project_context=project_context,
        language=req.language or "en"
    )
    
    conv_id = req.conversation_id or str(uuid.uuid4())
    
    suggested_actions = [
        "Analyze AS-IS process flow & bottlenecks",
        "Extract functional & compliance requirements",
        "Execute 8-dimension gap matrix",
        "Calculate TransformIQ readiness score"
    ]
    
    return ApiResponse(
        success=True,
        data={
            "message": ai_reply,
            "reply": ai_reply,
            "conversation_id": conv_id,
            "project_id": project.id,
            "suggested_actions": suggested_actions
        },
        message="AI Companion response generated"
    )
