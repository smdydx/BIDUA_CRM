"""HR Management endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
import app.crud.crud as crud
import app.schemas.schemas as schemas
from .auth import get_current_user, get_pagination_params

router = APIRouter()

# Department endpoints
@router.post("/departments/", response_model=schemas.DepartmentResponse)
async def create_department(
    department: schemas.DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new department"""
    existing = await crud.department.get_by_name(db, name=department.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department name already exists"
        )
    return await crud.department.create(db, obj_in=department)

@router.get("/departments/", response_model=List[schemas.DepartmentResponse])
async def get_departments(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    is_active: Optional[bool] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get all departments"""
    filters = {}
    if is_active is not None:
        filters['is_active'] = is_active
    
    return await crud.department.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

@router.get("/departments/{department_id}", response_model=schemas.DepartmentResponse)
async def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get department by ID"""
    department = await crud.department.get(db, id=department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@router.put("/departments/{department_id}", response_model=schemas.DepartmentResponse)
async def update_department(
    department_id: int,
    department_update: schemas.DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Update department"""
    department = await crud.department.get(db, id=department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return await crud.department.update(db, db_obj=department, obj_in=department_update)

# Designation endpoints
@router.post("/designations/", response_model=schemas.DesignationResponse)
async def create_designation(
    designation: schemas.DesignationCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new designation"""
    return await crud.designation.create(db, obj_in=designation)

@router.get("/designations/", response_model=List[schemas.DesignationResponse])
async def get_designations(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    department_id: Optional[int] = Query(None),
    is_active: Optional[bool] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get all designations"""
    filters = {}
    if department_id:
        filters['department_id'] = department_id
    if is_active is not None:
        filters['is_active'] = is_active
    
    return await crud.designation.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

# Employee endpoints
@router.post("/employees/", response_model=schemas.EmployeeResponse)
async def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new employee"""
    existing = await crud.employee.get_by_employee_id(db, employee_id=employee.employee_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID already exists"
        )
    return await crud.employee.create(db, obj_in=employee)

@router.get("/employees/", response_model=List[schemas.EmployeeResponse])
async def get_employees(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    department_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    manager_id: Optional[int] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get all employees with filtering"""
    filters = {}
    if department_id:
        filters['department_id'] = department_id
    if status:
        filters['status'] = status
    if manager_id:
        filters['manager_id'] = manager_id
    
    return await crud.employee.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

@router.get("/employees/{employee_id}", response_model=schemas.EmployeeResponse)
async def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get employee by ID"""
    employee = await crud.employee.get(db, id=employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.put("/employees/{employee_id}", response_model=schemas.EmployeeResponse)
async def update_employee(
    employee_id: int,
    employee_update: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Update employee"""
    employee = await crud.employee.get(db, id=employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return await crud.employee.update(db, db_obj=employee, obj_in=employee_update)

# Leave Management
@router.post("/leave-types/", response_model=schemas.LeaveTypeResponse)
async def create_leave_type(
    leave_type: schemas.LeaveTypeCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new leave type"""
    return await crud.leave_type.create(db, obj_in=leave_type)

@router.get("/leave-types/", response_model=List[schemas.LeaveTypeResponse])
async def get_leave_types(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    is_active: Optional[bool] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get all leave types"""
    filters = {}
    if is_active is not None:
        filters['is_active'] = is_active
    
    return await crud.leave_type.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

@router.post("/leave-requests/", response_model=schemas.LeaveRequestResponse)
async def create_leave_request(
    leave_request: schemas.LeaveRequestCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new leave request"""
    return await crud.leave_request.create(db, obj_in=leave_request, created_by_id=current_user.id)

@router.get("/leave-requests/", response_model=List[schemas.LeaveRequestResponse])
async def get_leave_requests(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    employee_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get leave requests with filtering"""
    filters = {}
    if employee_id:
        filters['employee_id'] = employee_id
    if status:
        filters['status'] = status
    
    return await crud.leave_request.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

@router.put("/leave-requests/{request_id}/approve")
async def approve_leave_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Approve a leave request"""
    leave_request = await crud.leave_request.get(db, id=request_id)
    if not leave_request:
        raise HTTPException(status_code=404, detail="Leave request not found")
    
    update_data = {"status": "approved", "approved_by_id": current_user.id}
    await crud.leave_request.update(db, db_obj=leave_request, obj_in=update_data)
    return {"message": "Leave request approved", "success": True}