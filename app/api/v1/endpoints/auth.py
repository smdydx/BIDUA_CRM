"""Authentication endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
import app.crud.crud as crud
import app.schemas.schemas as schemas

router = APIRouter()
security = HTTPBearer(auto_error=False)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user - simplified for demo"""
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # For demo purposes, accept any valid token format
    token = credentials.credentials
    if token == "demo_jwt_token":
        return schemas.UserResponse(
            id=1,
            username="admin",
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            role=schemas.UserRole.ADMIN,
            is_active=True,
            last_login=None,
            created_at="2025-01-01T00:00:00",
            updated_at=None
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_pagination_params(page: int = 1, size: int = 20):
    """Get pagination parameters"""
    if size > 100:
        size = 100
    if page < 1:
        page = 1
    skip = (page - 1) * size
    return {"skip": skip, "limit": size, "page": page, "size": size}

@router.post("/login")
async def login_user(
    login_data: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    """User login endpoint"""
    try:
        # For demo purposes, return success for any valid email/password
        if login_data.email and login_data.password:
            return {"access_token": "demo_jwt_token", "token_type": "bearer"}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.post("/register")
async def register_user(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """User registration endpoint"""
    try:
        # Check if user already exists
        existing_user = await crud.user.get_by_email(db, email=user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        existing_username = await crud.user.get_by_username(db, username=user_data.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Create new user
        new_user = await crud.user.create(db, obj_in=user_data)
        
        return {
            "message": "User registered successfully",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/refresh")
async def refresh_token(
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Refresh JWT token"""
    # TODO: Implement proper token refresh
    return {"access_token": "refreshed_mock_token", "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
async def get_current_user_info(
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get current user information"""
    return current_user