from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import org, admin
from app.core.database import db
from app.core.config import settings

app = FastAPI(title="Organization Management Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    db.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    db.disconnect()

app.include_router(org.router, prefix="/org", tags=["Organization"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Organization Management Service"}
