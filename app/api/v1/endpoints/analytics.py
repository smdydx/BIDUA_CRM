
"""Analytics endpoints"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
import app.crud.crud as crud
import app.schemas.schemas as schemas
from .auth import get_current_user

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_analytics(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get dashboard analytics summary"""
    # Count various entities
    total_users = await crud.user.get_count(db)
    total_employees = await crud.employee.get_count(db)
    total_companies = await crud.company.get_count(db)
    total_leads = await crud.lead.get_count(db)
    total_deals = await crud.deal.get_count(db)
    total_projects = await crud.project.get_count(db)
    total_tasks = await crud.task.get_count(db)
    
    # Get revenue by stage
    revenue_by_stage = await crud.deal.get_revenue_by_stage(db)
    
    return {
        "total_users": total_users,
        "total_employees": total_employees,
        "total_companies": total_companies,
        "total_leads": total_leads,
        "total_deals": total_deals,
        "total_projects": total_projects,
        "total_tasks": total_tasks,
        "revenue_by_stage": revenue_by_stage
    }
