
"""CRM Management endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
import app.crud.crud as crud
import app.schemas.schemas as schemas
from .auth import get_current_user, get_pagination_params

router = APIRouter()

# Company endpoints
@router.post("/companies/", response_model=schemas.CompanyResponse)
async def create_company(
    company: schemas.CompanyCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new company"""
    existing = await crud.company.get_by_name(db, name=company.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company name already exists"
        )
    return await crud.company.create(db, obj_in=company)

@router.get("/companies/", response_model=List[schemas.CompanyResponse])
async def get_companies(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    search: Optional[str] = Query(None),
    industry: Optional[str] = Query(None),
    size: Optional[str] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get all companies with search and filtering"""
    filters = {}
    if industry:
        filters['industry'] = industry
    if size:
        filters['size'] = size
    
    return await crud.company.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], 
        filters=filters, search=search
    )

@router.get("/companies/{company_id}", response_model=schemas.CompanyResponse)
async def get_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get company by ID"""
    company = await crud.company.get(db, id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.put("/companies/{company_id}", response_model=schemas.CompanyResponse)
async def update_company(
    company_id: int,
    company_update: schemas.CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Update company"""
    company = await crud.company.get(db, id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return await crud.company.update(db, db_obj=company, obj_in=company_update)

# Contact endpoints
@router.post("/contacts/", response_model=schemas.ContactResponse)
async def create_contact(
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new contact"""
    return await crud.contact.create(db, obj_in=contact)

@router.get("/contacts/", response_model=List[schemas.ContactResponse])
async def get_contacts(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    company_id: Optional[int] = Query(None),
    is_primary: Optional[bool] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get contacts with filtering"""
    filters = {}
    if company_id:
        filters['company_id'] = company_id
    if is_primary is not None:
        filters['is_primary'] = is_primary
    
    return await crud.contact.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

# Lead endpoints
@router.post("/leads/", response_model=schemas.LeadResponse)
async def create_lead(
    lead: schemas.LeadCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new lead"""
    return await crud.lead.create(db, obj_in=lead, created_by_id=current_user.id)

@router.get("/leads/", response_model=List[schemas.LeadResponse])
async def get_leads(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    status: Optional[str] = Query(None),
    assigned_to_id: Optional[int] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get leads with filtering"""
    filters = {}
    if status:
        filters['status'] = status
    if assigned_to_id:
        filters['assigned_to_id'] = assigned_to_id
    
    return await crud.lead.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

# Deal endpoints
@router.post("/deals/", response_model=schemas.DealResponse)
async def create_deal(
    deal: schemas.DealCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new deal"""
    return await crud.deal.create(db, obj_in=deal, created_by_id=current_user.id)

@router.get("/deals/", response_model=List[schemas.DealResponse])
async def get_deals(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    stage: Optional[str] = Query(None),
    owner_id: Optional[int] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get deals with filtering"""
    filters = {}
    if stage:
        filters['stage'] = stage
    if owner_id:
        filters['owner_id'] = owner_id
    
    return await crud.deal.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

@router.get("/deals/revenue/by-stage")
async def get_revenue_by_stage(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get revenue breakdown by deal stage"""
    return await crud.deal.get_revenue_by_stage(db)

# Activity endpoints
@router.post("/activities/", response_model=schemas.ActivityResponse)
async def create_activity(
    activity: schemas.ActivityCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new activity"""
    return await crud.activity.create(db, obj_in=activity, created_by_id=current_user.id)

@router.get("/activities/", response_model=List[schemas.ActivityResponse])
async def get_activities(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    lead_id: Optional[int] = Query(None),
    deal_id: Optional[int] = Query(None),
    is_completed: Optional[bool] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get activities with filtering"""
    filters = {}
    if lead_id:
        filters['lead_id'] = lead_id
    if deal_id:
        filters['deal_id'] = deal_id
    if is_completed is not None:
        filters['is_completed'] = is_completed
    
    return await crud.activity.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

@router.get("/activities/upcoming")
async def get_upcoming_activities(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get upcoming activities for current user"""
    return await crud.activity.get_upcoming_activities(db, user_id=current_user.id)
