import uuid
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Body, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.config.database import get_db
from app.auth.deps import get_current_user, require_project_permission, record_audit_log
from app.auth.permissions import Permission
from app.models.user import User
from app.models.project import Project
from app.models.architecture import ArchitectureComponent, ArchitectureConnection
from app.schemas.project import ApiResponse
from app.ai.orchestrator import orchestrator

router = APIRouter(prefix="/architecture", tags=["Solution Architecture Builder"])

@router.get("/project/{project_id}", response_model=ApiResponse)
async def get_architecture(
    project_id: str,
    project: Project = Depends(require_project_permission(Permission.ARCHITECTURE_VIEW)),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    comp_res = await db.execute(select(ArchitectureComponent).filter(ArchitectureComponent.project_id == project_id))
    comps = comp_res.scalars().all()
    
    conn_res = await db.execute(select(ArchitectureConnection).filter(ArchitectureConnection.project_id == project_id))
    conns = conn_res.scalars().all()
    
    if not comps:
        return ApiResponse(
            success=True,
            data={
                "hld_overview": f"Architecture for {project.name}",
                "deployment_model": "Microservices Cloud Native",
                "security_boundaries": ["Zero-Trust Network", "TLS 1.3 Ingress"],
                "data_flow_summary": "Client -> API Gateway -> AI Engine -> PostgreSQL",
                "components": [],
                "connections": []
            }
        )
        
    return ApiResponse(
        success=True,
        data={
            "hld_overview": f"High-Level Architecture for {project.name}: Event-driven microservices pattern with API Gateway, FastAPI core, asynchronous AI inference, and PostgreSQL storage.",
            "deployment_model": "Multi-Zone Kubernetes / Docker Swarm with Azure Container Apps or AWS ECS.",
            "security_boundaries": [
                "Public Ingress protected by Cloudflare WAF & TLS 1.3 Termination",
                "API Gateway with JWT validation and Rate Limiting per tenant",
                "Internal Service Mesh with mTLS and network isolation",
                "Database and Storage encrypted with customer-managed keys (KMS)"
            ],
            "data_flow_summary": "Inbound request -> API Gateway -> Auth check -> AI Engine Classifier -> Vector SOP Search -> PostgreSQL -> Webhook notification.",
            "components": [{
                "id": c.id,
                "name": c.name,
                "layer": c.layer,
                "tech_stack": c.tech_stack,
                "description": c.description,
                "responsibilities": c.responsibilities,
                "position_x": c.position_x,
                "position_y": c.position_y
            } for c in comps],
            "connections": [{
                "id": cn.id,
                "source": cn.source_component_id,
                "target": cn.target_component_id,
                "protocol": cn.protocol,
                "data_payload": cn.data_payload,
                "is_async": cn.is_async
            } for cn in conns],
            "lld_services": [
                {"name": "AuthService", "purpose": "Handles JWT authentication and RBAC guards."},
                {"name": "ContextService", "purpose": "Extracts and chunks enterprise document files."},
                {"name": "AIOrchestratorService", "purpose": "Coordinates multi-agent reasoning and schema validation."},
                {"name": "ExportService", "purpose": "Generates PDF, DOCX, XLSX, and PPTX reports."}
            ]
        }
    )

@router.post("/project/{project_id}/generate", response_model=ApiResponse)
async def generate_architecture(
    project_id: str,
    request: Request,
    project: Project = Depends(require_project_permission(Permission.ARCHITECTURE_GENERATE)),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    context_data = {
        "name": project.name,
        "industry": project.industry,
        "business_problem": project.business_problem,
        "business_objective": project.business_objective
    }
    
    result = await orchestrator.generate_architecture(context_data)
    
    # Clear existing
    old_comps = await db.execute(select(ArchitectureComponent).filter(ArchitectureComponent.project_id == project_id))
    for oc in old_comps.scalars().all():
        await db.delete(oc)
        
    old_conns = await db.execute(select(ArchitectureConnection).filter(ArchitectureConnection.project_id == project_id))
    for ocn in old_conns.scalars().all():
        await db.delete(ocn)
        
    comp_id_map = {}
    for c in result["components"]:
        new_id = str(uuid.uuid4())
        comp_id_map[c["id"]] = new_id
        db.add(ArchitectureComponent(
            id=new_id,
            project_id=project_id,
            name=c["name"],
            layer=c["layer"],
            tech_stack=c["tech_stack"],
            description=c["description"],
            responsibilities=c["responsibilities"],
            position_x=c["position_x"],
            position_y=c["position_y"]
        ))
        
    for cn in result["connections"]:
        src_id = comp_id_map.get(cn["source"], cn["source"])
        tgt_id = comp_id_map.get(cn["target"], cn["target"])
        db.add(ArchitectureConnection(
            id=str(uuid.uuid4()),
            project_id=project_id,
            source_component_id=src_id,
            target_component_id=tgt_id,
            protocol=cn.get("protocol", "HTTPS/REST"),
            data_payload=cn.get("data_payload"),
            is_async=cn.get("is_async", False)
        ))
        
    await record_audit_log(
        db=db,
        user=current_user,
        action="GENERATE_ARCHITECTURE",
        resource_type="ARCHITECTURE",
        resource_id=project_id,
        project_id=project_id,
        details=f"{current_user.full_name} ({current_user.role}) generated solution architecture with {len(result['components'])} components",
        request=request
    )
    
    await db.commit()
    return ApiResponse(success=True, data=result, message="Architecture generated successfully")

@router.post("/project/{project_id}/save-layout", response_model=ApiResponse)
async def save_architecture_layout(
    project_id: str,
    request: Request,
    nodes: List[Dict[str, Any]] = Body(...),
    project: Project = Depends(require_project_permission(Permission.ARCHITECTURE_EDIT)),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    for n in nodes:
        node_id = n.get("id")
        pos = n.get("position", {})
        if node_id and pos:
            comp_res = await db.execute(select(ArchitectureComponent).filter(ArchitectureComponent.id == node_id, ArchitectureComponent.project_id == project_id))
            comp = comp_res.scalars().first()
            if comp:
                comp.position_x = float(pos.get("x", comp.position_x))
                comp.position_y = float(pos.get("y", comp.position_y))
                
    await record_audit_log(
        db=db,
        user=current_user,
        action="UPDATE_ARCHITECTURE_LAYOUT",
        resource_type="ARCHITECTURE_LAYOUT",
        resource_id=project_id,
        project_id=project_id,
        details=f"{current_user.full_name} updated React Flow layout positions for {len(nodes)} components",
        request=request
    )
    
    await db.commit()
    return ApiResponse(success=True, message="Architecture diagram layout saved")
