from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URL, DATABASE_NAME

class DataBase:
    client: AsyncIOMotorClient = None
    db = None
    orders = None

db = DataBase()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(MONGO_DB_URL)
    db.db = db.client[DATABASE_NAME]
    db.orders = db.db.orders 


async def close_mongo_connection():
    if db.client:
        db.client.close()
    db.client = None
    db.db = None
    db.orders = None

def get_database() -> DataBase:
    return db