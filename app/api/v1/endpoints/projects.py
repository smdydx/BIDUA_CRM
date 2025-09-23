
"""Project Management endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
import app.crud.crud as crud
import app.schemas.schemas as schemas
from .auth import get_current_user, get_pagination_params

router = APIRouter()

# Project endpoints
@router.post("/projects/", response_model=schemas.ProjectResponse)
async def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new project"""
    return await crud.project.create(db, obj_in=project, created_by_id=current_user.id)

@router.get("/projects/", response_model=List[schemas.ProjectResponse])
async def get_projects(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    status: Optional[str] = Query(None),
    manager_id: Optional[int] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get projects with filtering"""
    filters = {}
    if status:
        filters['status'] = status
    if manager_id:
        filters['manager_id'] = manager_id
    
    return await crud.project.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

@router.get("/projects/{project_id}", response_model=schemas.ProjectResponse)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get project by ID"""
    project = await crud.project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# Task endpoints
@router.post("/tasks/", response_model=schemas.TaskResponse)
async def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new task"""
    return await crud.task.create(db, obj_in=task, created_by_id=current_user.id)

@router.get("/tasks/", response_model=List[schemas.TaskResponse])
async def get_tasks(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    project_id: Optional[int] = Query(None),
    assigned_to_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get tasks with filtering"""
    filters = {}
    if project_id:
        filters['project_id'] = project_id
    if assigned_to_id:
        filters['assigned_to_id'] = assigned_to_id
    if status:
        filters['status'] = status
    if priority:
        filters['priority'] = priority
    
    return await crud.task.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

@router.get("/tasks/overdue")
async def get_overdue_tasks(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get overdue tasks"""
    return await crud.task.get_overdue_tasks(db)

@router.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Update task"""
    task = await crud.task.get(db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return await crud.task.update(db, db_obj=task, obj_in=task_update)
