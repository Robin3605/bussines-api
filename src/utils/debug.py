
# from src.config.db import db  # ← ¡IMPORTA db, NO client!
# from beanie import init_beanie, PydanticObjectId
# from src.models.products import Products
# from src.models.users import Users

# async def debug():
#     # Re-inicializa Beanie con el MISMO db que usa la app
#     await init_beanie(database=db, document_models=[Products, Users])
    
#     product = await Products.get(PydanticObjectId("68fd4b572a4faf986e45d6f6"))
#     print("PRODUCTO:", product)

#     users = await Users.get(PydanticObjectId("68f828d02c5bfda37ebb4808"))
#     print("USUARIO:", users)

# import asyncio
# asyncio.run(debug())

from bson import ObjectId
from src.models.products import Products
from src.config.db import init_db
import asyncio

async def test():
    await init_db()
    product = await Products.get(ObjectId("690135b1c807d3bbda3050f1"))
    print("🔍 Resultado Products.get():", product)

asyncio.run(test())