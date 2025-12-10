from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class OrganizationCreate(BaseModel):
    organization_name: str
    email: EmailStr
    password: str

class OrganizationUpdate(BaseModel):
    organization_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class OrganizationResponse(BaseModel):
    organization_name: str
    collection_name: str
    admin_email: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "organization_name": "Acme Corp",
                "collection_name": "org_acme_corp",
                "admin_email": "admin@acme.com"
            }
        }
