from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class Database:
    client: AsyncIOMotorClient = None

    def connect(self):
        self.client = AsyncIOMotorClient(settings.MONGO_URI)
        print("Connected to MongoDB")

    def disconnect(self):
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB")

    def get_db(self):
        return self.client

db = Database()

async def get_database() -> AsyncIOMotorClient:
    return db.get_db()

async def get_master_db():
    client = db.get_db()
    return client[settings.MASTER_DB_NAME]
