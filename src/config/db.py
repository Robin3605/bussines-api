from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.config.config import settings
from src.models.users import Users
from src.models.cart import Cart
from src.models.products import Products

client = AsyncIOMotorClient(settings.db_link)
db = client.bussines

async def init_db():
    print(f"INICIALIZANDO BEANIE EN BASE DE DATOS: {db.name}")
    print(f"📦 Modelos a inicializar: {[Users, Products, Cart]}")
    
    await init_beanie(
        database=db,
        document_models=[Users, Products, Cart]
    )
    