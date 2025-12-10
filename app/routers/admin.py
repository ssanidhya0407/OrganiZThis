from fastapi import APIRouter, Depends, HTTPException, status
from app.models.auth import AdminLogin, Token
from app.core.database import get_master_db
from app.core.security import verify_password, create_access_token
from datetime import timedelta
from app.core.config import settings

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(login_data: AdminLogin, db = Depends(get_master_db)):
    # Find user
    user = await db["users"].find_one({"email": login_data.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(login_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # Include organization info in the token for easy access control?
    # Or just email and lookup on request. 
    # Let's put email in 'sub' and maybe org_name in claims?
    access_token = create_access_token(
        data={"sub": user["email"], "org": user.get("organization_name")},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "admin_email": user["email"],
        "organization_id": user.get("organization_name")
    }
