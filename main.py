from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware as StarletteHeaders
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

# JWT Configuration - No fallback for production security
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    if os.getenv("APP_ENV") == "production":
        raise ValueError("JWT_SECRET_KEY environment variable is required in production")
    else:
        # Development fallback only
        SECRET_KEY = "_aR4aqxoy0m4dIRx7PNrGI20SqruHEwHeHKSyJmlOSw"
        print("⚠️ Using development JWT secret - NOT FOR PRODUCTION")

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

if APP_ENV == "production":
    # Production security middleware
    app.add_middleware(HTTPSRedirectMiddleware)
    
    # Clean hostname for trusted hosts (remove scheme and port)
    clean_host = FRONTEND_URL.replace("https://", "").replace("http://", "").split(":")[0]
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=[clean_host, f"*.{clean_host}"]
    )

# Secure CORS configuration
if APP_ENV == "production":
    # Production: Only allow specific domain
    allowed_origins = [
        f"https://{FRONTEND_URL}" if not FRONTEND_URL.startswith("http") else FRONTEND_URL
    ]
else:
    # Development: Allow localhost variants
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

# Demo user database - DEVELOPMENT ONLY
DEMO_USERS = {}
if APP_ENV == "development":
    print("🔧 Loading demo users for DEVELOPMENT environment")
    DEMO_USERS = {
        "admin@company.com": {
            "password": get_password_hash("admin123"),
            "role": "admin", 
            "first_name": "Admin",
            "last_name": "User",
            "is_active": True
        },
        "hr@company.com": {
            "password": get_password_hash("hr123"),
            "role": "hr",
            "first_name": "HR",
            "last_name": "Manager", 
            "is_active": True
        },
        "employee@company.com": {
            "password": get_password_hash("emp123"),
            "role": "employee",
            "first_name": "John",
            "last_name": "Employee",
            "is_active": True
        }
    }
else:
    print("🔒 Production mode: Demo users DISABLED - Use real database authentication")

@app.get("/")
def read_root():
    return {"message": "CRM + HRMS Pro API is running!", "status": "success"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "CRM+HRMS Pro"}

# Authentication endpoints
@app.post("/api/v1/auth/login", response_model=Token)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login endpoint with proper JWT authentication"""
    try:
        email = login_data.username
        password = login_data.password

        # Production mode: Block demo authentication
        if APP_ENV == "production" and len(DEMO_USERS) > 0:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Demo authentication not available in production. Please implement database authentication.",
            )
            
        # Development mode: Use demo users if database lookup fails
        if APP_ENV == "development" and email in DEMO_USERS:
            user = DEMO_USERS[email]
            user_source = "demo"
        else:
            # Try database lookup (implement when database user model is ready)
            # For now, reject all non-demo logins in production
            if APP_ENV == "production":
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Database authentication not yet implemented. Contact system administrator.",
                )
            else:
                # Development: require demo users
                if email not in DEMO_USERS:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid credentials",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                user = DEMO_USERS[email]
                user_source = "demo"
        
        # Verify password
        if not verify_password(password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if user is active
        if not user.get("is_active", False):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is disabled",
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": email,
                "user_id": 1,  # In production, get from database
                "email": email,
                "first_name": user["first_name"],
                "last_name": user["last_name"], 
                "role": user["role"],
                "is_active": user["is_active"]
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
    """Register new user with proper JWT authentication"""
    try:
        # Production mode: Block registration completely  
        if APP_ENV == "production":
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Registration not available in production. Database authentication not implemented.",
            )
            
        # Development mode only: Demo registration
        if APP_ENV == "development":
            # Check if user already exists in demo users
            if user_data.email in DEMO_USERS:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            
            # Hash password
            hashed_password = get_password_hash(user_data.password)
            
            # Add user to demo database (DEVELOPMENT ONLY)
            DEMO_USERS[user_data.email] = {
                "password": hashed_password,
                "role": "employee",  # Default role
                "first_name": user_data.first_name,
                "last_name": user_data.last_name,
                "is_active": True
            }
            
            # Create access token
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={
                    "sub": user_data.email,
                    "user_id": len(DEMO_USERS),  # In production, get from database
                    "email": user_data.email,
                    "first_name": user_data.first_name,
                    "last_name": user_data.last_name,
                    "role": "employee",
                    "is_active": True
                },
                expires_delta=access_token_expires
            )
            
            return {
                "access_token": access_token,
                "token_type": "bearer"
            }
        else:
            # Fallback: should not reach here
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Registration service unavailable."
            )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )

@app.get("/api/v1/auth/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return current_user

# Analytics endpoint
@app.get("/api/v1/analytics/dashboard")
async def get_dashboard_analytics(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get dashboard analytics data"""
    try:
        # Return mock data for demo
        return {
            "total_users": 156,
            "total_employees": 89,
            "total_companies": 45,
            "total_leads": 234,
            "total_deals": 67,
            "total_projects": 23,
            "total_tasks": 156,
            "revenue_by_stage": [
                {"stage": "Prospecting", "total_value": 250000},
                {"stage": "Discovery", "total_value": 180000},
                {"stage": "Proposal", "total_value": 320000},
                {"stage": "Negotiation", "total_value": 450000},
                {"stage": "Closed Won", "total_value": 890000}
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch analytics: {str(e)}"
        )

# Static files for production deployment
# Check if we have the built React app
build_dir = os.path.join(os.path.dirname(__file__), "frontend", "build")
if os.path.exists(build_dir):
    # Mount static files
    app.mount("/static", StaticFiles(directory=os.path.join(build_dir, "static")), name="static")
    
    # Serve React app for all non-API routes
    @app.get("/{catch_all:path}")
    async def serve_react_app(catch_all: str):
        """Serve React app for all non-API routes in production"""
        # Don't serve React app for API routes
        if catch_all.startswith("api/") or catch_all.startswith("docs") or catch_all.startswith("openapi.json"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        # Serve index.html for all other routes
        return FileResponse(os.path.join(build_dir, "index.html"))

# Create tables on startup
@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

if __name__ == "__main__":
    # Create tables first
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

    # Environment-based configuration
    APP_ENV = os.getenv("APP_ENV", "development")
    PORT = int(os.getenv("PORT", "8000"))
    
    # Determine mode based on environment and port
    is_development = APP_ENV == "development" or PORT == 8000
    
    if is_development:
        # Development mode: Backend on port 8000, React dev server on port 5000
        port = 8000
        host = "localhost"  # Backend only needs localhost in dev
        reload = True
        print(f"🔧 Starting FastAPI backend in DEVELOPMENT mode on {host}:{port}")
        print("📝 Note: React dev server should run on port 5000 with proxy to this backend")
    else:
        # Production mode: Single server on port 5000
        port = PORT if PORT != 8000 else 5000  # Force port 5000 for production
        host = "0.0.0.0"
        reload = False
        print(f"🚀 Starting FastAPI server in PRODUCTION mode on {host}:{port}")
        print("📝 Note: Serving both API and built React app from this server")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )