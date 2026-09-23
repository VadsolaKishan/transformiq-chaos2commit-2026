import os
import uuid
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.config.database import get_db
from fastapi.security import HTTPAuthorizationCredentials
from app.auth.deps import get_current_user, verify_project_access, security_scheme
from app.auth.security import decode_access_token
from app.models.user import User
from app.models.project import Project
from app.models.transformation import Gap, Solution, Requirement
from app.models.planning import TransformationScore, Estimate
from app.models.collaboration import ExportJob
from app.schemas.project import ApiResponse
from app.exports.generator import (
    generate_pdf_blueprint,
    generate_docx_blueprint,
    generate_xlsx_blueprint,
    generate_pptx_blueprint
)

router = APIRouter(prefix="/exports", tags=["Export Engine"])

@router.get("/project/{project_id}/download")
async def download_export(
    project_id: str,
    format: str = Query("pdf", pattern="^(pdf|docx|xlsx|pptx)$"),
    token: Optional[str] = Query(None),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: AsyncSession = Depends(get_db)
):
    jwt_token = token or (credentials.credentials if credentials else None)
    if not jwt_token:
        raise HTTPException(status_code=401, detail="Authentication token required to download blueprint.")
        
    payload = decode_access_token(jwt_token)
    if not payload or not payload.get("sub"):
        raise HTTPException(status_code=401, detail="Invalid or expired access token.")
        
    user_id = payload.get("sub")
    user_res = await db.execute(select(User).filter(User.id == user_id))
    current_user = user_res.scalars().first()
    if not current_user:
        raise HTTPException(status_code=401, detail="User account not found.")

    project = await verify_project_access(project_id, current_user, db)
    
    # Gather project data for exporter
    gaps_res = await db.execute(select(Gap).filter(Gap.project_id == project.id))
    gaps = gaps_res.scalars().all()
    
    sol_res = await db.execute(select(Solution).filter(Solution.project_id == project.id))
    sol = sol_res.scalars().first()
    
    export_dir = "./exports_generated"
    os.makedirs(export_dir, exist_ok=True)
    
    export_data = {
        "name": project.name,
        "industry": project.industry,
        "executive_summary": sol.executive_summary if sol else (project.business_problem or "Digital transformation blueprint."),
        "gaps": [{
            "category": g.category,
            "current_state": g.current_state,
            "desired_state": g.desired_state,
            "severity": g.severity,
            "recommended_action": g.recommended_action
        } for g in gaps]
    }
    
    clean_name = "".join(c for c in project.name if c.isalnum() or c in (' ', '_', '-')).rstrip()
    base_filename = f"{clean_name}_Blueprint_{str(uuid.uuid4())[:6]}"
    
    if format == "pdf":
        file_path = os.path.join(export_dir, f"{base_filename}.pdf")
        generate_pdf_blueprint(export_data, file_path)
        media_type = "application/pdf"
        filename = f"{base_filename}.pdf"
    elif format == "docx":
        file_path = os.path.join(export_dir, f"{base_filename}.docx")
        generate_docx_blueprint(export_data, file_path)
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        filename = f"{base_filename}.docx"
    elif format == "xlsx":
        file_path = os.path.join(export_dir, f"{base_filename}.xlsx")
        generate_xlsx_blueprint(export_data, file_path)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = f"{base_filename}.xlsx"
    elif format == "pptx":
        file_path = os.path.join(export_dir, f"{base_filename}.pptx")
        generate_pptx_blueprint(export_data, file_path)
        media_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        filename = f"{base_filename}.pptx"
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")
        
    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=filename,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

from pydantic import BaseModel
class ExportGenerateRequest(BaseModel):
    project_id: str
    export_format: str = "pdf"
    artifact_type: Optional[str] = "FINAL_BLUEPRINT"

@router.post("/generate", response_model=ApiResponse)
async def generate_export_job(
    req: ExportGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    project = await verify_project_access(req.project_id, current_user, db)
    
    # Gather project data for exporter
    gaps_res = await db.execute(select(Gap).filter(Gap.project_id == project.id))
    gaps = gaps_res.scalars().all()
    
    sol_res = await db.execute(select(Solution).filter(Solution.project_id == project.id))
    sol = sol_res.scalars().first()
    
    export_dir = "./exports_generated"
    os.makedirs(export_dir, exist_ok=True)
    
    export_data = {
        "name": project.name,
        "industry": project.industry,
        "executive_summary": sol.executive_summary if sol else (project.business_problem or "Digital transformation blueprint."),
        "gaps": [{
            "category": g.category,
            "current_state": g.current_state,
            "desired_state": g.desired_state,
            "severity": g.severity,
            "recommended_action": g.recommended_action
        } for g in gaps]
    }
    
    fmt = req.export_format.lower()
    clean_name = "".join(c for c in project.name if c.isalnum() or c in (' ', '_', '-')).rstrip()
    base_filename = f"{clean_name}_Blueprint_{str(uuid.uuid4())[:6]}"
    
    if fmt == "pdf":
        file_path = os.path.join(export_dir, f"{base_filename}.pdf")
        generate_pdf_blueprint(export_data, file_path)
        filename = f"{base_filename}.pdf"
    elif fmt == "docx":
        file_path = os.path.join(export_dir, f"{base_filename}.docx")
        generate_docx_blueprint(export_data, file_path)
        filename = f"{base_filename}.docx"
    elif fmt == "xlsx":
        file_path = os.path.join(export_dir, f"{base_filename}.xlsx")
        generate_xlsx_blueprint(export_data, file_path)
        filename = f"{base_filename}.xlsx"
    elif fmt == "pptx":
        file_path = os.path.join(export_dir, f"{base_filename}.pptx")
        generate_pptx_blueprint(export_data, file_path)
        filename = f"{base_filename}.pptx"
    else:
        raise HTTPException(status_code=400, detail="Unsupported format. Must be pdf, docx, xlsx, or pptx.")

    file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0

    export_job = ExportJob(
        id=str(uuid.uuid4()),
        project_id=project.id,
        export_type=fmt.upper(),
        file_path=file_path,
        file_name=filename,
        file_size=file_size
    )
    db.add(export_job)
    await db.commit()

    return ApiResponse(
        success=True,
        data={
            "id": export_job.id,
            "file_name": filename,
            "file_path": file_path,
            "file_size": file_size,
            "download_url": f"/api/v1/exports/project/{req.project_id}/download?format={fmt}",
            "status": "COMPLETED"
        },
        message=f"{fmt.upper()} export generated successfully"
    )
