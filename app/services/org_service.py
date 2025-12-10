from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class OrganizationService:
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.master_db = client[settings.MASTER_DB_NAME]

    async def create_organization_collection(self, org_name: str):
        collection_name = f"org_{org_name.lower().replace(' ', '_')}"
        
        # Explicitly create collection
        # Check if it exists first? create_collection raises if exists
        # But create_organization checked logic.
        
        try:
            await self.master_db.create_collection(collection_name)
        except Exception as e:
            # Maybe it already exists?
            print(f"Collection creation warning: {e}")
            pass
            
        return collection_name

    async def rename_organization_collection(self, old_org_name: str, new_org_name: str):
        old_collection_name = f"org_{old_org_name.lower().replace(' ', '_')}"
        new_collection_name = f"org_{new_org_name.lower().replace(' ', '_')}"
        
        admin_db = self.client.admin
        
        try:
            # We rename using the admin command
            source_ns = f"{settings.MASTER_DB_NAME}.{old_collection_name}"
            target_ns = f"{settings.MASTER_DB_NAME}.{new_collection_name}"
            
            await admin_db.command("renameCollection", source_ns, to=target_ns)
            return new_collection_name
        except Exception as e:
            print(f"Error renaming collection: {e}")
            raise e

    async def delete_organization_collection(self, org_name: str):
        collection_name = f"org_{org_name.lower().replace(' ', '_')}"
        await self.master_db[collection_name].drop()
