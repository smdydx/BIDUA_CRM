
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, EmailStr
import uvicorn
import os

# Import database
from app.core.database import get_db, engine, Base

# Import models to ensure they're registered
from app.models.models import *

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "_aR4aqxoy0m4dIRx7PNrGI20SqruHEwHeHKSyJmlOSw")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool

app = FastAPI(
    title="CRM + HRMS Pro API",
    description="Complete CRM and HRMS Management System",
    version="1.0.0"
)

# Security middleware for production
FRONTEND_URL = os.getenv("REPLIT_DEV_DOMAIN", "localhost:5000")
APP_ENV = os.getenv("APP_ENV", "development")

# Add security middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Secure CORS configuration
if APP_ENV == "production":
    allowed_origins = [
        f"https://{FRONTEND_URL}" if not FRONTEND_URL.startswith("http") else FRONTEND_URL
    ]
else:
    allowed_origins = [
        f"https://{FRONTEND_URL}" if not FRONTEND_URL.startswith("http") else FRONTEND_URL,
        "http://localhost:5000", 
        "http://localhost:3000",
        "http://127.0.0.1:5000", 
        "http://127.0.0.1:3000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Security
security = HTTPBearer(auto_error=False)

# Utility functions
def verify_password(plain_password, hashed_password):
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Hash password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verify JWT token and return user data"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_user_by_email(db: Session, email: str):
    """Get user from database by email"""
    return db.query(Users).filter(Users.email == email).first()

def get_user_by_username(db: Session, username: str):
    """Get user from database by username"""
    return db.query(Users).filter(Users.username == username).first()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user with proper JWT verification"""
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = verify_token(credentials.credentials)
    user_data = {
        "id": payload.get("user_id", 1),
        "username": payload.get("sub"),
        "email": payload.get("email"),
        "first_name": payload.get("first_name"),
        "last_name": payload.get("last_name"),
        "role": payload.get("role", "user"),
        "is_active": payload.get("is_active", True)
    }
    return user_data

@app.get("/")
def read_root():
    return {"message": "CRM + HRMS Pro API is running!", "status": "success"}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check with database connectivity test"""
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy", 
            "service": "CRM+HRMS Pro",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )

# Authentication endpoints
@app.post("/api/v1/auth/login", response_model=Token)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login endpoint with real database authentication"""
    try:
        email = login_data.username
        password = login_data.password

        # Get user from database
        user = get_user_by_email(db, email)
        if not user:
            # Try username if email not found
            user = get_user_by_username(db, email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify password
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is disabled",
            )

        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()

        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": user.email,
                "user_id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name, 
                "role": user.role.value,
                "is_active": user.is_active
            },
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Login failed: {str(e)}"
        )

@app.post("/api/v1/auth/register", response_model=Token)
async def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    """Register new user with real database storage"""
    try:
        # Check if user already exists
        existing_user = get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        existing_username = get_user_by_username(db, user_data.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        # Hash password and create user
        hashed_password = get_password_hash(user_data.password)

        new_user = Users(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role=UserRole.EMPLOYEE,  # Default role
            is_active=True
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": new_user.email,
                "user_id": new_user.id,
                "email": new_user.email,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "role": new_user.role.value,
                "is_active": new_user.is_active
            },
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )

@app.get("/api/v1/auth/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return current_user

# Include API routers
from app.api.v1.endpoints import analytics, crm, hr, projects, users

app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(crm.router, prefix="/api/v1/crm", tags=["crm"])
app.include_router(hr.router, prefix="/api/v1/hr", tags=["hr"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

# Static files for production deployment
build_dir = os.path.join(os.path.dirname(__file__), "frontend", "build")
if os.path.exists(build_dir):
    app.mount("/static", StaticFiles(directory=os.path.join(build_dir, "static")), name="static")

    @app.get("/{catch_all:path}")
    async def serve_react_app(catch_all: str):
        """Serve React app for all non-API routes in production"""
        if catch_all.startswith("api/") or catch_all.startswith("docs") or catch_all.startswith("openapi.json"):
            raise HTTPException(status_code=404, detail="API endpoint not found")

        return FileResponse(os.path.join(build_dir, "index.html"))

if __name__ == "__main__":
    APP_ENV = os.getenv("APP_ENV", "production")
    PORT = int(os.getenv("PORT", "5000"))
    
    # Always use production settings on Replit
    host = "0.0.0.0"
    port = PORT
    reload = False
    print(f"🚀 Starting CRM+HRMS Pro Server on {host}:{port}")
    print(f"📊 API Documentation: https://{os.getenv('REPLIT_DEV_DOMAIN', 'localhost:5000')}/docs")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
