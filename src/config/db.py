from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.config.config import settings
from src.models.users import Users
from src.models.cart import Cart

client = AsyncIOMotorClient(settings.db_link)
db = client.get_default_database()

async def init_db():
    await init_beanie(
        database=db,
        document_models=[Users, Cart]
    )