from fastapi import APIRouter, Depends, HTTPException, status
from app.models.organization import OrganizationCreate, OrganizationResponse, OrganizationUpdate
from app.services.org_service import OrganizationService
from app.core.database import get_database, get_master_db
from app.core.security import get_password_hash, get_current_admin
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()

def get_org_service(client: AsyncIOMotorClient = Depends(get_database)):
    return OrganizationService(client)

@router.post("/create", response_model=OrganizationResponse)
async def create_organization(
    org: OrganizationCreate,
    db = Depends(get_master_db),
    org_service: OrganizationService = Depends(get_org_service)
):
    # 1. Validate organization name does not exist
    existing_org = await db["organizations"].find_one({"organization_name": org.organization_name})
    if existing_org:
        raise HTTPException(status_code=400, detail="Organization already exists")
    
    # 2. Dynamically create a new collection
    collection_name = await org_service.create_organization_collection(org.organization_name)
    
    # 3. Create admin user (check if email unique?)
    existing_user = await db["users"].find_one({"email": org.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Admin email already exists")

    hashed_password = get_password_hash(org.password)
    admin_user = {
        "email": org.email,
        "password_hash": hashed_password,
        "organization_name": org.organization_name
    }
    await db["users"].insert_one(admin_user)
    
    # 4. Store metadata
    org_doc = {
        "organization_name": org.organization_name,
        "collection_name": collection_name,
        "admin_email": org.email,
        # Connection details can be added here if we were using multi-DB
    }
    await db["organizations"].insert_one(org_doc)
    
    return OrganizationResponse(**org_doc)

@router.get("/get", response_model=OrganizationResponse)
async def get_organization(organization_name: str, db = Depends(get_master_db)):
    org_doc = await db["organizations"].find_one({"organization_name": organization_name})
    if not org_doc:
        raise HTTPException(status_code=404, detail="Organization not found")
    return OrganizationResponse(**org_doc)

@router.put("/update", response_model=OrganizationResponse)
async def update_organization(
    org_update: OrganizationUpdate,
    db = Depends(get_master_db),
    org_service: OrganizationService = Depends(get_org_service),
    current_user = Depends(get_current_admin)
):
    # Requirement: "Dynamically handle the new collection creation ... and sync existing data"
    # This implies we are UPDATING data for the organization identified by...?
    # The input has `organization_name`.
    # Is `organization_name` the OLD name (target) or the NEW name?
    # Usually `PUT` payload has the new state.
    # But how do we know WHICH org to update if we don't pass an ID in URL?
    # Requirement: "Input: organization_name, email, password".
    # And "Validate that the organization name does not already exist". This implies `organization_name` is the NEW name?
    # IF so, which org are we updating? The one the admin belongs to?
    # "Allow deletion for respective authenticated user only". Same logic likely applies to update.
    # So we update the org that `current_user` belongs to.
    
    current_org_name = current_user["organization_name"]
    
    # Prepare update data
    update_data = {}
    
    # If name is changing
    new_collection_name = None
    if org_update.organization_name and org_update.organization_name != current_org_name:
        # Check uniqueness
        if await db["organizations"].find_one({"organization_name": org_update.organization_name}):
            raise HTTPException(status_code=400, detail="Organization name already taken")
        
        # Rename collection
        try:
            new_collection_name = await org_service.rename_organization_collection(current_org_name, org_update.organization_name)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to rename collection: {str(e)}")
            
        update_data["organization_name"] = org_update.organization_name
        update_data["collection_name"] = new_collection_name
        
        # Also update the user's link?
        # Yes, we should update ALL users linked to this org.
        await db["users"].update_many(
            {"organization_name": current_org_name},
            {"$set": {"organization_name": org_update.organization_name}}
        )

    if org_update.email:
         # Check email uniqueness if changing?
         if org_update.email != current_user["email"]:
             if await db["users"].find_one({"email": org_update.email}):
                 raise HTTPException(status_code=400, detail="Email already taken")
             # Update admin email
             await db["users"].update_one(
                 {"_id": current_user["_id"]},
                 {"$set": {"email": org_update.email}}
             )
             update_data["admin_email"] = org_update.email

    if org_update.password:
        hashed = get_password_hash(org_update.password)
        await db["users"].update_one(
                 {"_id": current_user["_id"]},
                 {"$set": {"password_hash": hashed}}
             )

    if update_data:
        await db["organizations"].update_one(
            {"organization_name": current_org_name},
            {"$set": update_data}
        )
    
    # Return updated detail
    # We need to fetch it again because `current_org_name` might have changed
    target_name = org_update.organization_name if org_update.organization_name else current_org_name
    
    org_doc = await db["organizations"].find_one({"organization_name": target_name})
    return OrganizationResponse(**org_doc)

@router.delete("/delete")
async def delete_organization(
    organization_name: str,
    db = Depends(get_master_db),
    org_service: OrganizationService = Depends(get_org_service),
    current_user = Depends(get_current_admin)
):
    # "Allow deletion for respective authenticated user only"
    if current_user["organization_name"] != organization_name:
        raise HTTPException(status_code=403, detail="Not authorized to delete this organization")
        
    # Delete collection
    await org_service.delete_organization_collection(organization_name)
    
    # Delete metadata
    await db["organizations"].delete_one({"organization_name": organization_name})
    
    # Delete admin user(s)?
    # Prudence says yes, clean up users associated.
    await db["users"].delete_many({"organization_name": organization_name})
    
    return {"message": "Organization deleted successfully"}
