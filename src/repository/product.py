from src.models.products import Products
from src.schemas.products import  ProductUpdate
from src.helpers.api_responses import DBError, ConflictError
from bson import ObjectId
from beanie import PydanticObjectId
import traceback
from src.config.db import db

class ProductRepository:
    @staticmethod
    def serialize_product(product):
        data = product.dict()
        data["_id"] = str(product.id)
        data.pop("id", None)
        return data

    @staticmethod
    async def create_product(product: Products):
        try:
            saved_product = await product.insert()

            print("🧠 ID real:", saved_product.id)

            product_dict = saved_product.dict()
            product_dict["_id"] = str(saved_product.id) if saved_product.id else None
            product_dict.pop("id", None)

            print("✅ user_dict final:", product_dict)
            return product_dict
        except Exception as e:
            print("❌ Error exacto al crear producto:", e)
            raise e


    @staticmethod
    async def get_by_id(id: str):
        try:
            object_id = ObjectId(id)

            product3 = await db.products.find_one({"_id": object_id})
            product = Products(**product3)
            
            return product
        except Exception as e:
            print(f"❌ [DEBUG ERROR] Error completo: {traceback.format_exc()}")
            raise DBError(f"Error fetching product by id: {e}")

    @staticmethod
    async def get_all():
        try:
            return await Products.find_all().to_list()
        except Exception as e:
            raise DBError(f"Error fetching products: {e}")

    @staticmethod
    async def update_one(id: str, data: ProductUpdate):
        try:
            product = await ProductRepository.get_by_id(id)
            if not product:
                return None

            update_data = data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(product, key, value)

            await product.save()
            return product
        except Exception as e:
            raise DBError(f"Error updating user: {e}")

    @staticmethod
    async def delete_one(id: str):
        try:
            product = await ProductRepository.get_by_id(id)
            if product:
                await product.delete()
                return True
            return False
        except Exception as e:
            raise DBError(f"Error deleting user: {e}")