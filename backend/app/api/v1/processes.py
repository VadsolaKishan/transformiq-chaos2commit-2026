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
from app.models.architecture import WorkflowNode, WorkflowEdge
from app.schemas.project import ApiResponse
from app.ai.orchestrator import orchestrator

router = APIRouter(prefix="/processes", tags=["Process Intelligence & BPMN"])

@router.get("/project/{project_id}", response_model=ApiResponse)
async def get_process_workflow(
    project_id: str,
    project: Project = Depends(require_project_permission(Permission.PROCESS_VIEW)),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    node_res = await db.execute(select(WorkflowNode).filter(WorkflowNode.project_id == project_id))
    nodes = node_res.scalars().all()
    
    edge_res = await db.execute(select(WorkflowEdge).filter(WorkflowEdge.project_id == project_id))
    edges = edge_res.scalars().all()
    
    if not nodes:
        return ApiResponse(
            success=True,
            data={
                "cycle_time_current": "48 Hours",
                "cycle_time_projected": "12 Minutes",
                "efficiency_gain": "87.5%",
                "swimlanes": ["Customer", "AI Engine", "Integration", "Specialist"],
                "nodes": [],
                "edges": []
            }
        )
        
    return ApiResponse(
        success=True,
        data={
            "cycle_time_current": "48 Hours (Manual AS-IS)",
            "cycle_time_projected": "12 Minutes (AI-Powered TO-BE)",
            "efficiency_gain": "87.5% Latency Reduction",
            "swimlanes": ["Customer / Ingress", "TransformIQ AI Core", "Enterprise Systems", "Human Review Specialist"],
            "nodes": [{
                "id": n.id,
                "node_key": n.node_key,
                "label": n.label,
                "node_type": n.node_type,
                "actor": n.actor,
                "description": n.description,
                "swimlane": n.swimlane,
                "position_x": n.position_x,
                "position_y": n.position_y
            } for n in nodes],
            "edges": [{
                "id": e.id,
                "source": e.source_node_id,
                "target": e.target_node_id,
                "label": e.label,
                "condition": e.condition
            } for e in edges]
        }
    )

@router.post("/project/{project_id}/generate", response_model=ApiResponse)
async def generate_process_workflow(
    project_id: str,
    request: Request,
    project: Project = Depends(require_project_permission(Permission.PROCESS_GENERATE)),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    context_data = {
        "name": project.name,
        "industry": project.industry,
        "business_problem": project.business_problem,
        "business_objective": project.business_objective
    }
    
    result = await orchestrator.generate_process_workflow(context_data)
    
    # Clear existing
    old_nodes = await db.execute(select(WorkflowNode).filter(WorkflowNode.project_id == project_id))
    for on in old_nodes.scalars().all():
        await db.delete(on)
        
    old_edges = await db.execute(select(WorkflowEdge).filter(WorkflowEdge.project_id == project_id))
    for oe in old_edges.scalars().all():
        await db.delete(oe)
        
    node_id_map = {}
    for n in result["nodes"]:
        new_id = str(uuid.uuid4())
        node_id_map[n["id"]] = new_id
        db.add(WorkflowNode(
            id=new_id,
            project_id=project_id,
            node_key=n["id"],
            label=n["label"],
            node_type=n["node_type"],
            actor=n["actor"],
            description=n["description"],
            swimlane=n["swimlane"],
            position_x=n["position_x"],
            position_y=n["position_y"]
        ))
        
    for e in result["edges"]:
        src_id = node_id_map.get(e["source"], e["source"])
        tgt_id = node_id_map.get(e["target"], e["target"])
        db.add(WorkflowEdge(
            id=str(uuid.uuid4()),
            project_id=project_id,
            source_node_key=src_id,
            target_node_key=tgt_id,
            label=e.get("label"),
            condition=e.get("condition")
        ))
        
    await record_audit_log(
        db=db,
        user=current_user,
        action="GENERATE_PROCESS_WORKFLOW",
        resource_type="BPMN_PROCESS",
        resource_id=project_id,
        project_id=project_id,
        details=f"{current_user.full_name} generated BPMN process intelligence with {len(result['nodes'])} nodes",
        request=request
    )
        
    await db.commit()
    return ApiResponse(success=True, data=result, message="Process workflow generated successfully")

@router.post("/project/{project_id}/save-layout", response_model=ApiResponse)
async def save_process_layout(
    project_id: str,
    request: Request,
    nodes: List[Dict[str, Any]] = Body(...),
    project: Project = Depends(require_project_permission(Permission.PROCESS_EDIT)),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    for n in nodes:
        node_id = n.get("id")
        pos = n.get("position", {})
        if node_id and pos:
            node_res = await db.execute(select(WorkflowNode).filter(WorkflowNode.id == node_id, WorkflowNode.project_id == project_id))
            wnode = node_res.scalars().first()
            if wnode:
                wnode.position_x = float(pos.get("x", wnode.position_x))
                wnode.position_y = float(pos.get("y", wnode.position_y))
                
    await record_audit_log(
        db=db,
        user=current_user,
        action="UPDATE_PROCESS_LAYOUT",
        resource_type="BPMN_LAYOUT",
        resource_id=project_id,
        project_id=project_id,
        details=f"{current_user.full_name} updated BPMN diagram layout positions",
        request=request
    )
    
    await db.commit()
    return ApiResponse(success=True, message="Process diagram layout saved")
